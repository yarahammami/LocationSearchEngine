import json
import boto3
from algoliasearch.search_client import SearchClient

algolia_client = SearchClient.create("ZLYFD8VG8C", "c82aa53030c57199a0f750626533080c")
index = algolia_client.init_index("dev_test")

client = boto3.client('location')

def lambda_handler(event, context):
    print(event)
    for i in event['Records']:
        if i['eventName'] == 'INSERT':
            location_id = i['dynamodb']['NewImage']['locationId']['S']
            name = i['dynamodb']['NewImage']['name']['S']
            line1 = i['dynamodb']['NewImage']['line1']['S']
            line2 = i['dynamodb']['NewImage']['line2']['S']
            city = i['dynamodb']['NewImage']['city']['S']
            state = i['dynamodb']['NewImage']['state']['S']
            country = i['dynamodb']['NewImage']['country']['S']
            zipCode = i['dynamodb']['NewImage']['zipCode']['S']

            complete_address = location_id+', '+name+', '+line1+', '+line2+', '+city+', '+state+', '+zipCode
            print("Complete Address : {}".format(complete_address))

            record = {"objectId": location_id,
                      "name": name,
                      "line1": line1,
                      "line2": line2,
                      "city": city,
                      "state": state,
                      "country": country,
                      "zipCode": zipCode}

            response = client.search_place_index_for_text(IndexName='place_index1',
                                                          FilterCountries=["LB"],
                                                          MaxResults=1,
                                                          Text=complete_address)
            location_response = response['Results'][0]['Place']['Geometry']['Point']
            record['_geoloc'] = {
                "lat": location_response[1],
                "lng": location_response[0]
            }
            print(record)

            index.save_object(record).wait()


        elif i['eventName']=='REMOVE':
            location_id = i['dynamodb']['OldImage']['locationId']['S']
            print("Deleting the location ID : {}".format(location_id))
            index.delete_objects([location_id])











