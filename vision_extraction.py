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

def pixel_to_lat_lon(px, py, center_lat, center_lon, zoom=16, tile_size=256, grid_size=3):
    """Converts a local pixel coordinate from a stitched tile grid back to a global geographic coordinate"""
    x_center, y_center = lat_lon_to_tile_xy(center_lat, center_lon, zoom)
    
    offset = grid_size // 2
    top_left_x_tile = x_center - offset
    top_left_y_tile = y_center - offset
    
    n = 2.0 ** zoom
    fractional_x = top_left_x_tile + (px / tile_size)
    fractional_y = top_left_y_tile + (py / tile_size)
    
    lon_deg = fractional_x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * fractional_y / n)))
    lat_deg = math.degrees(lat_rad)
    
    return lat_deg, lon_deg

def prune_skeleton(skel, num_iter=30):
    """Prunes dangling branches (spurs) from a skeletonized image to create a clean planar graph."""
    skel = skel.copy()
    kernel = np.array([[1, 1, 1],
                       [1, 10, 1],
                       [1, 1, 1]])
    for _ in range(num_iter):
        neighbor_count = convolve(skel.astype(int), kernel, mode='constant', cval=0)
        endpoints = (neighbor_count == 11)
        if not np.any(endpoints):
            break
        skel[endpoints] = False
    return skel

def classify_land_cover(mean_color):
    """Simple heuristic land cover classification based on the mean RGB color of a field."""
    r, g, b = mean_color[:3]
    
    # Vegetation: Green channel is significantly higher
    if g > r + 5 and g > b + 5:
        return "Crop Land (Vegetation)", (42, 246, 178) # Bright Green
    # Water: Blue dominant and generally dark
    elif b > r and b > g and (r + g + b) < 350:
        return "Water Body", (50, 150, 255) # Blue
    # Built-up / Urban: Desaturated, high overall brightness
    elif abs(r-g) < 25 and abs(r-b) < 25 and r > 100:
        return "Built-up Area", (200, 200, 200) # Gray
    # Barren / Fallow: Brownish/Yellow (Red and Green high, Blue low)
    else:
        return "Barren / Fallow Land", (205, 133, 63) # Brown

def fetch_arcgis_satellite_imagery(lat, lon, zoom=16, grid_size=3):
    """Fetches a live high-res satellite tile grid from the ArcGIS REST API"""
    x_center, y_center = lat_lon_to_tile_xy(lat, lon, zoom)
    
    offset = grid_size // 2
    stitched_rows = []
    
    for dy in range(-offset, offset + 1):
        y_tile = y_center + dy
        row_images = []
        for dx in range(-offset, offset + 1):
            x_tile = x_center + dx
            url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y_tile}/{x_tile}"
            
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    image_bytes = np.asarray(bytearray(response.read()), dtype="uint8")
                    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    row_images.append(image_rgb)
            except Exception as e:
                print(f"Failed to fetch tile {x_tile},{y_tile}: {e}")
                # Fallback to a solid dark image if no internet
                row_images.append(np.zeros((256, 256, 3), dtype=np.uint8))
        
        # Horizontally stack the tiles in this row
        stitched_rows.append(np.hstack(row_images))
    
    # Vertically stack all the rows
    final_image = np.vstack(stitched_rows)
    return final_image

def extract_field_boundaries(image_rgb, center_lat, center_lon, zoom=16):
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
    
    # Base mask for computing mean color of each polygon
    base_mask = np.zeros(image_rgb.shape[:2], dtype=np.uint8)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100 and area < 25000: # Typical field size bounds for Zoom 16
            valid_fields_count += 1
            
            # Smooth the polygon (simplify the geometry into a clean vector)
            epsilon = 0.005 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Compute Mean Color to classify land cover
            mask = base_mask.copy()
            cv2.drawContours(mask, [approx], -1, 255, -1)
            mean_color = cv2.mean(image_rgb, mask=mask)
            
            lc_class, lc_color = classify_land_cover(mean_color)
            
            geo_polygon = []
            for point in approx:
                px, py = point[0]
                plat, plon = pixel_to_lat_lon(px, py, center_lat, center_lon, zoom)
                geo_polygon.append([plon, plat]) # PyDeck expects [longitude, latitude]
            
            valid_contours.append({
                "geometry": approx,
                "geo_polygon": geo_polygon,
                "class": lc_class,
                "color": lc_color
            })
            
            # Draw AI mask polygon outline with semantic color
            cv2.drawContours(overlay, [approx], -1, lc_color, 2)
            # Add a semantic fill overlay for the polygon interior
            fill_overlay = overlay.copy()
            cv2.drawContours(fill_overlay, [approx], -1, lc_color, cv2.FILLED)
            cv2.addWeighted(fill_overlay, 0.4, overlay, 0.6, 0, overlay)

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
