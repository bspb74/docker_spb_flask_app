import requests
import json
from flask import jsonify

host = "localhost"
port = "5551"


def login(email, pwd):
    # Login to get a JWT (assuming you have a login endpoint)
    login_url = f"http://{host}:{port}/api/v1/auth/login"
    login_data = {"email": f"{email}", "pwd": f"{pwd}"}
    response = requests.post(login_url, json=login_data)
    return response


def getProducts(response, protected_resource_url):
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Access token: %s" % access_token)

        # Access a protected endpoint using the JWT
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(protected_resource_url, headers=headers)

        if response.status_code == 200:
            protected_data = response.json()
            print("Protected data:", json.dumps(protected_data, indent=4, ensure_ascii=False))
        else:
            print("Failed to access protected resource:", response.status_code)


if __name__ == '__main__':

    email = "bspb74@gmail.com"
    pwd = "qw#rTy5152"

    get_products = True
    if get_products:
        protected_resource_url = f"http://{host}:{port}/api/v1/products"
        login_response = login(email, pwd)
        getProducts(login_response, protected_resource_url)

