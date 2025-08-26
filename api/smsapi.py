import requests
import json
from dotenv import dotenv_values
config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}



def send_sms(phone_number, message, sender_id="Sender Name"):

    # CREATE OBJECT
    username = config.get("SMS_USERNAME")
    password = config.get("SMS_PASSWORD")

      # request token (use dict so requests handles form encoding safely)
    token_payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    
    # Make the request
    response = requests.request("POST", f"{config.get('SMS_API_URL')}/token", data=token_payload,

    headers={'content-type': "application/x-www-form-urlencoded"})

    res = json.loads(response.text)
    

   
    payload = {
    "senderid": sender_id,
    "mobile":phone_number,
    "message": message,
    }



    sendsmsResp = requests.request("POST", f"{config.get('SMS_API_URL')}/api/SendSMS",data= json.dumps(payload),
    headers={'Content-Type':'application/json', 'Authorization': 'Bearer ' + res['access_token']})

    print(sendsmsResp)

    respObj = json.loads(sendsmsResp.text)

    return respObj

# Example usage
# response = send_sms("+252612907406", "Hello, this is a test message", "Istaqaana")
