import asyncio
from naxai.async_client import NaxaiAsyncClient
from naxai.models.voice.responses.call_responses import CreateCallResponse

# Assuming NAXAI_CLIENT_ID and NAXAI_SECRET are set in environment.

DESTINATION = "123456789"
FROM_NUMBER = "123456789"

async def main():

    async with NaxaiAsyncClient() as client:
        response: CreateCallResponse = await client.voice.call.create(welcome={"say": "Welcome to the SDK Demo!"},
                                                                      language="en-GB",
                                                                      to=[DESTINATION],
                                                                      from_=FROM_NUMBER,
                                                                      end={"say": "Thank you for using the Naxai SDK Demo!"})
        for call in response.calls:
            print(f"Call with id: {call.call_id} to destination: {call.to} will be sent shortly.")

asyncio.run(main())
