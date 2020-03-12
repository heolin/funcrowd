

class PackagesMetadataSearch:
    def __init__(self, mission_packages, search):
        self.mission_packages = mission_packages
        self.search = {
            f"metadata__{key}": value
            for (key, value) in search.items()
        }

    def get_query(self):
        return self.mission_packages.packages.filter(**self.search)
