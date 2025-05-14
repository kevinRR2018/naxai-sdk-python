"""
Email response models for the Naxai SDK.

This module provides data structures for responses from email-related API operations,
including domains, activity logs, metrics, newsletters, senders, templates, and
transactional emails.
"""

from .domains_responses import (ListSharedDomainsResponse,
                                ListDomainsResponse,
                                CreateDomainResponse,
                                GetDomainResponse,
                                UpdateDomainResponse,
                                VerifyDomainResponse)
from .activity_logs_responses import ListEmailActivityLogsResponse, GetEmailActivityLogsResponse
from .metrics_responses import ListClickedUrlsMetricsResponse, ListMetricsResponse
from .newsletters_responses import (CreateNewsletterResponse,
                                    ListNewsLettersResponse,
                                    UpdateNewsletterResponse,
                                    GetNewsletterResponse)
from .senders_responses import (CreateSenderResponse,
                                ListSendersResponse,
                                GetSenderResponse,
                                UpdateSenderResponse)
from .templates_responses import (CreateTemplateResponse,
                                ListTemplatesResponse,
                                GetTemplateResponse,
                                UpdateTemplateResponse,
                                ListSharedTemplatesRespone,
                                GetSharedTemplateResponse)
from .transactional_responses import SendTransactionalEmailResponse

__all__ = [
    "ListSharedDomainsResponse",
    "ListDomainsResponse",
    "CreateDomainResponse",
    "GetDomainResponse",
    "UpdateDomainResponse",
    "VerifyDomainResponse",
    "ListEmailActivityLogsResponse",
    "GetEmailActivityLogsResponse",
    "ListClickedUrlsMetricsResponse",
    "ListMetricsResponse",
    "CreateNewsletterResponse",
    "ListNewsLettersResponse",
    "UpdateNewsletterResponse",
    "GetNewsletterResponse",
    "CreateSenderResponse",
    "ListSendersResponse",
    "GetSenderResponse",
    "UpdateSenderResponse",
    "CreateTemplateResponse",
    "ListTemplatesResponse",
    "GetTemplateResponse",
    "UpdateTemplateResponse",
    "ListSharedTemplatesRespone",
    "GetSharedTemplateResponse",
    "SendTransactionalEmailResponse"
]
