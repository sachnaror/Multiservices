from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ServiceRequest, ServiceImage
from .serializers import ServiceRequestSerializer, ImageUploadSerializer

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all().order_by("-updated_at")
    serializer_class = ServiceRequestSerializer

    @action(detail=True, methods=["post"], url_path="images")
    def upload_image(self, request, pk=None):
        req = self.get_object()
        ser = ImageUploadSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        img = ServiceImage.objects.create(request=req, image=ser.validated_data["image"])
        return Response({"id": img.id, "image": request.build_absolute_uri(img.image.url)}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        obj = self.get_object()
        ser = self.get_serializer(obj, data=request.data or {}, partial=True)
        ser.is_valid(raise_exception=True)
        obj.status = ServiceRequest.Status.SUBMITTED
        obj.current_step = 3
        obj.save(update_fields=["status","current_step","updated_at"])
        return Response(self.get_serializer(obj).data)
