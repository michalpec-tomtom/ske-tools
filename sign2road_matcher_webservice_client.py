import json

import geojson
import requests

GET_MATCH_REQ = "api/v1/match"


class Sign2RoadMatcherWebserviceClient:

    def __init__(self, matcher_service_url: str):
        self.matcher_service_url = matcher_service_url
        if not self.matcher_service_url.endswith("/"):
            self.matcher_service_url = self.matcher_service_url + "/"

        self.get_match_req = self.matcher_service_url + GET_MATCH_REQ

    def get_match(self, traffic_sign_geojson: str, road_elements_geojson: str) -> requests.Response:
        payload = {"trafficSign": json.loads(traffic_sign_geojson), "roadElements": json.loads(road_elements_geojson)}
        print(payload)
        result = requests.post(self.get_match_req, json=payload)
        return result

