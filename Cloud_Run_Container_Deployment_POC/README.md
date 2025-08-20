# GCP Container Deployment Boilerplate

A simple, reusable template for deploying Python containers to Google Cloud Platform using Cloud Build and Cloud Run Jobs.

## Quick Start Guide

### Step 1: Create GitHub Repository
1. **Create a new repository** from this template:
   - Click "Use this template" on GitHub
   - Name your repository (e.g., `my-gcp-container`)
   - Choose public or private
   - Click "Create repository from template"

### Step 2: Clone and Setup Local Environment
```bash
# Clone your new repository
git clone https://github.com/yourusername/my-gcp-container.git
cd my-gcp-container

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\scripts\activate
```

### Step 3: Customize Your Application
1. **Update the main function** in `main.py`:
   ```python
   def do_work():
       # Replace this with your actual workload
       # Example: API calls, data processing, file operations, etc.
       return "Your custom work completed successfully"
   ```

2. **Create local environment file** (optional):
   ```bash
   # Create .env file for local development
   echo "PROJECT_ID=your-gcp-project-id" > .env
   echo "REGION=us-central1" >> .env
   echo "SECRET_NAMES=my-secret-1,my-secret-2" >> .env
   ```

### Step 4: Setup GCP Artifact Registry
1. **Go to GCP Console** → **Artifact Registry**
2. **Create a new repository**:
   - Click "Create Repository"
   - Name: `my-container-repo`
   - Format: `Docker`
   - Location: `us-central1` (or your preferred region)
   - Click "Create"

3. **Update `cloudbuild.yaml`** with your repository details:
   ```yaml
   # Replace these values in cloudbuild.yaml:
   - 'us-central1-docker.pkg.dev/YOUR_PROJECT_ID/my-container-repo/my-app:latest'
   ```

### Step 5: Update Dependencies
1. **Edit `requirements.txt`** to include your project dependencies:
   ```txt
   google-cloud-secret-manager
   python-dotenv
   # Add your specific dependencies here:
   # requests
   # pandas
   # google-cloud-bigquery
   ```

### Step 6: Commit and Push
```bash
# Add your changes
git add .

# Commit with descriptive message
git commit -m "feat: initial container setup with custom workload"

# Push to GitHub
git push origin main
```

### Step 7: Setup Cloud Build Trigger
1. **Go to GCP Console** → **Cloud Build** → **Triggers**
2. **Create a new trigger**:
   - Name: `my-container-trigger`
   - Event: `Push to a branch`
   - Repository: Connect your GitHub repository
   - Branch: `main`
   - Build configuration: `Cloud Build configuration file (yaml)`
   - Cloud Build configuration file location: `cloudbuild.yaml`
   - Click "Create"

### Step 8: Deploy to Cloud Run Jobs
1. **Go to GCP Console** → **Cloud Run** → **Jobs**
2. **Click "Create Job"**
3. **Configure the job**:
   - Job name: `my-container-job`
   - Region: `us-central1` (same as your Artifact Registry)
   - Click "Next"

4. **Select container image**:
   - Click "Select" next to Container image URL
   - Choose your repository: `my-container-repo`
   - Select the latest image
   - **Important**: Replace the full image URL with `:latest` tag
   
   **Example transformation:**
   ```
   From: us-central1-docker.pkg.dev/project-id/my-container-repo/my-app@sha256:abc123...
   To:   us-central1-docker.pkg.dev/project-id/my-container-repo/my-app:latest
   ```

5. **Set environment variables**:
   ```
   PROJECT_ID=your-gcp-project-id
   REGION=us-central1
   SECRET_NAMES=my-secret-1,my-secret-2
   LOG_LEVEL=INFO
   ```

6. **Configure execution**:
   - CPU allocation: `1`
   - Memory allocation: `512 MiB`
   - Timeout: `3600` (1 hour)
   - Retries: `3`

7. **Click "Create Job"**

### Step 9: Execute Your Job
1. **In Cloud Run Jobs**, find your job and click "Execute"
2. **Monitor execution** in the logs
3. **Verify results** in your application logs



