import asyncio
from naxai.async_client import NaxaiAsyncClient
from naxai.models.sms.responses.send_responses import SendSMSResponse

DESTINATION = "123456789"
FROM_NUMBER = "8810"

async def main():

    async with NaxaiAsyncClient() as client:
        response: SendSMSResponse = await client.sms.send(to=[DESTINATION],
                                                          from_=FROM_NUMBER,
                                                          body="This is a test message from Naxai SDK!") 
        for message in response.messages:
            print(f"Message with id: {message.message_id} to destination: {message.to} will be sent shortly.")

asyncio.run(main())
