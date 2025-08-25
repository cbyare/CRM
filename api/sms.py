import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

def sms(mobile, message, senderid="Sender Name"):
    # Get token
    payload = {
        "grant_type": "password",
        "username": config.get("SMS_USERNAME"),
        "password": config.get("SMS_PASSWORD"),
    }

    response = requests.post(
        f'{config.get("SMS_API_URL")}/token',
        data=payload,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    resp_dict1 = response.json()
    print(resp_dict1["access_token"])

    # Send SMS
    payload2 = {
        "senderid": senderid,
        "mobile": mobile,
        "message": message,
    }

    sendsmsResp = requests.post(
        f'{config.get("SMS_API_URL")}/api/SendSMS',
        json=payload2,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + resp_dict1["access_token"],
        },
    )
    return sendsmsResp.json()
