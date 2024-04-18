from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status

class UserComapanyNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('No company associated with the user was found')
    default_code = 'company_not_found'