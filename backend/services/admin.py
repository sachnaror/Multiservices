from django.contrib import admin
from .models import ServiceRequest, ServiceImage

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("id","category","status","name","email","created_at","notes_short")
    list_filter = ("category","status","created_at")

    def notes_short(self, obj):
        return (obj.notes[:40] + "…") if obj.notes and len(obj.notes) > 40 else obj.notes
    notes_short.short_description = "Notes"

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ("id","request","uploaded_at")
