from rest_framework.permissions import BasePermission

from utils.authentication import get_current_user


class IsCarrier(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user_data = get_current_user()
        entity_type = user_data.get('entity_type')
        if bool(request.user and request.user.is_authenticated) and entity_type == 'carrier':
            return True
        return False
