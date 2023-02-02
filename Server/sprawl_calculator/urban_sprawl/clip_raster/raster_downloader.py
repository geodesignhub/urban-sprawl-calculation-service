import requests
from tempfile import NamedTemporaryFile

def download_raster(url):
    response = requests.get(url)
    with NamedTemporaryFile(delete=False, suffix='.tif') as f:
        f.write(response.content)
        return f.name