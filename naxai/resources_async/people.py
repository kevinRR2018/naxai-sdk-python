from .people_resources import RESOURCE_CLASSES
from .people_resources.attributes import AttributesResource
from .people_resources.contacts import ContactsResource
from .people_resources.exports import ExportsResource
from .people_resources.imports import ImportsResource
from .people_resources.segments import SegmentsResource

class PeopleResource:
    """
    Provides access to people related API actions.
    """

    def __init__(self, client):
        self._client = client
        self.root_path = "/people"
        self.attributes: AttributesResource
        self.contacts: ContactsResource
        self.exports: ExportsResource
        self.imports: ImportsResource
        self.segments: SegmentsResource

        for name, cls in RESOURCE_CLASSES.items():
            self._client.logger.debug("Setting up resource %s. Resource class: %s", name, cls)
            setattr(self, name, cls(client, self.root_path))