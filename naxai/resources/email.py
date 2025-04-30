from .email_resources.transactional import TransactionalResource
from .email_resources.activity_logs import ActivityLogsResource
from .email_resources.domains import DomainsResource
from .email_resources.newsletters import NewslettersResource
from .email_resources.reporting import ReportingResource
from .email_resources.sender_identities import SenderIdentitiesResource
from .email_resources.suppression_lists import SuppressionListsResource
from .email_resources.templates import TemplatesResource
from .email_resources import RESOURCE_CLASSES


class EmailResource:
    """
    Provides access to email related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.transactional: TransactionalResource
        self.activity_logs: ActivityLogsResource
        self.domains: DomainsResource
        self.newsletters: NewslettersResource
        self.reporting: ReportingResource
        self.sender_identities: SenderIdentitiesResource
        self.suppression_lists: SuppressionListsResource
        self.templates: TemplatesResource
        

        for name, cls in RESOURCE_CLASSES.items():
            self._client.logger.debug("Setting up resource %s. Resource class: %s", name, cls)
            setattr(self, name, cls(client, "/email"))