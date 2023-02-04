from typing import Tuple, Any

from osgeo import gdal
from PyQt5.QtCore import QVariant

from qgis import processing
from qgis.core import (
    QgsProcessingContext,
    QgsFeature,
    QgsVectorLayer,
    QgsProcessing,
    QgsProcessingUtils,
    QgsField,
    QgsProcessingFeatureSourceDefinition,
    QgsMapLayer,
)

from ...urban_sprawl.common.common import Common


class RasterClipperServer:
    @staticmethod
    def get_x_y_offset(
        raster: gdal.Dataset, clipped_raster: gdal.Dataset, pixel_size: float,
    ) -> Tuple[int, int]:
        raster_geo_transform = Common.get_geo_transform(raster)
        clipped_geo_transform = Common.get_geo_transform(clipped_raster)

        x_index = int(
            (raster_geo_transform.position_y - clipped_geo_transform.position_y)
            / pixel_size
        )
        y_index = int(
            (clipped_geo_transform.position_x - raster_geo_transform.position_x)
            / pixel_size
        )

        return x_index, y_index

class RasterClipper:
    @staticmethod
    def get_x_y_offset(
        raster: gdal.Dataset, clipped_raster: gdal.Dataset, pixel_size: float,
    ) -> Tuple[int, int]:
        raster_geo_transform = Common.get_geo_transform(raster)
        clipped_geo_transform = Common.get_geo_transform(clipped_raster)

        x_index = int(
            (raster_geo_transform.position_y - clipped_geo_transform.position_y)
            / pixel_size
        )
        y_index = int(
            (clipped_geo_transform.position_x - raster_geo_transform.position_x)
            / pixel_size
        )

        return x_index, y_index

    @staticmethod
    def get_clipped_raster_path(
        feature: QgsFeature, parameters: Any, vector: QgsVectorLayer, raster_name: str,
    ) -> str:
        vector.removeSelection()
        vector.select(feature.id())

        clipped_raster_path = processing.run(
            "gdal:cliprasterbymasklayer",
            {
                "INPUT": parameters[raster_name],
                "MASK": QgsProcessingFeatureSourceDefinition(vector.id(), True),
                "NODATA": 0,
                "CROP_TO_CUTLINE": True,
                "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
            },
        )["OUTPUT"]

        vector.removeSelection()

        return str(clipped_raster_path)

    @staticmethod
    def create_fields(vector: QgsVectorLayer) -> None:
        layer_provider = vector.dataProvider()

        wdis_index = vector.fields().indexOf("Wdis")
        if wdis_index == -1:
            layer_provider.addAttributes([QgsField("Wdis", QVariant.Double)])

        lup_index = vector.fields().indexOf("Lup")
        if lup_index == -1:
            layer_provider.addAttributes([QgsField("Lup", QVariant.Double)])

        pba_index = vector.fields().indexOf("Pba")
        if pba_index == -1:
            layer_provider.addAttributes([QgsField("Pba", QVariant.Double)])

        up_index = vector.fields().indexOf("Up")
        if up_index == -1:
            layer_provider.addAttributes([QgsField("Up", QVariant.Double)])

        ud_index = vector.fields().indexOf("Ud")
        if ud_index == -1:
            layer_provider.addAttributes([QgsField("Ud", QVariant.Double)])

        w_ud_index = vector.fields().indexOf("Wud")
        if w_ud_index == -1:
            layer_provider.addAttributes([QgsField("Wud", QVariant.Double)])

        ts_index = vector.fields().indexOf("Ts")
        if ts_index == -1:
            layer_provider.addAttributes([QgsField("Ts", QVariant.Double)])

        wup_index = vector.fields().indexOf("Wup_a")
        if wup_index == -1:
            layer_provider.addAttributes([QgsField("Wup_a", QVariant.Double)])

        wup_b_index = vector.fields().indexOf("Wup_b")
        if wup_b_index == -1:
            layer_provider.addAttributes([QgsField("Wup_b", QVariant.Double)])

        wspc_index = vector.fields().indexOf("Wspc")
        if wspc_index == -1:
            layer_provider.addAttributes([QgsField("Wspc", QVariant.Double)])

    @staticmethod
    def get_vectorlayer_of_feature(
        context: QgsProcessingContext, vector: QgsVectorLayer,
    ) -> QgsMapLayer:
        alg_params = {
            "INPUT": vector,
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        temp_layer = processing.run(
            "native:saveselectedfeatures",
            alg_params,
            context=context,
            is_child_algorithm=True,
        )["OUTPUT"]
        polygon_layer = QgsProcessingUtils.mapLayerFromString(temp_layer, context)
        return polygon_layer

    @staticmethod
    def copy_vector_layer(
        context: QgsProcessingContext, vector: QgsVectorLayer
    ) -> QgsVectorLayer:
        vector.removeSelection()
        vector.selectAll()
        vector = RasterClipper.get_vectorlayer_of_feature(context, vector)
        vector.setName("WUP_Result_Layer")
        vector.removeSelection()
        return vector
