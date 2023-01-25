import rasterio
from rasterio.mask import mask


def clip_raster_with_geojson(raster_file, geojson):
	# load the raster, mask it by the polygon and crop it
	with rasterio.open(raster_file) as src:
		out_image, out_transform = mask(src, geojson, crop=True)
		out_meta = src.meta.copy()

	# save the resulting raster  
	out_meta.update({"driver": "GTiff",
		"height": out_image.shape[1],
	    "width": out_image.shape[2],
	    "transform": out_transform})

	with rasterio.open(raster_file, "w", **out_meta) as dest:
	    dest.write(out_image)

	return out_image, out_transform

