from rest_framework import serializers

from modules.packages.models import UserPackageProgress


class PackageProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPackageProgress
        fields = ('user', 'package', 'item_done', 'status')

