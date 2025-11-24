import os
def notify_user(message):
    """
    Display a notification to the user.
    
    Args:
        message (str): The message to display in the notification.
    """
    os.system(f'notify-send "WhatsApp Automation" "{message}"')