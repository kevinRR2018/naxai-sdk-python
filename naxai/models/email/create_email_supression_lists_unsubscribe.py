"""
Email suppression list models for the Naxai SDK.

This module defines the data structures for managing email suppression lists,
which help prevent sending emails to recipients who have unsubscribed.
"""

from pydantic import BaseModel, Field

#TODO: email validation
class CreateEmailSuppressionListsUnsubscribe(BaseModel):
    """
    Model representing a request to add an email address to the suppression list.
    
    This class defines the structure for adding an email address to the unsubscribe
    suppression list, preventing future emails from being sent to this address
    for the specified domain.
    
    Attributes:
        email (str): The email address to add to the suppression list.
            This is the address that will no longer receive emails.
        domain_name (str): The domain name for which this suppression applies.
            Mapped from JSON key 'domainName'.
    
    Example:
        >>> unsubscribe = CreateEmailSuppressionListsUnsubscribe(
        ...     email="recipient@example.com",
        ...     domainName="sender-domain.com"
        ... )
        >>> print(f"Unsubscribing {unsubscribe.email} from {unsubscribe.domain_name}")
        Unsubscribing recipient@example.com from sender-domain.com
    
    Note:
        - This class supports both alias-based and direct field name access
        - Email validation is planned but not yet implemented (see TODO)
        - Adding an email to the suppression list is permanent unless manually removed
        - The domain_name should be the sending domain, not the recipient's domain
    
    TODO:
        - Add email validation to ensure valid email format
    """
    email: str
    domain_name: str = Field(alias="domainName")

    model_config = {"populate_by_name": True}
