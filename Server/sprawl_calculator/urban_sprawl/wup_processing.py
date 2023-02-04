import ctypes
import os
from typing import Tuple, Optional, Any
from sys import platform

import numpy
from osgeo import gdal

from qgis.core import (
    QgsProcessing,
    QgsProcessingFeedback,
    QgsFeature,
    QgsVectorLayer,
)

from .urban_sprawl.clip_raster.raster_clipper import RasterClipper, RasterClipperServer
from .urban_sprawl.common import constants
from .urban_sprawl.common.common import Common
from .urban_sprawl.common.weight import get_weighted_dis, get_weighted_ud
from .urban_sprawl.dis.dis_calculator import DisCalculator
from .urban_sprawl.lup.lup_calculator import LupCalculator
from .urban_sprawl.pba.pba_calculator import PbaCalculator
from .urban_sprawl.si.si_calculator import SiCalculator
from .urban_sprawl.wup.wup_calculator import WupCalculator
from .urban_sprawl.wspc.wspc_calculator import WspcCalculator


def calculate_and_save_wup_a(
    dis_value: float,
    feat: QgsFeature,
    lup_value: float,
    up_value: float,
    vector: QgsVectorLayer,
) -> float:
    wup_calculator = WupCalculator(up_value, dis_value, lup_value)
    wup_value = wup_calculator.calculate()
    wup_field_index = vector.fields().indexOf("Wup_a")
    vector.changeAttributeValue(
        fid=feat.id(), field=wup_field_index, newValue=float(wup_value)
    )
    return wup_value


def calculate_and_save_wup_b(
    feat: QgsFeature, parameters: Any, vector: QgsVectorLayer, wup_value: float,
) -> None:
    if (
        parameters[constants.SSA_FIELD]
        and feat[parameters[constants.SSA_FIELD]]
        and 1 >= round(float(feat[parameters[constants.SSA_FIELD]]), 5) >= 0
    ):
        wup_b_value = wup_value / (feat[parameters[constants.SSA_FIELD]])
        wup_b_field_index = vector.fields().indexOf("Wup_b")
        vector.changeAttributeValue(
            fid=feat.id(), field=wup_b_field_index, newValue=float(wup_b_value),
        )


def calculate_wup_a_and_b(
    dis_value: float,
    feat: QgsFeature,
    feedback: QgsProcessingFeedback,
    lup_value: float,
    parameters: Any,
    up_value: float,
    vector: QgsVectorLayer,
    resident_employee_count: int,
) -> None:
    if resident_employee_count > 0:
        wup_value = calculate_and_save_wup_a(
            dis_value, feat, lup_value, up_value, vector
        )

        calculate_and_save_wup_b(feat, parameters, vector, wup_value)

        calculate_and_save_wspc(feat, resident_employee_count, wup_value, vector)
    else:
        feedback.reportError(
            "Can't Calculate WUP as there is the number of residents or employees missing"
        )


def calculate_and_save_wspc(
    feat: QgsFeature,
    resident_employee_count: int,
    wup_value: float,
    vector: QgsVectorLayer,
) -> None:
    wspc_calculator = WspcCalculator(
        feat.geometry().area(), resident_employee_count, wup_value
    )
    wspc_value = wspc_calculator.calculate()
    wspc_field_index = vector.fields().indexOf("Wspc")
    vector.changeAttributeValue(
        fid=feat.id(), field=wspc_field_index, newValue=wspc_value
    )


def calculate_and_save_up(
    dis_value: float, feat: QgsFeature, pba_value: float, vector: QgsVectorLayer
) -> float:
    up_value = float(dis_value * pba_value)
    up_field_index = vector.fields().indexOf("Up")
    vector.changeAttributeValue(fid=feat.id(), field=up_field_index, newValue=up_value)
    return up_value


def calculate_and_save_pba(
    build_up_area: float, feat: QgsFeature, vector: QgsVectorLayer
) -> float:
    pba_calculator = PbaCalculator(build_up_area, float(feat.geometry().area()))
    pba_value = pba_calculator.calculate()
    pba_field_index = vector.fields().indexOf("Pba")
    vector.changeAttributeValue(
        fid=feat.id(), field=pba_field_index, newValue=pba_value
    )
    return pba_value


def calculate_and_save_wdis(
    dis_value: float, feat: QgsFeature, vector: QgsVectorLayer
) -> None:
    wdis_field_index = vector.fields().indexOf("Wdis")
    vector.changeAttributeValue(
        fid=feat.id(),
        field=wdis_field_index,
        newValue=float(get_weighted_dis(dis_value)),
    )


def calculate_and_save_ts(
    dis_value: float, build_up_area: float, feat: QgsFeature, vector: QgsVectorLayer
) -> None:
    ts_field_index = vector.fields().indexOf("Ts")
    vector.changeAttributeValue(
        fid=feat.id(), field=ts_field_index, newValue=float(dis_value * build_up_area),
    )


def calculate_and_save_settlement_area(
    build_up_area: float, feat: QgsFeature, vector: QgsVectorLayer
) -> None:
    settlement_area_field_index = vector.fields().indexOf("settlement_area")
    vector.changeAttributeValue(
        fid=feat.id(), field=settlement_area_field_index, newValue=float(build_up_area),
    )


def calculate_and_save_ud(
    lup_value: float, feat: QgsFeature, vector: QgsVectorLayer
) -> float:
    ud_value = (1 / lup_value) * 1000000

    ud_field_index = vector.fields().indexOf("Ud")
    vector.changeAttributeValue(
        fid=feat.id(), field=ud_field_index, newValue=float(ud_value)
    )
    return ud_value


def calculate_and_save_wud(
    ud_value: float, feat: QgsFeature, vector: QgsVectorLayer
) -> None:
    wud_field_index = vector.fields().indexOf("Wud")
    vector.changeAttributeValue(
        fid=feat.id(), field=wud_field_index, newValue=float(get_weighted_ud(ud_value)),
    )


def calculate_and_save_lup(
    feat: QgsFeature,
    feedback: QgsProcessingFeedback,
    parameters: Any,
    vector: QgsVectorLayer,
    build_up_area: float,
) -> Tuple[float, int]:
    resident_employee_count = LupCalculator.check_lup_input(feat, feedback, parameters,)

    lup_calculator = LupCalculator(build_up_area, resident_employee_count,)
    lup_value = float(lup_calculator.calculate())
    # Add Value to LUP field
    lup_field_index = vector.fields().indexOf("Lup")
    vector.changeAttributeValue(
        fid=feat.id(), field=lup_field_index, newValue=lup_value
    )

    return lup_value, resident_employee_count


def calculate_and_save_dis(
    feat: QgsFeature,
    feedback: QgsProcessingFeedback,
    result_matrix: numpy.ndarray,
    vector: QgsVectorLayer,
) -> float:
    dis_calculator = DisCalculator(result_matrix)
    dis_value = dis_calculator.calculate()
    if dis_value == -1:
        feedback.reportError("Unable to Properly calculate Si_Raster")
        return -1.0
    dis_field_index = vector.fields().indexOf("Dis")
    vector.changeAttributeValue(
        fid=feat.id(), field=dis_field_index, newValue=float(dis_value)
    )
    return dis_value


def save_raster(
    clipped_raster: gdal.Dataset,
    feat: QgsFeature,
    output_path: str,
    parameters: Any,
    result_matrix: numpy.ndarray,
) -> None:
    shape = Common.get_shape(result_matrix)
    feature_name = Common.get_clipped_raster_name(parameters, feat)
    path_output = get_output_path(parameters, output_path, feature_name + ".tif")
    driver = gdal.GetDriverByName("GTiff")
    si_raster = driver.Create(
        path_output,
        bands=1,
        xsize=shape.columns,
        ysize=shape.rows,
        eType=gdal.GDT_Float32,
    )
    si_raster.GetRasterBand(1).WriteArray(numpy.asarray(result_matrix))
    si_raster.SetGeoTransform(clipped_raster.GetGeoTransform())
    si_raster.SetProjection(clipped_raster.GetProjection())
    si_raster.FlushCache()

def get_si_raster(
    feat: QgsFeature,
    feedback: QgsProcessingFeedback,
    parameters: Any,
    pixel_size: float,
    raster: gdal.Dataset,
    si_lib: ctypes.CDLL,
    vector: QgsVectorLayer,
    output_path: str,
) -> Any:
    if parameters[constants.NAME_FIELD] and feat[parameters[constants.NAME_FIELD]]:
        feedback.pushInfo(
            "Calculating for: " + str(feat[parameters[constants.NAME_FIELD]])
        )
    clipped_raster_path = RasterClipper.get_clipped_raster_path(
        feat, parameters, vector, constants.RASTER
    )
    clipped_raster = gdal.Open(clipped_raster_path)
    if clipped_raster:
        clipped_matrix = Common.get_matrix(clipped_raster)
        si_calculator = SiCalculator(raster, clipped_matrix, 2000)
        x_index, y_index = RasterClipper.get_x_y_offset(
            raster, clipped_raster, pixel_size
        )
        result_matrix = si_calculator.calculate(si_lib, x_index, y_index)
        save_raster(clipped_raster, feat, output_path, parameters, result_matrix)
        return clipped_matrix, clipped_raster, result_matrix
    else:
        feedback.reportError(
            "Invalid Geometry for " + str(feat[parameters[constants.NAME_FIELD]])
        )
        return None, None, None


def get_si_raster_server(
    pixel_size: float,
    raster: gdal.Dataset,
    clipped_raster_path:str,
    si_lib: ctypes.CDLL,
) -> Any:
    
    clipped_raster = gdal.Open(clipped_raster_path)
    if clipped_raster:
        clipped_matrix = Common.get_matrix(clipped_raster)
        si_calculator = SiCalculator(raster, clipped_matrix, 2000)
        x_index, y_index = RasterClipperServer.get_x_y_offset(
            raster, clipped_raster, pixel_size
        )
        result_matrix = si_calculator.calculate(si_lib, x_index, y_index)
        
        return clipped_matrix, clipped_raster, result_matrix
    else:
        print(
            "Invalid Geometry provided"
        )
        return None, None, None


def get_si_lib() -> Optional[ctypes.CDLL]:
    dll_path = os.path.dirname(os.path.realpath(__file__))

    si_lib = None

    if platform in ("linux", "linux2"):
        si_lib = ctypes.CDLL(os.path.join(dll_path, "QGis_Plugin_SO.so"))
    elif platform == "darwin":
        si_lib = ctypes.CDLL(os.path.join(dll_path, "QGis_Plugin_DYLIB.dylib"))
    elif platform == "win32":
        si_lib = ctypes.CDLL(os.path.join(dll_path, "QGis_Plugin_DLL.dll"))

    return si_lib


def get_output_path(parameters: Any, output_path: str, file: str) -> str:
    if parameters[constants.OUTPUT] == QgsProcessing.TEMPORARY_OUTPUT:
        output_path = output_path + file
    else:
        output_path = os.path.join(output_path, file)

    return output_path


def calculate(
    feat: QgsFeature,
    vector: QgsVectorLayer,
    build_up_area: float,
    dis_value: float,
    feedback: QgsProcessingFeedback,
    parameters: Any,
) -> None:
    calculate_and_save_settlement_area(build_up_area, feat, vector)

    calculate_and_save_ts(dis_value, build_up_area, feat, vector)

    # Calculate LUP Value
    (lup_value, resident_employee_count,) = calculate_and_save_lup(
        feat, feedback, parameters, vector, build_up_area
    )

    ud_value = calculate_and_save_ud(lup_value, feat, vector)

    calculate_and_save_wud(ud_value, feat, vector)

    pba_value = calculate_and_save_pba(build_up_area, feat, vector)

    up_value = calculate_and_save_up(dis_value, feat, pba_value, vector)

    calculate_wup_a_and_b(
        dis_value,
        feat,
        feedback,
        lup_value,
        parameters,
        up_value,
        vector,
        resident_employee_count,
    )
