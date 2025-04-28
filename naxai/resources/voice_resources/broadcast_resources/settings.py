from .broadcast_settings_resources.dynamic_load_distribution import DynamicLoadDistributionResource
class SettingsResource:
    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/settings"
        self.dynamic_load_distribution = DynamicLoadDistributionResource(self._client, self.root_path)
        self.version = "2023-03-25"
        self.headers = {"X-version": self.version,
                        "Content-Type": "application/json"}