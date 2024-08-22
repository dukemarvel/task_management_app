from pyfcm import FCMNotification
import os
from dotenv import load_dotenv

load_dotenv()
push_service = FCMNotification(api_key=os.getenv("FIREBASE_SERVER_KEY"))

def send_push_notification(token: str, message: str):
    result = push_service.notify_single_device(registration_id=token, message_body=message)
    return result
