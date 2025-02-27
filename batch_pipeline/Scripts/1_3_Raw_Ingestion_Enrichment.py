
import requests
import json
from google.cloud import storage

def fetch_ipma_data():
    url = "https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")
    
def ipma_filter(response):
    stationid = "1200535"
    timestamps = list(response.keys())

    result_list = []

    for timestamp in timestamps:
        filtered_data = response[timestamp][stationid]
        filtered_data["timestamp"] = timestamp
        filtered_data["location"] = "Lisboa"

        result_list.append(filtered_data)

    return result_list

def upload_to_gcs(data, bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    json_data = json.dumps(data, indent=2)
    blob.upload_from_string(json_data, content_type='application/json')
    
    print(f"File uploaded to {blob_name} in bucket {bucket_name}")



def main():
    try:
        ipma_data = fetch_ipma_data()
        filtered_data = ipma_filter(ipma_data)
        
        bucket_name = "edit-data-eng-project-group1"
        blob_name = "LandingZone/Enrichment/ipma_lisbon_data.json"
        
        upload_to_gcs(filtered_data, bucket_name, blob_name)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
