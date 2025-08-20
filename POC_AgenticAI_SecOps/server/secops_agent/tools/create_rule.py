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


def create_rule(
    credentials, rule_text: str
) -> Mapping[str, Any]:
    """Creates a new rule.

    Args:
        credentials: Authorized session creds for HTTP requests.
        rule_text: The content of the YARA-L 2.0 rule.

    Returns:
        New rule.

    Raises:
        requests.exceptions.HTTPError: HTTP request resulted in an error
          (response.status_code >= 400).
    """
    url = "https://backstory.googleapis.com/v2/detect/rules"
    body = {"ruleText": rule_text}

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {credentials.token}"},
        json=body
    )

    if response.status_code >= 400:
        print(response.text)
    response.raise_for_status()
    print(response.json())
    return response.json()


def create_rule_tool(environment: str = "default", rule_text: str = "") -> dict:
    """Creates a new detection rule in Chronicle.

    Args:
        environment (str, optional): The environment from which to fetch credentials.
        rule_text (str): The content of the YARA-L 2.0 rule to create.

    Returns:
        dict: status and result (created rule) or error message.
    """
    try:
        if not rule_text.strip():
            return {"status": "error", "error_message": "Rule text cannot be empty."}

        credentials = get_chronicle_credentials(environment)
        result = create_rule(credentials, rule_text)

        return {"status": "success", "rule": result}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error_message": f"HTTP error creating rule: {e}"}
    except ValueError as e:
        return {"status": "error", "error_message": str(e)}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {e}"}
