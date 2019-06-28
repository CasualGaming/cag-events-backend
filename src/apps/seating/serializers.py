from drf_dynamic_fields import DynamicFieldsMixin

from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, ValidationError

from .models import AreaLayout, RowLayout


class RowLayoutSerializer(ModelSerializer):
    """Serializes a row layout."""

    class Meta:
        model = RowLayout
        fields = ("row_number",
                  "description",
                  "seat_count_horizontal",
                  "seat_count_vertical",
                  "offset_horizontal",
                  "offset_vertical",
                  "rotation",
                  "seat_width",
                  "seat_height",
                  "seat_spacing_horizontal",
                  "seat_spacing_vertical")


class AreaLayoutSerializer(DynamicFieldsMixin, HyperlinkedModelSerializer):
    """Serializes an area layout including rows."""

    row_layouts = RowLayoutSerializer(many=True)

    class Meta:
        model = AreaLayout
        fields = ("url",
                  "short_title",
                  "long_title",
                  "width",
                  "height",
                  "background_url",
                  "is_active",
                  "row_layouts")

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
