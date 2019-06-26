from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework_xml.renderers import XMLRenderer

from common.permissions import DenyAll, DisjunctionPermission, IsActive, ModelPermission

from .models import AreaLayout
from .serializers import AreaLayoutSerializer


class AreaLayoutViewSet(ModelViewSet):
    queryset = AreaLayout.objects.all()
    serializer_class = AreaLayoutSerializer

    def get_permissions(self):
        permissions = {
            "list": [ModelPermission("seating.area_layout.list")],
            "create": [ModelPermission("seating.area_layout.create")],
            "retrieve": [DisjunctionPermission(IsActive(), ModelPermission("seating.area_layout.view_inactive"))],
            "update": [ModelPermission("seating.area_layout.change")],
            "partial_update": [ModelPermission("seating.area_layout.change")],
            "destroy": [ModelPermission("seating.area_layout.delete")],
            "generated_image": [DisjunctionPermission(IsActive(), ModelPermission("seating.area_layout.view_inactive"))],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_queryset(self):
        queryset = self.queryset
        if self.action != "list":
            return queryset

        # Hide all inactive if the user is not allowed to see inactive
        if not self.request.user.has_perm("seating.area_layout.view_inactive"):
            queryset = queryset.filter(is_active=True)

        is_active_str = self.request.query_params.get("active", None)
        if is_active_str is not None and (is_active_str == "true" or is_active_str == "false"):
            is_active = is_active_str == "true"
            queryset = queryset.filter(is_active=is_active)

        return queryset

    @action(detail=True, methods=["get"], renderer_classes=[XMLRenderer])
    def generated_image(self, request, *args, **kwargs):
        # TODO
        content = "<svg></svg>"
        return Response(content, content_type="image/svg+xml")
