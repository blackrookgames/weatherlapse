import geopandas as gpd
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import sys

from pathlib import Path
from PIL import Image

def error(message):
    print(f"ERROR: {message}", file = sys.stderr)
    return 1

def main():
    path_dir = Path(sys.argv[0]).resolve().parent.joinpath("secret").joinpath("test.output")
    path_geo = path_dir.joinpath("test.geojson")
    path0_png = path_dir.joinpath("test0.png")
    path1_png = path_dir.joinpath("test1.png")
    # Get geo
    if not path_geo.is_file():
        print("Geo not found; creating")
        # Fetch country data
        print("  Fetching")
        _url = "https://www.geoboundaries.org/api/current/gbOpen/ALL/ADM0/"
        _response = requests.get(_url)
        if _response.status_code != 200:
            return error(f"{_url} Status code {_response.status_code}")
        # Loop thru each country
        _data = json.loads(_response.content)
        print(f"  {len(_data)} countries found")
        _gdfs:list[gpd.GeoDataFrame] = []
        for _i in range(len(_data)):
            _country = _data[_i]
            # iso
            _geo_iso = _country.get('boundaryISO', '')
            if _geo_iso == '': continue
            # url
            _geo_url = _country.get('simplifiedGeometryGeoJSON', '')
            if _geo_url == '': continue
            # Fetch
            print(f"    {_geo_iso} {(_i + 1)}/{len(_data)}")
            _geo_response = requests.get(_geo_url)
            if _geo_response.status_code != 200:
                return error(f"{_geo_url} Status code {_geo_response.status_code}")
            # Load
            _gdfs.append(gpd.read_file(_geo_response.content)) # type: ignore
            # Next
            _i += 1
        # Composite
        print("  Compositing")
        geo = pd.concat(_gdfs, ignore_index = True)
        geo.to_file(path_geo, driver='GeoJSON') # type: ignore
    else:
        print("Loading geo")
        geo = gpd.read_file(path_geo)
    # Plot
    print("Plotting 0")
    ax = geo.plot(color = '#FFFFFF40', edgecolor = 'black', linewidth = 0.3)
    ax.margins(0)
    ax.set_aspect('auto')
    plt.axis('off') # Remove coordinates for a clean PNG
    fig = plt.gcf() # Get current figure
    fig.set_size_inches(10, 10)
    fig.savefig(path0_png, dpi = 300, bbox_inches = 'tight', pad_inches = 0.0, transparent = True)
    plt.cla()
    print("Plotting 1")
    ax = geo.plot(color = 'green', edgecolor = 'none')
    ax.margins(0)
    ax.set_aspect('auto')
    plt.axis('off') # Remove coordinates for a clean PNG
    fig = plt.gcf() # Get current figure
    fig.set_size_inches(10, 10)
    fig.savefig(path1_png, dpi = 300, bbox_inches = 'tight', pad_inches = 0.0, transparent = True)


    # Success!!!
    return 0

if __name__ == "__main__" and len(sys.argv) > 0:
    sys.exit(main())