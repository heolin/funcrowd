from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.packages.api.serializers import PackageProgressSerializer
from modules.packages.models import Package, UserPackageProgress


class PackageProgressView(GenericAPIView):
    serializer_class = PackageProgressSerializer

    def get(self, request, package_id, *args, **kwargs):
        package = Package.objects.filter(id=package_id).first()
        if package:
            progress = package.get_user_progress(request.user)
            serializer = self.serializer_class(progress)
            return Response(serializer.data)
        raise NotFound("No Package found given id.")


class PackagesProgressListView(GenericAPIView):
    serializer_class = PackageProgressSerializer

    def get(self, request, *args, **kwargs):
        progresses = UserPackageProgress.objects.filter(user=request.user)
        serializer = self.serializer_class(progresses, many=True)
        return Response(serializer.data)
