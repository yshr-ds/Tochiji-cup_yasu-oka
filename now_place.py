import requests

class NOW_PLACE:
    def n_place(self):
        geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
        data = requests.get(geo_request_url).json()
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])

        # 東京駅の緯度経度に固定　
        latitude = 35.6809591
        longitude = 139.7673068

        latitude_1 = latitude + 0.0025
        latitude_2 = latitude - 0.0025
        longitude_1 = longitude + 0.0025
        longitude_2 = longitude - 0.0025

        return latitude_1, latitude_2, longitude_1, longitude_2