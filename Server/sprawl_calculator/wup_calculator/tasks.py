from celery import Celery
from wup_calculator.data_definitions import AlgorithmProcessingParameters
import json
from .sprawl_index_generator import generate_sprawl_indices

app = Celery('tasks', broker='redis://localhost:8000')

@app.task
def process_algorithm_async(algorithm_parameters:str):
    '''
    The "processAlgorithm" method is a part of the QGIS Processing Framework 
    and it is used to perform some action for processing a raster and a vector layer.
    '''
    parameters = json.loads(algorithm_parameters)
    algorithm_parameters = AlgorithmProcessingParameters.from_dict(parameters)
    # 1.Get the downloaded file as input raster layer.
    generate_sprawl_indices(parameters= algorithm_parameters)
