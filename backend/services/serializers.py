from rest_framework import serializers
from .models import ServiceRequest, ServiceImage
from .catalog import CATEGORIES, SCHEMAS

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ("id","image","uploaded_at")
        read_only_fields = ("id","uploaded_at")
        notes = serializers.CharField(required=False, allow_blank=True, max_length=500)

class ServiceRequestSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceRequest
        fields = (
            "id","category",
            "name","email","phone","address","time_from","hours","days_of_week","notes",
            "extra","status","current_step","created_at","updated_at","images"
        )
        read_only_fields = ("id","status","current_step","created_at","updated_at","images")

    def validate_category(self, v):
        if v not in CATEGORIES:
            raise serializers.ValidationError("Invalid category.")
        return v

    def validate(self, data):
        base_required = ["name","email","phone","address"]
        missing = [f for f in base_required if not (data.get(f) or getattr(self.instance, f, None))]
        if missing:
            raise serializers.ValidationError({f:"This field is required." for f in missing})

        category = data.get("category") or getattr(self.instance,"category",None)
        extra = data.get("extra") if "extra" in data else getattr(self.instance,"extra",{})
        schema = SCHEMAS.get(category)
        if schema:
            for req in schema["required"]:
                if extra.get(req) in [None,"",[]]:
                    raise serializers.ValidationError({"extra":{req:"Required for this category."}})
            for field, rules in schema["fields"].items():
                if field in extra:
                    val = extra[field]; t = rules.get("type")
                    if t=="string" and not isinstance(val,str): raise serializers.ValidationError({"extra":{field:"Must be string"}})
                    if t=="integer" and not isinstance(val,int): raise serializers.ValidationError({"extra":{field:"Must be integer"}})
                    if t=="boolean" and not isinstance(val,bool): raise serializers.ValidationError({"extra":{field:"Must be boolean"}})
                    if "enum" in rules and val not in rules["enum"]: raise serializers.ValidationError({"extra":{field:f"Must be one of {rules['enum']}"}})
                    if "min" in rules and isinstance(val,int) and val < rules["min"]: raise serializers.ValidationError({"extra":{field:f"Min {rules['min']}"}})
                    if "max" in rules and isinstance(val,int) and val > rules["max"]: raise serializers.ValidationError({"extra":{field:f"Max {rules['max']}"}})
        return data

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
