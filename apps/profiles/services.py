from core.settings import AUTH_USER_MODEL

from apps.companies.models import Company
from apps.profiles.models import *


def create_profile(user: AUTH_USER_MODEL, validate_data):
    if user.type == 1:
        return Administrador.objects.create(user=user, name=validate_data['name'])

    company = Company.objects.get(id=validate_data['company_id'])

    if user.type == 3:
        return AccountManager.objects.create(
            user=user,
            name=validate_data['name'],
            company=company)


