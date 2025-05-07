from .voice_resources import RESOURCE_CLASSES
from .voice_resources.call import CallResource
from .voice_resources.broadcast import BroadcastsResource
from .voice_resources.scheduled_calls import ScheduledCallsResource
from .voice_resources.reporting import ReportingResource
from .voice_resources.activity_logs import ActivityLogsResource

class VoiceResource:
    """
    Provides access to voice related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.call: CallResource = CallResource(client, "/voice")
        self.broadcasts: BroadcastsResource
        #self.scheduled_calls: ScheduledCallsResource
        self.reporting: ReportingResource
        self.activity_logs: ActivityLogsResource

        for name, cls in RESOURCE_CLASSES.items():
            self._client.logger.debug("Setting up resource %s. Resource class: %s", name, cls)
            setattr(self, name, cls(client, "/voice"))