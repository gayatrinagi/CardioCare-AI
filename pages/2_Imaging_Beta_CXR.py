# pages/2_Imaging_Beta_CXR.py
import io
import numpy as np
import streamlit as st

# Optional imaging deps
try:
    import cv2
    from skimage import measure
    import pydicom
    _IMAGING_READY = True
except Exception:
    _IMAGING_READY = False

st.title("🫁 Imaging (beta): Post-COVID Lung Opacities (heuristic)")

# Login gate
if not st.session_state.get("logged_in", False):
    st.warning("🔒 Please log in on the **0_Login** page to use Imaging.")
    st.stop()

st.caption(
    "Upload a chest X-ray (PNG/JPG/DICOM). We’ll segment lungs and highlight brighter-than-expected regions "
    "(e.g., ground-glass / consolidation). **Research use only — not diagnostic.**"
)

if not _IMAGING_READY:
    st.error("Imaging dependencies missing. Install: `py -m pip install opencv-python-headless pydicom scikit-image`")
    st.stop()

# ---------- Utils ----------
def read_cxr_file(uploaded_file):
    name = uploaded_file.name.lower()
    data = uploaded_file.read()
    if name.endswith((".dcm", ".dicom")):
        ds = pydicom.dcmread(io.BytesIO(data))
        arr = ds.pixel_array.astype(np.float32)
        slope = float(getattr(ds, "RescaleSlope", 1.0))
        intercept = float(getattr(ds, "RescaleIntercept", 0.0))
        arr = arr * slope + intercept
        photometric = getattr(ds, "PhotometricInterpretation", "MONOCHROME2")
        if photometric and str(photometric).upper() == "MONOCHROME1":
            arr = arr.max() - arr
        img = arr
    else:
        img_gray = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_GRAYSCALE)
        if img_gray is None:
            raise ValueError("Unsupported or corrupted image file.")
        img = img_gray.astype(np.float32)
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return img

def preprocess(img, target=512):
    img = cv2.resize(img, (target, target), interpolation=cv2.INTER_AREA)
    img = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(img)
    img = cv2.medianBlur(img, 3)
    return img

def lung_mask_quick(img):
    inv = cv2.bitwise_not(img)
    _, th = cv2.threshold(inv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((5,5), np.uint8), iterations=2)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(th, connectivity=8)
    if num <= 1:
        return np.zeros_like(img, dtype=np.uint8)
    areas = [(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num)]
    areas.sort(key=lambda x: x[1], reverse=True)
    keep = [i for i,_ in areas[:2]]
    mask = np.isin(labels, keep).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9,9), np.uint8), iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5,5), np.uint8), iterations=1)
    return mask

def abnormal_map_zscore(img, lung_mask, z_thresh=1.0, min_region_px=300):
    """Bright-abnormal mask using Z-score within lung pixels."""
    lung_pixels = img[lung_mask > 0].astype(np.float32)
    if lung_pixels.size < 1000:
        return np.zeros_like(img, dtype=np.uint8), None
    mu = float(lung_pixels.mean())
    sd = float(lung_pixels.std() + 1e-6)
    z = (cv2.GaussianBlur(img, (0,0), 1.0).astype(np.float32) - mu) / sd
    abn = np.zeros_like(img, dtype=np.uint8)
    abn[(z > float(z_thresh)) & (lung_mask > 0)] = 255

    abn = cv2.morphologyEx(abn, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=1)
    abn = cv2.morphologyEx(abn, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8), iterations=1)

    lab = measure.label(abn > 0, connectivity=2)
    cleaned = np.zeros_like(abn)
    for region in measure.regionprops(lab):
        if region.area >= int(min_region_px):
            cleaned[lab == region.label] = 255
    return cleaned, {"mean": mu, "std": sd, "z_thresh": z_thresh}

def abnormal_map_percentile(img, lung_mask, pct_thresh=90, min_region_px=300):
    """Bright-abnormal mask using intensity percentile within lung pixels."""
    lung_vals = img[lung_mask > 0].astype(np.float32)
    if lung_vals.size < 1000:
        return np.zeros_like(img, dtype=np.uint8), None
    thr = float(np.percentile(lung_vals, pct_thresh))
    abn = np.zeros_like(img, dtype=np.uint8)
    abn[(img >= thr) & (lung_mask > 0)] = 255

    abn = cv2.morphologyEx(abn, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=1)
    abn = cv2.morphologyEx(abn, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8), iterations=1)

    lab = measure.label(abn > 0, connectivity=2)
    cleaned = np.zeros_like(abn)
    for region in measure.regionprops(lab):
        if region.area >= int(min_region_px):
            cleaned[lab == region.label] = 255
    return cleaned, {"pct_thresh": pct_thresh, "intensity_thr": thr}

def color_overlay(gray_0_255, heat_0_255, alpha=0.45):
    gray_rgb = cv2.cvtColor(gray_0_255, cv2.COLOR_GRAY2BGR)
    color = cv2.applyColorMap(heat_0_255, cv2.COLORMAP_JET)
    return cv2.addWeighted(gray_rgb, 1.0, color, float(alpha), 0.0)

def pct(n, d): 
    return float(n) * 100.0 / float(d) if d > 0 else 0.0

# ---------- Controls ----------
with st.sidebar:
    st.header("Detection Settings")
    method = st.selectbox("Threshold method", ["Z-score (bright)", "Percentile (bright)"])
    if method.startswith("Z-score"):
        z_thresh = st.slider("Sensitivity (Z-score threshold)", 0.3, 2.5, 0.9, 0.05,
                             help="Lower → more sensitive (more areas flagged).")
        pct_thresh = None
    else:
        pct_thresh = st.slider("Top intensity percentile", 80, 99, 90, 1,
                               help="Flag top X% brightest pixels inside lungs.")
        z_thresh = None

    min_region = st.slider("Min region size (pixels)", 50, 2000, 200, 50,
                           help="Filters tiny specks of noise.")
    mask_pad = st.slider("Mask padding (px)", 0, 15, 5, 1,
                         help="Dilate lung mask to include pleura/periphery.")
    alpha = st.slider("Overlay opacity", 0.1, 0.9, 0.45, 0.05)
    target_size = st.select_slider("Working resolution", options=[384, 448, 512, 640], value=512)
    debug = st.toggle("Show debug details", value=False)

uploaded = st.file_uploader(
    "Upload chest X-ray", type=["png","jpg","jpeg","dcm","dicom"], accept_multiple_files=False
)
if not uploaded:
    st.info("Supported: PNG, JPG/JPEG, DICOM. For CT series, use a representative slice for now.")
    st.stop()

# ---------- Run ----------
try:
    img_raw = read_cxr_file(uploaded)
    img = preprocess(img_raw, target=target_size)
    lung = lung_mask_quick(img)

    # Optional padding of lung mask to include periphery
    if mask_pad > 0:
        kernel = np.ones((mask_pad, mask_pad), np.uint8)
        lung = cv2.dilate(lung, kernel, iterations=1)

    # Sanity check on mask size (too small = under-segmentation → % affected looks small)
    total_pixels = img.size
    lung_pixels = int((lung > 0).sum())
    lung_ratio = lung_pixels / float(total_pixels)
    if lung_ratio < 0.10:
        st.warning(
            f"⚠️ Lung mask is very small ({lung_ratio*100:.1f}% of image). "
            "This often underestimates % affected. Try increasing mask padding, "
            "or use a higher working resolution."
        )

    # Abnormal map via chosen method
    if method.startswith("Z-score"):
        abn, info = abnormal_map_zscore(img, lung, z_thresh=z_thresh, min_region_px=min_region)
        threshold_expl = f"Z-score > {info['z_thresh']:.2f} (mean={info['mean']:.1f}, std={info['std']:.1f})" if info else "n/a"
    else:
        abn, info = abnormal_map_percentile(img, lung, pct_thresh=pct_thresh, min_region_px=min_region)
        threshold_expl = f"Top {info['pct_thresh']}% brightest (intensity ≥ {info['intensity_thr']:.1f})" if info else "n/a"

    heat = cv2.normalize(abn, None, 0, 255, cv2.NORM_MINMAX)
    overlay = color_overlay(img, heat, alpha=alpha)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(img, clamp=True, use_container_width=True, caption="Input (processed)")
    with c2:
        st.image(lung, clamp=True, use_container_width=True, caption="Lung Mask (quick + padding)")
    with c3:
        st.image(overlay, channels="BGR", use_container_width=True, caption="Opacity Map (overlay)")

    # Metrics & explanation
    total_lung = int((lung > 0).sum())
    total_abn = int((abn > 0).sum())
    percent_affected = pct(total_abn, total_lung)

    st.markdown("---")
    st.subheader("Quantitative cues (heuristic)")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Lung affected", f"{percent_affected:.1f}%")
    with m2:
        st.metric("Lung pixels (mask)", f"{total_lung:,}")
    with m3:
        st.metric("Flagged pixels", f"{total_abn:,}")

    st.markdown(
        f"""
        **How we computed this**  
        - We create a lung mask (white areas) and only analyze pixels **inside** it.  
        - We flag pixels as **bright-abnormal** using **{threshold_expl}**.  
        - **% Lung affected = (Flagged pixels ÷ Lung pixels) × 100**.  
        """
    )

    if debug:
        st.markdown("##### Debug details")
        st.write({
            "threshold_method": "zscore" if method.startswith("Z-score") else "percentile",
            "threshold_explained": threshold_expl,
            "total_image_pixels": int(total_pixels),
            "lung_pixels": int(total_lung),
            "flagged_pixels": int(total_abn),
            "lung_ratio_of_image_%": float(lung_ratio*100.0),
            "min_region_px": int(min_region),
            "mask_padding_px": int(mask_pad),
            "working_resolution": int(target_size),
        })

    # Download overlay
    out_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
    ok, buf = cv2.imencode(".png", out_rgb)
    if ok:
        st.download_button("⬇️ Download overlay PNG", data=buf.tobytes(), file_name="cxr_overlay.png", mime="image/png")

    st.info(
        "Interpretation tips:\n"
        "- **Higher % affected** suggests more extensive opacities.\n"
        "- Post-COVID often shows **peripheral** and sometimes **lower-zone** predominance.\n"
        "- Underestimation can happen if the lung mask is too small/tight, the threshold is high, or small regions are filtered out.\n"
        "These are heuristics only—confirm with a clinician and proper models."
    )
except Exception as e:
    st.error(f"Could not process this file: {e}")
