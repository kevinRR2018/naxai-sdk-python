from naxai.resources.voice_resources.reporting_resources.outbound import OutboundResource
from naxai.resources.voice_resources.reporting_resources.inbound import InboundResource
from naxai.resources.voice_resources.reporting_resources.transfer import TransferResource

class ReportingResource:

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting/metrics"
        self.outbound: OutboundResource = OutboundResource(self._client, self.root_path)
        self.inbound: InboundResource = InboundResource(self._client, self.root_path)
        self.transfer: TransferResource = TransferResource(self._client, self.root_path)
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}