import geocoder
import numpy as np


# Вбиваешь почтовый индекс - получаешь широту и долготу
def postal_code_to_lat_lng(postal_code):
    g = geocoder.osm(postal_code)
    lat, lng = g.latlng
    return lat, lng

# Расстояние между координатами
def haversine(lat1, lng1, lat2, lng2):
    r = 6371
    phi1, lam1, phi2, lam2 = map(np.radians, (lat1, lng1, lat2, lng2))
    first_part = np.sin((phi2 - phi1) / 2) ** 2
    second_part = np.cos(phi1) * np.cos(phi2) * np.sin((lam2 - lam1) / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(first_part + second_part))

