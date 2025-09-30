import requests

BASE_API = "https://data.gov.sg/api/action/datastore_search"

def fetch_dataset(resource_id, limit=100, offset=0):
    params = {
        "resource_id": resource_id,
        "limit": limit,
        "offset": offset,
    }
    resp = requests.get(BASE_API, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", {})



def fetch_all_records(resource_id, chunk_size=1000):
    offset = 0
    all_records = []
    while True:
        result = fetch_dataset(resource_id, limit=chunk_size, offset=offset)
        records = result.get("records", [])
        all_records.extend(records) 

        if len(records) < chunk_size:
            break
        offset += chunk_size
    return all_records
   
