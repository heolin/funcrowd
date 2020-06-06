from rest_framework import serializers

from modules.packages.api.serializers.package import PackageSerializer
from modules.packages.models import UserPackageProgress


class PackageProgressSerializer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)

    class Meta:
        model = UserPackageProgress
        fields = ('user', 'package', 'items_done', 'items_count', 'progress', 'status', 'reward')
