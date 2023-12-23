import contextvars

import redis
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from account import models

# REDIS_DB = 0
# REDIS_CONN = (redis.Redis(host='127.0.0.1', port=6379, db=REDIS_DB))

current_user = contextvars.ContextVar('current_user', default=None)


def __set_current_user(user_data):
    current_user.set(user_data)


def get_current_user():
    return current_user.get()


def manage_current_user(token: models.AuthToken) -> dict:
    # user_data_json = REDIS_CONN.get(token.key)
    #
    # if user_data_json:
    #     user_data = json.loads(user_data_json)
    # else:
    user: models.User = token.user
    profile: models.Profile = user.profile
    company: models.Company = profile.get_company()

    user_data: dict = {
        "id": user.id,
        "entity_type": company.entity_type,
        "last_name": user.last_name,
        "first_name": user.first_name,
        "email": user.email,
        "phone": profile.phone,
        "mc": company.mc,
        "usdot": company.usdot,
        "company_name": company.name,
        "company_address": company.address1,
        "company_phone": company.phone

    }
    # REDIS_CONN.set(token.key, json.dumps(user_data))
    __set_current_user(user_data)
    return user_data


class AuthTokenAuthentication(TokenAuthentication):
    model = models.AuthToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        # Check if the token is expired
        if token.expired_date and token.expired_date < timezone.now():
            raise AuthenticationFailed('Token has expired')

        manage_current_user(token)
        return token.user, token
