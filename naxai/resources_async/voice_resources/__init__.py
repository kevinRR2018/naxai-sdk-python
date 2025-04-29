from .call import CallResource
from .broadcast import BroadcastsResource
from .scheduled_calls import ScheduledCallsResource
from .reporting import ReportingResource
from .activity_logs import ActivityLogsResource

RESOURCE_CLASSES = {
    "call": CallResource,
    "broadcasts": BroadcastsResource,
    "scheduled_calls": ScheduledCallsResource,
    "reporting": ReportingResource,
    "activity_logs": ActivityLogsResource
}