from rest_framework import viewsets, status
from rest_framework.response import Response
from main import models
from main.serializers import LoadSerializer
from utils.authentication import get_current_user


class LoadViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        loads = models.Load.objects.all()
        serializer = LoadSerializer(loads, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = LoadSerializer(data=request.data)
        if serializer.is_valid():
            current_user = get_current_user()
            current_profile = request.user.profile
            load = models.Load.objects.create(
                company_id=current_user.get('company_id'),
                owner_id=current_profile.id,

            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
