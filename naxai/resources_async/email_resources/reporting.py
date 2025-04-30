from .reporting_resources.metrics import MetricsResource
from .reporting_resources.clicked_urls import ClickedUrlsResource

class ReportingResource:

    def __init__(self, client, root_path):
            self._client = client
            self.root_path = root_path + "/reporting"
            self.version = "2023-03-25"
            self.headers = {"X-version": self.version,
                            "Content-Type": "application/json"}
            
            self.metrics = MetricsResource(client, self.root_path)
            self.cliqued_urls = ClickedUrlsResource(client, self.root_path)