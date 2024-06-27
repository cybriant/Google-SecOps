from google.oauth2 import service_account
from googleapiclient import _auth
from google.auth.transport.requests import Request
import json
import requests


def upload_axonius_data(myLogger, credentials, entities, customer_id):
    """
    upload data to SecOps using Ingestion API.
    connect to SecOps using secret_key, parse Axonius data into UDM and upload the list of assets/entities to SecOps
    catch and report specific errors related to the process
    """
    try:
        if(customer_id == ""):
            print("No Customer ID Provided!")
            exit()
            
        # Define the Chronicle Ingestion API endpoint
        url = "https://malachiteingestion-pa.googleapis.com/v2/entities:batchCreate"

        payload = {
            "customer_id": customer_id,
            "log_type": "AXONIUS",
            "entities": entities,
        }

        # Convert payload to JSON
        payload_json = json.dumps(payload)

        # Make the POST request
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {credentials.token}"},
            data=payload_json,
        )
        print("Status Code: " + str(response.status_code))
        print("Response Content: \n" + str(response.content))
        print("Response Headers: \n" + str(response.headers))
        print("Response JSON: \n" + str(response.json()))

        # Check the response status
        if response.status_code == 200:
            myLogger.info(f"uploaded {len(entities)} assets")
            print("Successfully uploaded asset data.")
        else:
            print(f"Failed to upload asset data.")

    except Exception as e:
        print(f"Error uploading assets: {e}")
