from pyproj import Proj
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Definition of lambert conical projection.
lambert = {'proj': 'lcc', # Lambert Conformal Conic 2SP (epsg:9802)
     'ellps': 'GRS80', #'epsg:7019', #'epsg:9802', # 'epsg:6651',
     'lon_0': -102.00000000,
     'lat_0': 12.00000000, # 12° 00’ 0.0’’ N
     'lat_1': 17.50000000, # 17° 30’ 0.00’’ N
     'lat_2': 29.50000000, # 29° 30’ 0.00’’ N
     'x_0': 2500000,
     'y_0': 0}

prj = Proj(lambert) 

# Coordinates for the city of Monterrey, Nuevo León, México

city = {'c_name': 'Monterrey', 'lon': -100.316116, 'lat': 25.686613}

x, y = prj(city['lon'], city['lat']) 

print('                     X                 Y')
print(city['c_name'], ':  lon:', city['lon'], '      , lat:', city['lat'])
print('Lambert function:', x, ',', y)
print('   Should return: 2668223.843       , 1516271.922') 

# Should return:

"""
                     X                 Y
Monterrey :  lon: -100.316116       , lat: 25.686613
Lambert function: 2668223.842598227 , 1516271.9216458194
   Should return: 2668223.843       , 1516271.922
"""
