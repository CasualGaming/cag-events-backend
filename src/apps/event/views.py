from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from common.permissions import DenyAll, IsAuthenticated, StringPermission
from common.request_utils import get_query_param_str

from .models import Attendance, Event
from .serializers import AttendanceArrivalSerializer, AttendanceAttendSerializer, AttendanceSerializer, AttendanceUpdateSerializer, EventSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        permissions = {
            "list": [],
            "retrieve": [],
            "create": [StringPermission("event.event.create")],
            "update": [StringPermission("event.event.change")],
            "partial_update": [StringPermission("event.event.change")],
            "destroy": [StringPermission("event.event.delete")],
            "attend": [IsAuthenticated()],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_queryset(self):
        queryset = self.queryset
        if self.action != "list":
            return queryset

        slug = get_query_param_str(self.request, "slug")
        if slug is not None:
            queryset = queryset.filter(slug=slug)

        return queryset

    # TODO test
    @action(detail=True, methods=["GET", "POST", "DELETE"])
    def attend(self, request, *args, **kwargs):
        user = self.request.user
        event = self.get_object()
        attendance_qs = self.get_object().attendances.filter(user=user)
        attendance = attendance_qs[0] if attendance_qs.exists() else None

        if self.request.method == "POST":
            # Attend
            if attendance is None:
                Attendance.objects.create(event=event, user=user)
        elif self.request.method == "DELETE":
            # Unattend
            if attendance is not None:
                attendance_qs.delete()

        if attendance is not None:
            serializer = AttendanceAttendSerializer(attendance, context={"request": self.request})
            return Response(serializer.data)
        else:
            # TODO return 404?
            return Response()


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()

    def get_permissions(self):
        permissions = {
            "list": [StringPermission("event.attendance.list")],
            "retrieve": [StringPermission("event.attendance.view")],
            "create": [StringPermission("event.attendance.create")],
            "update": [StringPermission("event.attendance.change")],
            "partial_update": [StringPermission("event.attendance.change")],
            "destroy": [StringPermission("event.attendance.delete")],
            "arrival": [StringPermission("event.attendance.register_arrival")],
        }
        return permissions.get(self.action, [DenyAll()])

    def get_serializer_class(self):
        if self.action == "update" or self.action == "partial_update":
            return AttendanceUpdateSerializer
        if self.action == "arrival":
            return AttendanceArrivalSerializer
        return AttendanceSerializer

    @action(detail=True, methods=["GET", "POST", "DELETE"])
    def arrival(self, request, *args, **kwargs):
        attendance = self.get_object()
        if self.request.method == "POST":
            # Set arrived now
            attendance.arrival_time = timezone.now()
            attendance.save()
        elif self.request.method == "DELETE":
            # Remove arrival
            attendance.arrival_time = None
            attendance.save()
        serializer = AttendanceArrivalSerializer(attendance, context={"request": self.request})
        return Response(serializer.data)
