import json
import boto3
from algoliasearch.search_client import SearchClient

algolia_client = SearchClient.create("ZLYFD8VG8C", "c82aa53030c57199a0f750626533080c")
index = algolia_client.init_index("dev_test")
client = boto3.client('location')


def lambda_handler(event, context):
    complete_address = json.loads(event['body'])['complete_address']
    print("complete Address : {}".format(complete_address))

    response = client.search_place_index_for_text(IndexName ='placetest',
                                                  FilterCountries=["LBN"],
                                                  MaxResults=1,
                                                  Text=complete_address)

    longi, lat = response["Results"][0]['Place']['Geometry']['Point']

    results = index.search('', {
        'aroundLatLng': '{}, {}'.format(lat, longi),
        'aroundRadius': 100000
    })

    return results