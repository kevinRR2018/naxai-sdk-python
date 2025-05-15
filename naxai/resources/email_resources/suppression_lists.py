"""
Email suppression lists resource for the Naxai SDK.

This module provides access to email suppression list functionality, including
management of bounces and unsubscribes to maintain email deliverability and
compliance with email marketing regulations. Suppression lists help prevent
sending emails to addresses that have previously bounced or opted out.
"""

from .suppression_lists_resources.unsubscribes import UnsubscribesResource
from .suppression_lists_resources.bounces import BouncesResource

class SuppressionListsResource:
    """ suppressionlists resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/suppression-lists"
        self.unsubscribes = UnsubscribesResource(client, self.root_path)
        self.bounces = BouncesResource(client, self.root_path)
        