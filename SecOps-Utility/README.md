# SecOps HealthCheck Utility - Feeds Report Generator

## What This Tool Does

This utility automatically generates reports about data feeds from Google SecOps.

## Overview

The tool creates an Excel file containing:
- Client names
- Feed names and types
- Feed status (active, error, etc.)
- Last feed initiation times
- Log types and source types
- Any error details if feeds are failing

## Prerequisites

Before running this tool, you need:

1. **Python 3.9 or higher** installed on your computer
2. **Service Account JSON files** for each client you want to check
   - These should be placed in a `service_accounts` folder
   - Each file should be named after the client (e.g., `client1.json`, `client2.json`)

## Installation

### Step 1: Create Virtual Environment

1. **Open Command Prompt/Terminal** in the project folder

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   
   **On Windows**:
   ```bash
   venv\Scripts\activate
   ```
   
   **On macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```

   You should see `(venv)` at the beginning of your command prompt when activated.

### Step 2: Install Dependencies

1. **With the virtual environment activated**, install required packages:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `google-auth` - For Google API authentication
   - `google-auth-oauthlib` - For OAuth authentication
   - `pandas` - For data processing
   - `openpyxl` - For Excel file creation

### Deactivating the Environment
When you're done working, deactivate the virtual environment:
```bash
deactivate
```

## Setup

1. **Create a `service_accounts` folder** in the same directory as the script
2. **Add your service account JSON files** to this folder
   - Each file should be named after the client (e.g., `acme_corp.json`)
   - The JSON files should have the necessary permissions for Chronicle API access

## How to Run

1. **Open Command Prompt/Terminal** in the project folder
2. **Activate the virtual environment** (if not already activated)
3. **Run the script**:
   ```bash
   python get_feeds_report.py
   ```

## What Happens When You Run It

1. The script looks for JSON files in the `service_accounts` folder
2. For each client, it connects to Google Chronicle API
3. Fetches information about all data feeds for that client
4. Combines all the data into a single Excel report
5. Saves the report as `feeds_YYYY-MM-DD.xlsx` in a `reports` folder

## Output

- **Location**: `reports/feeds_YYYY-MM-DD.xlsx`
- **Format**: Excel file with auto-sized columns
- **Content**: All feed information organized by client