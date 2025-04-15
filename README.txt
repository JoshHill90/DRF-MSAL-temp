# Django Backend API with Microsoft OAuth Integration

This is a Django-based backend API template designed to handle authentication via Microsoft OAuth and securely serve MS Graph API requests. It is built to integrate with a separate frontend application while keeping all sensitive Microsoft credentials on the backend.

---

## 🔧 Project Setup

### 1. Clone the Repository and Create a Virtual Environment

git clone <your-repo-url>  
cd <repo-folder>  
python -m venv apiVM

### 2. Activate the Virtual Environment

**Windows:**  
.\apiVM\Scripts\activate

**macOS/Linux:**  
source apiVM/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Initialize Django Secret Key

Start a Python shell:

python

Then run:

from django.core.management.utils import get_random_secret_key  
print(get_random_secret_key())

Copy the generated key and use it in your environment configuration as shown below.

---

## 🔐 Environment Configuration

All environment variables should be stored in a `.env` file inside the `utils/env/` directory.

Use the format below. Replace `"INITAL"` with your project or site initials and update key names accordingly.

## Django Secret Key
#API_PROJECT_DJANGO_KEY="your-generated-secret-key"

# Microsoft OAuth Values
#CLIENT_ID=""
#OBJECT_ID=""
#DIRECTORY_ID=""
#SECRECT_KEY="" 
#CLIENT_SECRET=""
#CLIENT_SECRET_ID=""
#AUTHORITY="https://login.microsoftonline.com/DOMAIN.sharepoint"
#TENANT_NAME=""
#TENANT_ID=""

⚠️ Rename `API_INITAL_DJANGO_KEY` to something more specific like `API_XYZ_DJANGO_KEY`, and match the name in your codebase (e.g., in `utils/key`).

---

## 📡 Purpose

- Backend-only API to integrate with a frontend application  
- Microsoft OAuth integration for secure user login  
- Proxy to Microsoft Graph API, hiding all credentials from the frontend

---

## 🗂 Folder Structure Overview

/api                   → Main Django app  
/utils/env/.env        → Environment variables  
/requirements.txt      → Python dependencies  
/manage.py             → Django CLI entry point

