from dotenv import load_dotenv
import os


def get_cookies():
    load_dotenv(dotenv_path="Cookies.env")

    auth_token = os.getenv("AUTH_TOKEN")
    twid = os.getenv("TWID")
    ct0 = os.getenv("CT0")

    return auth_token, twid, ct0


def get_second_cookies():
    load_dotenv(dotenv_path="Cookies2.env")

    auth_token = os.getenv("AUTH_TOKEN_2")
    twid = os.getenv("TWID_2")
    ct0 = os.getenv("CT0_2")

    return auth_token, twid, ct0
