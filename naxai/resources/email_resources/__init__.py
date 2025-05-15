"""
Email resources package for the Naxai SDK.

This package provides access to various email-related API resources including:
- Activity logs: For tracking email delivery and engagement
- Domains: For managing email sending domains and verification
- Newsletters: For creating and managing email newsletters
- Reporting: For analyzing email performance metrics
- Sender identities: For managing email sender profiles
- Suppression lists: For handling bounces and unsubscribes
- Templates: For creating reusable email templates
- Transactional: For sending transactional emails
"""

from .activity_logs import ActivityLogsResource
from .domains import DomainsResource
from .newsletters import NewslettersResource
from .reporting import ReportingResource
from .sender_identities import SenderIdentitiesResource
from .suppression_lists import SuppressionListsResource
from .templates import TemplatesResource
from .transactional import TransactionalResource

__all__ = [
    "ActivityLogsResource",
    "DomainsResource",
    "NewslettersResource",
    "ReportingResource",
    "SenderIdentitiesResource",
    "SuppressionListsResource",
    "TemplatesResource",
    "TransactionalResource",
]

RESOURCE_CLASSES = {
    "activity_logs": ActivityLogsResource,
    "domains": DomainsResource,
    "newsletters": NewslettersResource,
    "reporting": ReportingResource,
    "sender_identities": SenderIdentitiesResource,
    "suppression_lists": SuppressionListsResource,
    "templates": TemplatesResource,
    "transactional": TransactionalResource,
}
