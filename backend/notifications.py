from pyfcm import FCMNotification

push_service = FCMNotification(api_key="your_firebase_server_key")

def send_push_notification(token: str, message: str):
    result = push_service.notify_single_device(registration_id=token, message_body=message)
    return result
