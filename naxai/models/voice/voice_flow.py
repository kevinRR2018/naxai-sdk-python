from typing import Optional, Literal, Union
from pydantic import BaseModel, Field



class End(BaseModel):
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given

class Whisper(BaseModel):
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given

class Transfer(BaseModel):
    destination: str = Field(alias="destination")
    attempts: Optional[int] = Field(alias="attempts", default=1, max_digits=1) # validate that it's between 1 and 3
    timeout: Optional[int] = Field(alias="timeout", default=15, max_digits=2) # validate that it's between 5 and 30
    whisper: Optional[Whisper] = Field(alias="whisper", default=None)

class Choice(BaseModel):
    key: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#"]
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given
    replay: Optional[int] = Field(alias="replay", default=0)
    transfer: Optional[Transfer] = Field(alias="transfer", default=None)

class Menu(BaseModel):
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given
    replay: Optional[int] = Field(alias="replay", default=0)
    choices: list[Choice] = Field(alias="choices")

class Welcome(BaseModel):
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given
    replay: Optional[int] = Field(alias="replay", default=0)

class VoiceMail(BaseModel):
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given

class VoiceFlow(BaseModel):
    machine_detection: Optional[bool] = Field(alias="machineDetection", default=False)
    voicemail: Optional[VoiceMail] = Field(default=None)
    welcome: Welcome = Field(alias="welcome")
    menu: Optional[Menu] = Field(alias="menu", default=None)
    end: Optional[End] = Field(alias="end", default=None)