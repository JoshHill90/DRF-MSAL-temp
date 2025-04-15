import os
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent		
ven = current_dir / "./env/.env/"
load_dotenv(ven)

class EmailKeys:

	host = os.getenv('API_PSMS_EMAIL_HOST')
	send_email = os.getenv('API_PSMS_MANAGER_EMAIL')
	send_passwd = os.getenv('API_PSMS_EMAIL_PASSWORD')
	port = os.getenv('API_PSMS_EMAIL_PORT')
	
	owner_email = os.getenv('API_PSMS_EMAIL_CONTACT')


class BackEnd: 
    dj_key = os.getenv('API_PSMS_DJANGO_KEY')
 
class MSAuth:
    CLIENT_ID = os.getenv("CLIENT_ID")

    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"

    REDIRECT_PATH = "/getAToken"  

    ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  
    SCOPE = ["User.ReadBasic.All"]

    SESSION_TYPE = "filesystem"

    FLASK_SECRET = os.getenv('FLASK_SECRET')

class DataBase:
    db_engine = os.getenv("API_PSMS_DB_ENGINE")
    db_name = os.getenv("API_PSMS_DB_NAME")
    db_user = os.getenv("API_PSMS_DB_USER")
    db_key = os.getenv("API_PSMS_DB_PSSWORD")
    db_host = os.getenv("API_PSMS_DB_HOST")
    db_port = os.getenv("API_PSMS_DB_PORT")

