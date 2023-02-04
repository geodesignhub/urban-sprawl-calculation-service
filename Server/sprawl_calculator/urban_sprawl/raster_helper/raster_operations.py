import rasterio
from rasterio.mask import mask
from tempfile import NamedTemporaryFile
from data_definitions import GeoJSONFeature

def clip_raster_with_geojson(raster_file: NamedTemporaryFile, geojson:GeoJSONFeature) -> NamedTemporaryFile:
	
	# load the raster, mask it by the polygon and crop it
	with rasterio.open(raster_file) as src:
		out_image, out_transform = mask(src, geojson.feature, crop=True)
		out_meta = src.meta.copy()

	# save the resulting raster  
	out_meta.update({"driver": "GTiff",
		"height": out_image.shape[1],
		"width": out_image.shape[2],
		"transform": out_transform})

	output_file = NamedTemporaryFile(suffix='.tif')
	with rasterio.open(output_file, "w", **out_meta) as dest:
		dest.write(out_image)

	return output_file
