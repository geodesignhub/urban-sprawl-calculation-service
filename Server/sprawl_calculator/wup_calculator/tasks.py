from celery import Celery
from wup_calculator.data_definitions import AlgorithmProcessingParameters
import json
from .sprawl_index_generator import generate_sprawl_indices
from dacite import from_dict
from sprawl_calculator.celery import app

@app.task(name="process_algorithm_async")
def process_algorithm_async(algorithm_parameters:str):
    '''
    The "processAlgorithm" method is a part of the QGIS Processing Framework 
    and it is used to perform some action for processing a raster and a vector layer.
    '''
    parameters = json.loads(algorithm_parameters)
    algorithm_parameters = from_dict(data_class= AlgorithmProcessingParameters, data= parameters)
    # 1.Get the downloaded file as input raster layer.
    generate_sprawl_indices(parameters= algorithm_parameters)
