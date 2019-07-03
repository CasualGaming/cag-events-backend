from django.conf import settings
from django.db.models import Q
from django.http.response import HttpResponse

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from common.permissions import DenyAll, DisjunctionPermission, IsActive, StringPermission

from .generators import generate_area_layout
from .models import AreaLayout, Seat, Seating
from .serializers import AreaLayoutSerializer, SeatSerializer, SeatingSerializer


class AreaLayoutViewSet(ModelViewSet):
    queryset = AreaLayout.objects.all()
    serializer_class = AreaLayoutSerializer

    def get_permissions(self):
        permissions = {
            # List has more granular permission filtering
            "list": [StringPermission("seating.layout.list")],
            "retrieve": [DisjunctionPermission(IsActive(), StringPermission("seating.layout.view_inactive"))],
            "create": [StringPermission("seating.layout.create")],
            "update": [StringPermission("seating.layout.change")],
            "partial_update": [StringPermission("seating.layout.change")],
            "destroy": [StringPermission("seating.layout.delete")],
            "generated_image": [DisjunctionPermission(IsActive(), StringPermission("seating.layout.generate_image"))],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_queryset(self):
        queryset = self.queryset
        if self.action != "list":
            return queryset

        # Hide all inactive if the user is not allowed to see inactive
        if not self.request.user.has_perm("seating.layout.view_inactive"):
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
            # List has more granular permission filtering
            "list": [StringPermission("seating.seating.list")],
            "retrieve": [DisjunctionPermission(IsActive(), StringPermission("seating.seating.view_inactive"))],
            "create": [StringPermission("seating.seating.create")],
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


class SeatViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_permissions(self):
        permissions = {
            "list": [],
            "retrieve": [],
            "create": [StringPermission("seating.seat.create")],
            "update": [StringPermission("seating.seat.change")],
            "partial_update": [StringPermission("seating.seat.change")],
            "destroy": [StringPermission("seating.seat.delete")],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_queryset(self):
        queryset = self.queryset
        if self.action != "list":
            return queryset

        seating_str = self.request.query_params.get("seating", None)
        if seating_str is not None:
            try:
                seating = int(seating_str)
                queryset = queryset.filter(seating=seating)
            except ValueError:
                pass

        area_code = self.request.query_params.get("area_code", None)
        if area_code is not None:
            queryset = queryset.filter(area__area_code=area_code)

        row_number_str = self.request.query_params.get("row_number", None)
        if row_number_str is not None:
            try:
                row_number = int(row_number_str)
                queryset = queryset.filter(row_number=row_number)
            except ValueError:
                pass

        is_taken_str = self.request.query_params.get("is_taken", None)
        if is_taken_str is not None and (is_taken_str == "true" or is_taken_str == "false"):
            is_taken = is_taken_str == "true"
            if is_taken:
                queryset = queryset.filter(~Q(assigned_ticket=None))
            else:
                queryset = queryset.filter(assigned_ticket=None)

        is_reserved_str = self.request.query_params.get("is_reserved", None)
        if is_reserved_str is not None and (is_reserved_str == "true" or is_reserved_str == "false"):
            is_reserved = is_reserved_str == "true"
            queryset = queryset.filter(is_reserved=is_reserved)

        is_available_str = self.request.query_params.get("is_available", None)
        if is_available_str is not None and (is_available_str == "true" or is_available_str == "false"):
            is_available = is_available_str == "true"
            if is_available:
                queryset = queryset.filter(assigned_ticket=None, is_reserved=False)
            else:
                queryset = queryset.filter(~Q(assigned_ticket=None) | Q(is_reserved=True))

        return queryset
