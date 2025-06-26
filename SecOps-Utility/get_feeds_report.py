import json
import requests
import pandas as pd
import os
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2 import service_account

def get_chronicle_credentials(service_account_json):
    """Retrieves Chronicle API credentials from service account JSON."""
    credential = service_account.Credentials.from_service_account_info(
        service_account_json,
        scopes=['https://www.googleapis.com/auth/chronicle-backstory']
    )
    request = Request()
    credential.refresh(request)
    return credential

def list_feeds_tool(service_account_json: dict) -> dict:
    """
    Fetches the list of feeds from Chronicle API.
    Args:
        service_account_json (dict): The service account JSON as dictionary.
    Returns:
        dict: status and feeds or error message.
    """
    try:
        credentials = get_chronicle_credentials(service_account_json)
        headers = {"Authorization": f"Bearer {credentials.token}"}
        url = 'https://backstory.googleapis.com/v1/feeds'
        response = requests.get(url, headers=headers)
        if not response.ok:
            return {
                "status": "error",
                "error_message": f"Failed to fetch feeds: {response.text}"
            }
        feeds_data = response.json()
        return {
            "status": "success",
            "feeds": feeds_data
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def main():
    # Get current date for filename
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    service_accounts_dir = os.path.join(script_dir, "service_accounts")
    reports_dir = os.path.join(script_dir, "reports")
    
    # Create reports directory if it doesn't exist
    os.makedirs(reports_dir, exist_ok=True)
    
    # Check if service_accounts directory exists
    if not os.path.exists(service_accounts_dir):
        print(f"Error: Service accounts directory not found at {service_accounts_dir}")
        return
    
    # Get all JSON files from service_accounts directory
    json_files = [f for f in os.listdir(service_accounts_dir) if f.endswith('.json')]
    
    if not json_files:
        print("No JSON files found in service_accounts directory")
        return
    
    all_feeds = []
    
    # Process each service account
    for json_file in json_files:
        client_name = os.path.splitext(json_file)[0]  # Remove .json extension
        file_path = os.path.join(service_accounts_dir, json_file)
        
        print(f"Processing {client_name}...")
        
        try:
            # Read service account JSON
            with open(file_path, 'r') as f:
                service_account_json = json.load(f)
            
            # Get feeds data
            result = list_feeds_tool(service_account_json)
            
            if result["status"] == "success":
                feeds = result["feeds"].get("feeds", [])
                for feed in feeds:
                    details = feed.get("details", {})
                    feed["feedSourceType"] = details.get("feedSourceType", "")
                    feed["logType"] = details.get("logType", "")
                    feed["client_name"] = client_name  # Add client name from filename
                all_feeds.extend(feeds)
                print(f"  ✓ Successfully fetched {len(feeds)} feeds")
            else:
                print(f"  ✗ Error: {result.get('error_message', 'Unknown error')}")
                # Add error entry to track failed clients
                all_feeds.append({
                    "client_name": client_name,
                    "name": "ERROR",
                    "logType": "",
                    "displayName": "",
                    "feedState": "ERROR",
                    "feedSourceType": "",
                    "lastFeedInitiationTime": "",
                    "details": "",
                    "failureDetails": result.get("error_message", "Unknown error")
                })
                
        except Exception as e:
            print(f"  ✗ Error processing {client_name}: {str(e)}")
            # Add error entry
            all_feeds.append({
                "client_name": client_name,
                "name": "ERROR",
                "logType": "",
                "displayName": "",
                "feedState": "ERROR",
                "feedSourceType": "",
                "lastFeedInitiationTime": "",
                "details": "",
                "failureDetails": str(e)
            })
    
    # Create DataFrame and save to Excel
    if all_feeds:
        # Define columns to display
        columns_to_display = ["client_name", "name", "logType", "displayName", "feedState", "feedSourceType", "lastFeedInitiationTime", "details", "failureDetails"]
        
        # Create DataFrame with only specified columns
        df = pd.DataFrame([{col: feed.get(col, "") for col in columns_to_display} for feed in all_feeds])
        
        # Save to Excel
        excel_filename = f"feeds_{current_date}.xlsx"
        excel_path = os.path.join(reports_dir, excel_filename)
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Feeds Report', index=False)
            
            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Feeds Report']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"\n✓ Report saved to: {excel_path}")
        print(f"  Total feeds processed: {len(all_feeds)}")
        print(f"  Clients processed: {len(json_files)}")
    else:
        print("No feeds data to save")

if __name__ == "__main__":
    main()

