from drf_dynamic_fields import DynamicFieldsMixin

from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField, ModelSerializer, StringRelatedField, ValidationError

from apps.ticket.models import TicketType

from authentication.models import User

from .models import Area, AreaLayout, RowLayout, RowTicketType, Seat, Seating


class RowLayoutNestedSerializer(ModelSerializer):
    """Serializes a row layout, for use within the area layout serializer."""

    class Meta:
        model = RowLayout
        fields = [
            "row_number",
            "description",
            "seat_count_horizontal",
            "seat_count_vertical",
            "offset_horizontal",
            "offset_vertical",
            "rotation",
            "seat_width",
            "seat_height",
            "seat_spacing_horizontal",
            "seat_spacing_vertical",
            "seat_count",
        ]


class AreaLayoutSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):
    """Serializes an area layout including rows."""

    row_layouts = RowLayoutNestedSerializer(many=True)

    class Meta:
        model = AreaLayout
        fields = [
            "url",
            "title",
            "is_enabled",
            "width",
            "height",
            "background_url",
            "row_layouts",
            "seat_count",
        ]

    def validate(self, data):
        row_numbers = []
        for row_layout in data.get("row_layouts", []):
            if "row_number" not in row_layout:
                continue
            row_number = row_layout["row_number"]
            if row_number in row_numbers:
                raise ValidationError("Duplicate row number in area layout")
            row_numbers.append(row_number)
        return data

    def create(self, validated_data):
        row_layouts_data = validated_data.pop("row_layouts", [])
        area_layout = super(AreaLayoutSerializer, self).create(validated_data)
        for row_layout_data in row_layouts_data:
            RowLayout.objects.create(area_layout=area_layout, **row_layout_data)
        return area_layout

    def update(self, instance, validated_data):
        contains_row_layouts = "row_layouts" in validated_data
        row_layouts_data = validated_data.pop("row_layouts", [])
        area_layout = super(AreaLayoutSerializer, self).update(instance, validated_data)
        if contains_row_layouts:
            area_layout.row_layouts.all().delete()
            for row_layout_data in row_layouts_data:
                RowLayout.objects.create(area_layout=area_layout, **row_layout_data)
        return area_layout


class RowTicketTypeNestedSerializer(ModelSerializer):
    """Serializes a row ticket type relation, for use within the area serializer."""

    ticket_type = HyperlinkedRelatedField(view_name="tickettype-detail", queryset=TicketType.objects.all())

    class Meta:
        model = RowTicketType
        fields = [
            "row_number",
            "ticket_type",
        ]


class AreaNestedSerializer(ModelSerializer):
    """Serializes an area, for use within the seating serializer."""

    area_layout = HyperlinkedRelatedField(view_name="arealayout-detail", queryset=AreaLayout.objects.all())
    row_ticket_types = RowTicketTypeNestedSerializer(many=True)

    class Meta:
        model = Area
        fields = [
            "title",
            "area_code",
            "description",
            "area_layout",
            "row_ticket_types",
        ]


class SeatingSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):
    """Serializes an area layout including rows."""

    areas = AreaNestedSerializer(many=True)

    class Meta:
        model = Seating
        fields = [
            "url",
            "event",
            "is_enabled",
            "areas",
            "seat_count",
        ]
        extra_kwargs = {
            "event": {
                "view_name": "event-detail",
            },
        }

    def validate(self, data):
        area_codes = []
        for area in data.get("areas", []):
            if "area_code" not in area:
                continue
            area_code = area["area_code"]
            if area_code in area_codes:
                raise ValidationError("Duplicate area code in seating")
            area_codes.append(area_code)
        return data

    def create(self, validated_data):
        areas_data = validated_data.pop("areas", [])
        seating = super(SeatingSerializer, self).create(validated_data)
        for area_data in areas_data:
            Area.objects.create(seating=seating, **area_data)
        return seating

    def update(self, instance, validated_data):
        contains_areas = "areas" in validated_data
        areas_data = validated_data.pop("areas", [])
        seating = super(SeatingSerializer, self).update(instance, validated_data)
        if contains_areas:
            seating.areas.all().delete()
            for area_data in areas_data:
                Area.objects.create(seating=seating, **area_data)
        return seating


class SeatSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):
    """Serializes a seat, including the assigned ticket and user assigned to that ticket."""

    seating = HyperlinkedRelatedField(source="area.seating", view_name="seating-detail", queryset=Seating.objects.all())
    area_code = StringRelatedField(source="area.area_code")
    user = HyperlinkedRelatedField(source="assigned_ticket.assignee", view_name="user-detail", lookup_field="username", queryset=User.objects.all())
    public_user = HyperlinkedRelatedField(source="assigned_ticket.assignee.public_seat_user", view_name="user-detail", lookup_field="username", queryset=User.objects.all())

    class Meta:
        model = Seat
        _public_fields = [
            "url",
            "seating",
            "area_code",
            "row_number",
            "seat_number",
            "is_reserved",
            "is_taken",
            "public_user",
        ]
        _user_fields = [
            "user",
        ]
        _ticket_fields = [
            "assigned_ticket",
        ]
        fields = _public_fields + _user_fields + _ticket_fields

    @property
    def fields(self):
        fields = super(SeatSerializer, self).fields
        allowed_fields = self.get_allowed_fields()
        for field in set(fields.keys()):
            if field not in allowed_fields:
                fields.pop(field, None)
        return fields

    def get_allowed_fields(self):
        allowed_fields = []
        request = self.context["request"]
        is_detail = isinstance(self.instance, User)
        assigned_ticket = self.instance.assigned_ticket if is_detail else None
        is_assigned_to_self = is_detail and assigned_ticket is not None and assigned_ticket.assigned_user == request.user

        # Public fields
        allowed_fields += self.Meta._public_fields

        # User field
        if request.user.has_perm("seating.seat.view_hidden_user") or is_assigned_to_self:
            allowed_fields += self.Meta._user_fields

        # Ticket field
        if request.user.has_perm("seating.seat.view_ticket") or is_assigned_to_self:
            allowed_fields += self.Meta._ticket_fields

        return allowed_fields
