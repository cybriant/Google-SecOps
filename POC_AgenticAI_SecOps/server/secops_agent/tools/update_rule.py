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


def update_rule(
    credentials,
    rule_id: str,
    rule_text: str,
) -> Mapping[str, Any]:
    """Updates an existing rule by creating a new version with the provided text.

    Args:
        credentials: Authorized session creds for HTTP requests.
        rule_id: Rule Id for the rule to update.
        rule_text: The new YARA-L 2.0 rule content.

    Returns:
        New version of the rule.

    Raises:
        requests.exceptions.HTTPError: HTTP request resulted in an error
            (response.status_code >= 400).
    """
    url = f"https://backstory.googleapis.com/v2/detect/rules/{rule_id}:createVersion"
    body = {"ruleText": rule_text}
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {credentials.token}"},
        json=body
    )

    if response.status_code >= 400:
        print(response.text)
    response.raise_for_status()

    return response.json()


def update_rule_tool(environment: str = "default", rule_id: str = "", rule_text: str = "") -> dict:
    """Updates an existing detection rule by creating a new version.

    Args:
        environment (str, optional): The environment from which to fetch credentials. Defaults to "default".
        rule_id (str): The ID of the rule to update.
        rule_text (str): The new YARA-L 2.0 rule content.

    Returns:
        dict: status and the new rule version details or an error message.
    """
    try:
        if not rule_id.strip():
            return {"status": "error", "error_message": "Rule ID cannot be empty."}
        if not rule_text.strip():
            return {"status": "error", "error_message": "New rule text cannot be empty."}

        credentials = get_chronicle_credentials(environment)
        result = update_rule(credentials, rule_id, rule_text)

        return {"status": "success", "updated_rule": result}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error_message": f"HTTP error updating rule: {e}"}
    except ValueError as e:
        return {"status": "error", "error_message": str(e)}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {e}"}