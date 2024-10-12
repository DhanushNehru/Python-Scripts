## Longitude and Latitude to Conical Converter

This script converts longitude and latitude to [Lambert conformal conic projection](https://en.wikipedia.org/wiki/Lambert_conformal_conic_projection).
The example used is for Mexico, under International Terrestrial Reference Frame 2008, which uses Lambert Conformal Conic projection 2SP (epsg:9802). 

This script is useful to combine census and geographic data, with traditional Longitude and Latitude from the more international frame of reference.

For more reference, see [National Geography institute explanatory PDF](https://www.inegi.org.mx/contenidos/temas/MapaDigital/Doc/asignar_sistema_coordenadas.pdf)
and [Pyproj, Lambert projections](https://proj.org/operations/projections/lcc.html).

## Prerequisites
- Python 3.x installed on your machine.

## Dependencies
The script requires the following Python libraries:
`pyproj`
`shapely`

You can install the required library using pip:
`pip install pyproj`
`pip install shapely`
