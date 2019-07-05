from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Attendance, Event


class EventSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = [
            "url",
            "title",
            "slug",
            "start_time",
            "end_time",
            "location",
            "require_ticket",
            "age_requirement",
            "map_url",
            "banner_url",
            "description",
        ]


class AttendanceSerializer(HyperlinkedModelSerializer):
    """Serializer for viewing attendances."""

    class Meta:
        model = Attendance
        fields = [
            "url",
            "event",
            "user",
            "arrival_time",
            "has_arrived",
            "has_ticket",
        ]
        extra_kwargs = {
            "user": {
                "lookup_field": "username",
            },
        }


class AttendanceUpdateSerializer(HyperlinkedModelSerializer):
    """Serializer for changing attendances by staff."""

    class Meta:
        model = Attendance
        fields = [
            "url",
            "arrival_time",
            "has_arrived",
        ]


class AttendanceArrivalSerializer(HyperlinkedModelSerializer):
    """Serializer for registering arrivals by staff."""

    class Meta:
        model = Attendance
        fields = [
            "url",
            "has_arrived",
        ]


class AttendanceAttendSerializer(HyperlinkedModelSerializer):
    """Serializer for attending and unattending an event by users themselves."""

    class Meta:
        model = Attendance
        fields = [
            "url",
        ]
