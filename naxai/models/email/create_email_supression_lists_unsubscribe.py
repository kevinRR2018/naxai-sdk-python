from pydantic import BaseModel, Field

#TODO: email validation
class CreateEmailSuppressionListsUnsubscribe(BaseModel):
    email: str
    domain_name: str = Field(alias="domainName")

    model_config = {"populate_by_name": True}
