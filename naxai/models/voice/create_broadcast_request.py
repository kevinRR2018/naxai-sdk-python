from pydantic import BaseModel, Field
from typing import Optional, Literal, Union
from .voice_flow import VoiceFlow

class ActionItem(BaseModel):
    attribute: Optional[str] = Field(alias="attribute", default=None)
    value: Optional[Union[str, int, bool]] = Field(alias="value", default=None)

class Sms(BaseModel):
    message: Optional[str] = Field(alias="message", default=None)
    sender_service_id: Optional[str] = Field(alias="senderServiceId", default=None)

class Inputs(BaseModel):
    field_0: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="0", default=None)
    field_1: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="1", default=None)
    field_2: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="2", default=None)
    field_3: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="3", default=None)
    field_4: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="4", default=None)
    field_5: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="5", default=None)
    field_6: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="6", default=None)
    field_7: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="7", default=None)
    field_8: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="8", default=None)
    field_9: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="9", default=None)
    field_star: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="star", default=None)
    field_hash: Optional[Union[list[ActionItem], dict[str, Sms]]] = Field(alias="hash", default=None)


class Status(BaseModel):
    delivered: Optional[Union[
        list[ActionItem],                # list of ActionItem
        dict[str, Sms]]]                # OR dict like {"sms": SmsMessage}
    failed: Optional[Union[
        list[ActionItem],                # list of ActionItem
        dict[str, Sms]]]                # OR dict like {"sms": SmsMessage}

class Actions(BaseModel):
    status: Optional[Status] = Field(alias="actions", default=None)
    inputs: Optional[Inputs] = Field(alias="inputs", default=None)

class CreateBroadcastRequest(BaseModel):
    name: str
    from_: str = Field(alias="from", min_length=8, max_length=15)
    source: Optional[str] = Field(alias="source", default="people")
    segment_ids: list[str] = Field(alias="segmentIds", max_length=1)
    inclube_unsubscribed: Optional[bool] = Field(alias="inclubeUnsubscribed", default=False)
    language: Optional[Literal["fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE"]] = "fr-BE"
    voice: Optional[Literal["woman", "man"]] = "woman"
    scheduled_at: Optional[str] = Field(alias="scheduledAt", default=None)
    retries: Optional[int] = 0
    retry_on_no_input: Optional[bool] = Field(alias="retryOnNoInput", default=False)
    retry_on_failed: Optional[bool] = Field(alias="retryOnFailed", default=False)
    retry_delays: Optional[list[int]] = Field(alias="retryDelays", default=None, min_length=0, max_length=3)
    calendar_id: Optional[str] = Field(alias="calendarId", default=None)
    distribution: Optional[Literal["none", "dynamic"]]= "none"
    dynamic_name: Optional[str] = Field(alias="dynamicName", default=None)
    voice_flow: VoiceFlow = Field(alias="voiceFlow")
    actions: Optional[Actions] = Field(alias="actions", default=None)

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
