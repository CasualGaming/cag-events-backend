from django.conf import settings
from django.http.response import HttpResponse

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from common.permissions import DenyAll, DisjunctionPermission, IsActive, StringPermission

from .generators import generate_area_layout
from .models import AreaLayout, Seating
from .serializers import AreaLayoutSerializer, SeatingSerializer


class AreaLayoutViewSet(ModelViewSet):
    queryset = AreaLayout.objects.all()
    serializer_class = AreaLayoutSerializer

    def get_permissions(self):
        permissions = {
            "list": [StringPermission("seating.area_layout.list")],
            "retrieve": [DisjunctionPermission(IsActive(), StringPermission("seating.area_layout.view_inactive"))],
            "create": [StringPermission("seating.area_layout.create")],
            "update": [StringPermission("seating.area_layout.change")],
            "partial_update": [StringPermission("seating.area_layout.change")],
            "destroy": [StringPermission("seating.area_layout.delete")],
            "generated_image": [DisjunctionPermission(IsActive(), StringPermission("seating.area_layout.view_inactive"))],
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

    @action(detail=True, methods=["get"])
    def generated_image(self, request, *args, **kwargs):
        if settings.SEATING_GENERATE_IMAGES:
            area_layout = self.get_object()
            content = generate_area_layout(area_layout)
            return HttpResponse(content, content_type="image/svg+xml")
        else:
            response = HttpResponse("Disabled")
            response.status_code = 503
            return response


class SeatingViewSet(ModelViewSet):
    queryset = Seating.objects.all()
    serializer_class = SeatingSerializer

    def get_permissions(self):
        permissions = {
            "list": [StringPermission("seating.seating.list")],
            "create": [StringPermission("seating.seating.create")],
            "retrieve": [DisjunctionPermission(IsActive(), StringPermission("seating.seating.view_inactive"))],
            "update": [StringPermission("seating.seating.change")],
            "partial_update": [StringPermission("seating.seating.change")],
            "destroy": [StringPermission("seating.seating.delete")],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_queryset(self):
        queryset = self.queryset
        if self.action != "list":
            return queryset

        # Hide all inactive if the user is not allowed to see inactive
        if not self.request.user.has_perm("seating.seating.view_inactive"):
            queryset = queryset.filter(is_active=True)

        is_active_str = self.request.query_params.get("active", None)
        if is_active_str is not None and (is_active_str == "true" or is_active_str == "false"):
            is_active = is_active_str == "true"
            queryset = queryset.filter(is_active=is_active)

        return queryset
