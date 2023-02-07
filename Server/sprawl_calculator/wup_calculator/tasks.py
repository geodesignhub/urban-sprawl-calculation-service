from celery import Celery

app = Celery('tasks', broker='redis://localhost:8000')

@app.tasks
def process_algorithm_async(url:str, geojson:GeoJSONFeature):
    return processAlgorithm(url, geojson)