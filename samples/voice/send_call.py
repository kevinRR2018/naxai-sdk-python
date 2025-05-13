from naxai.client import NaxaiClient
from naxai.models.voice.responses.call_responses import CreateCallResponse

DESTINATION = "123456789"
FROM_NUMBER = "123456789"

with NaxaiClient() as client:

    response: CreateCallResponse = client.voice.call.create(welcome={"say": "Welcome to the SDK Demo!"},
                                                            language="en-GB",
                                                            to=[DESTINATION],
                                                            from_=FROM_NUMBER,
                                                            end={"say": "Thank you for using the Naxai SDK Demo!"})
    for call in response.calls:
        print(f"Call with id: {call.call_id} to destination: {call.to} will be sent shortly.")
