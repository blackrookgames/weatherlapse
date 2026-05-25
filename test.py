import geopandas as gpd
import io
import mapbox_vector_tile
import matplotlib.pyplot as plt
import pandas as pd
import requests
import sys

from pathlib import Path
from PIL import Image
from shapely.geometry import LineString, shape
from shapely.ops import linemerge

def polygon_to_segments(poly):
# Get exterior coordinates
    b = poly.exterior.coords
# Create a LineString for each segment
    return [LineString(b[k:k+2]) for k in range(len(b) - 1)]

def fetch(z, x, y, api_key):
    # osm
    def osm():
        nonlocal z, x, y
        # Fetch
        print("Fetch")
        osm_url = f"https://vector.openstreetmap.org/shortbread_v1/{z}/{x}/{y}.mvt"
        osm_headers = {"User-Agent": "WeatherApp/1.0 (blackrookgames@gmail.com)"}
        osm_response = requests.get(osm_url, headers = osm_headers)
        if osm_response.status_code != 200:
            print(f"OSM Error: {osm_response.status_code}", file = sys.stderr)
            return False
        # Decode
        print("Decode")
        decoded_tile = mapbox_vector_tile.decode(osm_response.content)
        gdfs = {}
        for layer_name, layer_data in decoded_tile.items():
            features = []
            for feature in layer_data["features"]:
                # Extract properties (attributes)
                properties = feature["properties"]
                # Convert the MVT geometry dict into a Shapely geometry object
                geometry = shape(feature["geometry"])
                # Combine geometry and properties into a single dictionary
                feature_dict = {"geometry": geometry, **properties}
                features.append(feature_dict)
            # 3. Create the GeoDataFrame for this specific layer
            if features:
                gdf = gpd.GeoDataFrame(features, crs = "EPSG:3857")
                gdfs[layer_name] = gdf
        # 4. Access and plot your target layer
        # Plot
        print("Plot")
        geo_raw = gdfs["ocean"]
        assert isinstance(geo_raw, gpd.GeoDataFrame)
        # 1. Generate ALL boundaries (captures exterior paths AND interior continent holes)
        geo = geo_raw.copy()
        geo['geometry'] = geo.boundary
        # 2. Explode the resulting MultiLineStrings into individual LineString rows
        geo = geo.explode(index_parts=False)
        # 3. Standardize the geometries to clean LineStrings
        geo['geometry'] = [LineString(geom.coords) if geom else None for geom in geo.geometry] # type: ignore
        # Test
        xmin, ymin, xmax, ymax = geo.total_bounds
        grid_width = xmax - xmin
        grid_height = ymax - ymin
        tol = 0.1
        def strip_canvas_borders(line):
            if not line: return None
            coords = list(line.coords)
            clean_segments = []
            # Evaluate every individual point-to-point segment
            for i in range(len(coords) - 1):
                p1, p2 = coords[i], coords[i+1]
                # Check if BOTH points sit on the exact same border wall
                on_left   = abs(p1[0] - xmin) < tol and abs(p2[0] - xmin) < tol
                on_right  = abs(p1[0] - xmax) < tol and abs(p2[0] - xmax) < tol
                on_bottom = abs(p1[1] - ymin) < tol and abs(p2[1] - ymin) < tol
                on_top    = abs(p1[1] - ymax) < tol and abs(p2[1] - ymax) < tol
                # If the segment belongs to the outer frame, discard it
                if on_left or on_right or on_bottom or on_top:
                    continue
                clean_segments.append(LineString([p1, p2]))
            if not clean_segments:
                return None
            # Stitch the surviving non-border pieces back into a continuous line
            return linemerge(clean_segments)
        # Apply the segment-level filter
        geo['geometry'] = geo.geometry.apply(strip_canvas_borders) # type: ignore
        # Drop any lines that were completely made of border edges
        geo = geo[geo.geometry.notnull()]
        geo = geo.explode(index_parts=False)
        # 4. Render with the correct stroke properties
        ax = geo.plot(edgecolor='black', linewidth=0.3)
        ax.margins(0)
        ax.set_aspect('equal')
        ax.set_xlim(0, 2048)
        ax.set_ylim(0, 2048)
        plt.axis('off') # Remove coordinates for a clean PNG
        fig = plt.gcf() # Get current figure
        fig.set_size_inches(1, 1)
        fig.subplots_adjust(left = 0, right = 1, bottom = 0, top = 1, wspace = 0, hspace = 0)
        fig.savefig("test.osm.png", dpi = 256, pad_inches = 0.0, transparent = True)
        # Success!!!
        return True
    def owm():
        nonlocal z, x, y, api_key
        # Fetch
        print("Fetch")
        owm_url = f"https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png"
        owm_params = {"appid": api_key}
        owm_response = requests.get(owm_url, params = owm_params)
        if owm_response.status_code != 200:
            print(f"OWM Error: {owm_response.status_code}", file = sys.stderr)
            return False
        # Render
        print("Render")
        image = Image.open(io.BytesIO(owm_response.content)).convert("RGBA")
        image.save("test.owm.png")
        # Success!!!
        return True
    if not osm(): return False
    if not owm(): return False
    return True
    

def main():
    # Determine directory
    if len(sys.argv) > 0:
        main_dir_path = Path(sys.argv[0]).resolve().parent
    else: 
        main_dir_path = Path('.').resolve()
    # Get secret
    secret_dir_path = main_dir_path.joinpath("secret")
    secret_key_path = secret_dir_path.joinpath("key")
    with open(secret_key_path, 'r') as _f:
        secret_key = _f.read().strip()
    # Request
    if not fetch(1, 0, 0, secret_key): return 1
    # Success
    return 0

if __name__ == "__main__":
    sys.exit(main())