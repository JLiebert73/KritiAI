import cv2
import numpy as np
import plotly.graph_objects as go
from vision_extraction import fetch_arcgis_satellite_imagery, extract_field_boundaries

img = fetch_arcgis_satellite_imagery(26.2343, 91.5644, zoom=16)
mask, skel, overlay, count, contours = extract_field_boundaries(img)

fig = go.Figure()
fig.add_trace(go.Image(z=img))

owners = ["Bipul Das", "Dipankar Saikia", "Meera Gogoi", "Raju Das", "Anita Borah"]

for contour in contours:
    x = contour[:, 0, 0]
    y = contour[:, 0, 1]
    
    # Close polygon
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    
    area = cv2.contourArea(contour)
    
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        fill="toself",
        fillcolor="rgba(42, 246, 178, 0.4)",
        line=dict(color="rgb(42, 246, 178)", width=2),
        hoverinfo="text",
        text=f"Owner: {np.random.choice(owners)}<br>Area: {int(area)} px²",
        showlegend=False
    ))

# Important: Plotly Image traces don't automatically flip the Y axis for scatter plots drawn on top.
# But go.Image handles the coordinate system such that (0,0) is bottom left for scatters, BUT top-left for the image?
# Actually, go.Image puts (0,0) at the bottom left by default?
# Let's save it to HTML and see if it aligns.
fig.write_html("test_plotly.html")
print("Done")
