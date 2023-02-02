import requests
from tempfile import NamedTemporaryFile

def download_raster(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        with NamedTemporaryFile(delete=False, suffix='.tif') as f:
            f.write(response.content)
            return f.name
    else:
        raise Exception("Unable to download raster from URL, status code: {}".format(response.status_code))