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
            myLogger.critical("No Customer ID Provided!")
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
        # myLogger.info("Status Code: " + str(response.status_code))
        # myLogger.info("Response Content: \n" + str(response.content))
        myLogger.info("Response Headers: \n" + str(response.headers))
        # myLogger.info("Response JSON: \n" + str(response.json()))

        # Check the response status
        if response.status_code == 200:
            myLogger.info(f"Uploaded {len(entities)} assets")
        else:
            myLogger.critical(f"Failed to upload asset data.")
            myLogger.critical("Response JSON: \n" + str(response.json()))

    except Exception as e:
        myLogger.critical(f"Error uploading assets: {e}")
