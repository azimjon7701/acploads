from rest_framework.permissions import BasePermission
from account import models

class IsCarrier(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        profile:models.Profile = request.user.profile
        # bu yerda companiya carrier ekanligini tekshiradigan kod bo'lishi kerak
        return bool(request.user and request.user.is_authenticated)