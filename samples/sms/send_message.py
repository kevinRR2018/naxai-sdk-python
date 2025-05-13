from naxai.client import NaxaiClient
from naxai.models.sms.responses.send_responses import SendSMSResponse

DESTINATION = "123456789"
FROM_NUMBER = "8810"

with NaxaiClient() as client:

    response: SendSMSResponse = client.sms.send(to=[DESTINATION],
                                                from_=FROM_NUMBER,
                                                body="This is a test message from Naxai SDK!")
    for message in response.messages:
        print(f"Message with id: {message.message_id} to destination: {message.to} will be sent shortly.")
