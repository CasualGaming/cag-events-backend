from django.conf import settings
from django.db.models import Q
from django.http.response import HttpResponse

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from common.permissions import DenyAll, DisjunctionPermission, IsActive, StringPermission
from common.request_utils import get_query_param_bool, get_query_param_int, get_query_param_str

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

        is_active = get_query_param_bool(self.request, "active")
        if is_active is not None:
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

        seating_id = get_query_param_int(self.request, "seating")
        if seating_id is not None:
            queryset = queryset.filter(seating=seating_id)

        area_code = get_query_param_str(self.request, "area_code")
        if area_code is not None:
            queryset = queryset.filter(area__area_code=area_code)

        row_number = get_query_param_int(self.request, "row_number")
        if row_number is not None:
            queryset = queryset.filter(row_number=row_number)

        is_taken = get_query_param_bool(self.request, "is_taken")
        if is_taken is not None:
            if is_taken:
                queryset = queryset.filter(~Q(assigned_ticket=None))
            else:
                queryset = queryset.filter(assigned_ticket=None)

        is_reserved = get_query_param_bool(self.request, "is_reserved")
        if is_reserved is not None:
            queryset = queryset.filter(is_reserved=is_reserved)

        is_available = get_query_param_bool(self.request, "is_available")
        if is_available is not None:
            if is_available:
                queryset = queryset.filter(assigned_ticket=None, is_reserved=False)
            else:
                queryset = queryset.filter(~Q(assigned_ticket=None) | Q(is_reserved=True))

        return queryset
