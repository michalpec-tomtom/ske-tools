from s2r_datatypes.traffic_sign import TrafficSign

import json
import geojson
from geojson import Feature, Point, FeatureCollection
import requests
import os

from s2r_datatypes.traffic_sign_serialization import traffic_sign_collection_to_feature_collection, write_geojson_to_string

OUTPUT_DIR = "C:\DataD\REKS_689_Incorrect_matches_ndl\output_single"
# SKE_SERVICE_URL = "http://knowledge-base-read-service-main-2022-06-06.dev.ref-platform-dev.ad.az.tt3.com/collections/knowledge/items/"
SKE_SERVICE_URL = "http://knowledge-base-read-service.api.dev.ref-platform-dev.ad.az.tt3.com/collections/knowledge/items/"

ROADNETWORK_SERVICE_URL = 'http://roadnetwork-service.sign2road.ref-platform-dev.ad.az.tt3.com:8080/sign2road-roadnetwork-provider-service/api/v1/roadelements/dseg'
OUTPUT_SKE = os.path.join(OUTPUT_DIR, "ske")
OUTPUT_TS = os.path.join(OUTPUT_DIR, "ts")
OUTPUT_RE = os.path.join(OUTPUT_DIR, "re")


def get_road_network(lon, lat, buffer):
    request_url = f'{ROADNETWORK_SERVICE_URL}/{lat}/{lon}/{buffer}'
    r = requests.get(request_url)
    return r.text

def get_ske(id: str):
    url = SKE_SERVICE_URL + id
    r = requests.get(url)
    return r.text


def ske_data_from_string(ske_str: str):
    data = json.loads(ske_str)
    geometry = data['geometry']
    sign2road = data['properties']['associations']['sign2road'][0]

def map_ske_to_traffic_sign_primitive(ske_dict: dict) -> TrafficSign:
    """Maps Sign Knowledge Elements (SKEs) to Traffic Sign Primitives (see https://confluence.tomtomgroup.com/x/8iXIOg)
    format.

    Args:
        ske_dict: a dictionary containing SKE information

    Returns:
        dict: Traffic sign primitive in GeoJson FeatureCollection format.
    """
    # assert "sign_knowledge_element_id" in ske_dict
    # assert "category" in ske_dict
    # assert "longitude" in ske_dict
    # assert "latitude" in ske_dict

    heading = None
    if "heading" in ske_dict["properties"]["attributes"]:
        if ske_dict["properties"]["attributes"]["heading"] is not None:
            heading = ske_dict["properties"]["attributes"]["heading"]["value"]


    traffic_sign = TrafficSign(
        feature_id=ske_dict["id"],
        source="SKE",
        category=ske_dict["properties"]["attributes"]["category"][0]["category"],
        position_lon=ske_dict["properties"]["attributes"]["position"]["longitude"],
        position_lat=ske_dict["properties"]["attributes"]["position"]["latitude"],
        heading=heading,
        position_z=ske_dict["properties"]["attributes"]["position"]["altitude"] if "altitude" in ske_dict["properties"]["attributes"]["position"] else None,
        value=ske_dict["properties"]["attributes"]["category"]["value"] if "value" in ske_dict["properties"]["attributes"]["category"] else None,
        knowledge_version= None,
        # Note: Name of car_position_lon, car_position_lat, car_position_lat will probably change once provided.
        car_position_lon=None,
        car_position_lat=None,
        car_heading=None)
    return traffic_sign


if __name__ == '__main__':
    try:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        if not os.path.exists(OUTPUT_SKE):
            os.makedirs(OUTPUT_SKE)
        if not os.path.exists(OUTPUT_TS):
            os.makedirs(OUTPUT_TS)
        if not os.path.exists(OUTPUT_RE):
            os.makedirs(OUTPUT_RE)

    except Exception as e:
        print("Could not create output dir " + e)
        exit(1)
    ids = (['fd44e15b-3c99-4c65-abf6-e726dea8f8ff'])


    # ids = ('00004e4c-3100-2800-0000-000014ebfe28',
    #        '00004e4c-3200-2800-0000-000015753b21',
    #        '93151271-ceb1-48bf-80fd-a6de9b47a416',
    #        '9c40d0f2-a71f-4d50-b2cb-7d7cf85ad49c',
    #        'aa55f591-0a5d-41de-aa7e-561eb76d3553',
    #        'aec29dfd-3a82-4f1a-9db9-d7f1503989e9',
    #        'c8ac5dcb-0c36-4b79-9cf1-f4c433d872fe',
    #        'f12095af-9989-4d62-bf1e-34d6c080656e',
    #        '00413d0f-93f3-4e82-8e22-739ed1d12999',
    #        '00aa84fe-f079-48b4-8396-0b3595d418f7',
    #        '014564c6-decc-4a9d-9507-48c55d948ad8',
    #        '014e2b48-6a76-41cd-82e5-cb75089876d6',
    #        '014e80d6-6949-449e-baef-27afc7c4e039',
    #        '01c54aa8-d55f-487d-9857-12aa943f65dd',
    #        '020ca282-5b24-40d3-8765-a8afa12c04a9',
    #        '0472fd54-828a-49a1-98ae-2437cbe02572',
    #        '05b07f9d-41e9-426d-a0bc-38061a1b7b40',
    #        '098169b4-652f-460d-98a2-3b5d9403e042',
    #        '0a59b3c9-a526-4055-83e1-cdec202a0591',
    #        '146d7367-2a6f-4fda-8daf-51bab95d3bfe',
    #        '14873adf-f43f-4879-bf63-6f488d342610',
    #        '00004e4c-3100-2800-0000-000014ec82ed',
    #        '00004e4c-3200-2800-0000-000015754515',
    #        '8d0057f6-5866-44be-9f74-e2013b50836c',
    #        '8e45a1d6-5782-4866-b327-eb0d1905f8e8',
    #        '9df7e12c-679c-42ba-bf85-d254af034cd3',
    #        '9f038d69-6006-42e8-b7a6-aff721b6adfc',
    #        'a5cd37b3-6a55-4d0d-94a4-b5b6a8ae6c4c',
    #        'a6a264cf-3474-4d5f-940c-80cc8774142b',
    #        'b127d930-7e21-4131-b87d-f42bc4d9bdb6',
    #        'b14837fd-a1c3-4fce-bec1-5a432fc1cb46',
    #        'b27cdf0d-68a5-4d48-989c-1365a3e94a4b',
    #        'bda0d0be-9c5f-46e1-b7b0-bea330e27f92',
    #        'd0cb365b-a98d-4c5c-9b74-6afc8cb97197',
    #        'd2bc869f-65fe-4815-8c71-f549138aa663',
    #        'f822ca6a-f910-45e4-b1fb-104e2998b926',
    #        '8bd1bb50-8263-444c-9fb2-a0b4b1952794',
    #        '9ca33582-2961-463b-a98e-b9a51ed1b4ed',
    #        'ad8a6f0e-3469-44d8-987e-7e67c3c3b45c',
    #        '00747516-c24a-465b-9eab-39c0dbdbeca6',
    #        '020e1adb-872f-43d6-b006-c17f7bd0501a',
    #        '00320828-2cd9-4bcf-877e-dc52aaba719d',
    #        '00e65c3e-66bf-4479-a415-5e13853dcf86',
    #        '01321d6e-4ce6-42d9-bdbf-d11364d017e4',
    #        '0152f15f-87a1-4ea9-8a2d-b2770b41a435',
    #        '0157c97d-11b8-4d13-bfdb-63253d8700c0',
    #        '01f79a0b-0eaf-4152-953a-fc2846432b4b',
    #        '02b701b3-71ce-4e4d-a385-9e2d83b4ba71',
    #        '03bd6f70-e40c-4162-b787-67c1060be46f',
    #        '05056516-5150-499f-9c64-31bc1dc45ce9',
    #        '051350b6-9f6e-4a0a-998f-b4fe55d3a606',
    #        '08c422e9-b4d1-4a59-afe4-09d836d4f478',
    #        '14a5f3f9-01a6-49b6-8be0-55abcd870ca9',
    #        '14bcf58c-2417-49bf-9bb7-25970eb9e58e',
    #        '14cc0730-8f78-4c1a-a9de-aa32c7ff320b',
    #        '85d8e298-798d-4e4c-8941-ae413d2c9ce9'
    #        )

    feature_list = []
    for id in ids:
        ske = get_ske(id)
        feature = geojson.loads(ske)
        traffic_sign = map_ske_to_traffic_sign_primitive(feature)
        ts_fc = traffic_sign_collection_to_feature_collection([traffic_sign])

        feature_list.append(feature)
        ske_data_from_string(ske)
        id_based_name = id + ".geojson"
        with open(os.path.join(OUTPUT_SKE, id_based_name), "wt") as output:
            output.write(ske)
        with open(os.path.join(OUTPUT_TS, id_based_name), "wt") as output:
            tss = write_geojson_to_string(ts_fc)
            output.write(tss)

        o = get_road_network(traffic_sign.position_lon, traffic_sign.position_lat, 100)
        with open(os.path.join(OUTPUT_RE, id_based_name), "wt") as output:
            output.write(o)
        a = 5


    feature_collection = FeatureCollection(feature_list)
    s = geojson.dumps(feature_collection)
    with open(os.path.join(OUTPUT_DIR, 'selected_ske3.geojson'), "wt") as output:
        output.write(s)
    a = 6;



