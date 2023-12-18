from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from account.models import AuthToken


class AuthTokenAuthentication(TokenAuthentication):
    model = AuthToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        # Check if the token is expired
        if token.expired_date and token.expired_date < timezone.now():
            raise AuthenticationFailed('Token has expired')

        return token.user, token