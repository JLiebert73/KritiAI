import cv2
import numpy as np
import urllib.request
import math
from skimage.morphology import skeletonize
from scipy.ndimage import convolve

def lat_lon_to_tile_xy(lat, lon, zoom):
    """Converts Latitude/Longitude to Web Mercator XYZ Tile Coordinates"""
    n = 2.0 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x_tile, y_tile

def prune_skeleton(skel, num_iter=30):
    """Prunes dangling branches (spurs) from a skeletonized image to create a clean planar graph."""
    skel = skel.copy()
    kernel = np.array([[1, 1, 1],
                       [1, 10, 1],
                       [1, 1, 1]])
    for _ in range(num_iter):
        neighbor_count = convolve(skel.astype(int), kernel, mode='constant', cval=0)
        # Endpoints are pixels that are True (10) and have exactly 1 neighbor (1) -> 11
        endpoints = (neighbor_count == 11)
        if not np.any(endpoints):
            break
        skel[endpoints] = False
    return skel

def fetch_arcgis_satellite_imagery(lat, lon, zoom=16):
    """Fetches a live high-res satellite tile from the ArcGIS REST API"""
    x, y = lat_lon_to_tile_xy(lat, lon, zoom)
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            image_bytes = np.asarray(bytearray(response.read()), dtype="uint8")
            image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
            # OpenCV loads as BGR, convert to RGB for Streamlit displaying
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return image_rgb
    except Exception as e:
        print(f"Failed to fetch tile: {e}")
        # Fallback to a solid dark image if no internet
        return np.zeros((256, 256, 3), dtype=np.uint8)

def extract_field_boundaries(image_rgb):
    """
    Simulates a heavy segmentation model (like SAM or DINO) by using a lightning-fast
    OpenCV morphological pipeline to extract agricultural field boundaries.
    """
    # 1. Convert to grayscale for feature extraction
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    
    # 2. Gaussian blur to remove ambient sensor noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Canny Edge Detection (extracting raw boundaries)
    # Using specific thresholds adapted for agricultural satellite imagery
    edges = cv2.Canny(blurred, 30, 100)
    
    # 4. Morphological Transformations to close the polygons
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=2)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # 5. Extract Contours (Polygons) of the actual fields!
    # The 'closed' mask has white edges and black fields. Invert it so fields are white.
    fields_mask = cv2.bitwise_not(closed)
    contours, _ = cv2.findContours(fields_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # 6. Apply Skeletonization to the edges to extract pure topological centerlines
    # This reduces the thick white boundaries to 1-pixel thin lines
    bool_mask = closed > 0
    raw_skeleton = skeletonize(bool_mask)
    
    # Prune stray dangling edges to make the graph perfectly planar
    clean_skeleton = prune_skeleton(raw_skeleton, num_iter=45)
    
    skeleton_uint8 = (clean_skeleton * 255).astype(np.uint8)
    skeleton_rgb = cv2.cvtColor(skeleton_uint8, cv2.COLOR_GRAY2RGB)
    
    overlay = image_rgb.copy()
    valid_fields_count = 0
    valid_contours = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100 and area < 60000: # Typical field size bounds for higher zoom levels
            valid_fields_count += 1
            
            # Smooth the polygon (simplify the geometry into a clean vector)
            epsilon = 0.005 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            valid_contours.append(approx)
            
            # Draw highly visible AI mask polygon outline (Bright Cyan/Green)
            cv2.drawContours(overlay, [approx], -1, (42, 246, 178), 2)
            # Add a faint fill overlay for the polygon interior
            fill_overlay = overlay.copy()
            cv2.drawContours(fill_overlay, [approx], -1, (42, 246, 178), cv2.FILLED)
            cv2.addWeighted(fill_overlay, 0.2, overlay, 0.8, 0, overlay)

    # Convert the binary edge mask to RGB so Streamlit can display it
    mask_rgb = cv2.cvtColor(closed, cv2.COLOR_GRAY2RGB)
    
    return mask_rgb, skeleton_rgb, overlay, valid_fields_count, valid_contours

if __name__ == "__main__":
    # Test execution
    # Kamrup, Assam agricultural region
    lat, lon = 26.2343, 91.5644
    img = fetch_arcgis_satellite_imagery(lat, lon, zoom=16)
    mask, skel, overlay, count, v_contours = extract_field_boundaries(img)
    print(f"Successfully extracted {count} field polygons with skeleton topology.")
