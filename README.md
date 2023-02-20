## Urban Sprawl Calculation Service 
An API defintion and server to compute urban sprawl indicators. 

 # Urban Sprawl Metrics Calculator
The API defines a service that calculates [Urban Sprawl Metrics](https://gitlab.com/geometalab/usm_toolset/usm_calculator/). 

## API Explorer
See the [OpenAPI definition](api/sprawl-calculation-service.yaml) or the [rendered version](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/geodesignhub/urban-sprawl-calculation-service/master/api/sprawl-calculation-service.yaml)

### Process diagram
![WUP Calcluations](/api/images/sprawl-calculation-service.png)

## Deployment Instructions 

This toolset requires and uses `gdal` library it is recommended that you install externally. Following are the instructions: 
- Install gdal on Linux first via a command like `sudo apt-get install libgdal-dev`
- Install gdal libraries for Python. It is recommended that you use a environment like [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and use `conda install gdal` 
