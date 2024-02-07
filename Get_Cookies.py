from dotenv import load_dotenv
import os

def get_cookies():
    load_dotenv(dotenv_path="Cookies.env")

    auth_token = os.getenv("AUTH_TOKEN")
    twid = os.getenv("TWID")
    ct0 = os.getenv("CT0")

    return auth_token, twid, ct0