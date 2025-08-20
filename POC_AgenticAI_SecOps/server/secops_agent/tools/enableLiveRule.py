from google.auth.transport.requests import Request
from typing import Mapping, Any
import requests
from google.oauth2 import service_account
import json
import os


def get_chronicle_credentials(environment):
    """Retrieves Chronicle API credentials from environment variable."""
    api_key = os.environ.get(environment)
    if not api_key:
        raise ValueError(
            f"{environment} environment variable not set. Please set your API key."
        )

    credential = service_account.Credentials.from_service_account_info(
        json.loads(api_key),
        scopes=['https://www.googleapis.com/auth/chronicle-backstory']
    )
    request = Request()
    credential.refresh(request)
    return credential


def enableLiveRule(
    credentials,
    rule_id: str,
) -> Mapping[str, Any]:
    """Enable Latest Version For A Rule.

    Args:
        credentials: Authorized session creds for HTTP requests.
        rule_id: Rule Id for the rule to update.

    Returns:
        Response 200

    Raises:
        requests.exceptions.HTTPError: HTTP request resulted in an error
            (response.status_code >= 400).
    """
    url = f"https://backstory.googleapis.com/v2/detect/rules/{rule_id}:enableLiveRule"
    params={"ruleId": rule_id}
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {credentials.token}"},
        params=params
    )

    if response.status_code >= 400:
        print(response.text)
    response.raise_for_status()

    return response.json()


def enable_live_rule_tool(environment: str = "default", rule_id: str = "") -> dict:
    """Enables the latest version of a specified Chronicle detection rule.

    Args:
        environment (str, optional): The environment from which to fetch credentials. Defaults to "default".
        rule_id (str): The ID of the rule to enable.

    Returns:
        dict: status indicating success or error, and details of the operation.
    """
    try:
        if not rule_id.strip():
            return {"status": "error", "error_message": "Rule ID cannot be empty."}

        credentials = get_chronicle_credentials(environment)
        result = enableLiveRule(credentials, rule_id)

        return {"status": "success", "result": result, "message": f"Latest version enabled for rule ID: {rule_id}"}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error_message": f"HTTP error enabling rule: {e}"}
    except ValueError as e:
        return {"status": "error", "error_message": str(e)}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {e}"}