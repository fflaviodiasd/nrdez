from django.utils.translation import gettext_lazy as _
from datetime import datetime
from unidecode import unidecode
import uuid

from core.settings import AUTH_USER_MODEL

from .exceptions import UserComapanyNotFound


def hasCompany(profile) -> bool:
    if profile.company == None or profile.company == '':
        raise UserComapanyNotFound()


def isAdministrator(user: AUTH_USER_MODEL):
    return user.type == 1 or False


def isEmployee(user: AUTH_USER_MODEL):
    return user.type == 2 or False


def get_profile(generic_profile, type):
    if type == 1:
        return generic_profile.administrador

    if type == 2:
        return generic_profile.employee

    if type == 3:
        return generic_profile.accountmanager

    if type == 4 or type == 5:
        return generic_profile.provider

