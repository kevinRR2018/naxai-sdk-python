from .broadcast_settings_resources.dynamic_load_distribution import DynamicLoadDistributionResource

class SettingsResource:
    """ A class for handling settings-related operations for voice broadcasts. """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/settings"
        self.dynamic_load_distribution = DynamicLoadDistributionResource(self._client,
                                                                         self.root_path)
