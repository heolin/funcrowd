from rest_framework import status
from rest_framework.exceptions import APIException


class AccountUnactive(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Account is not active'
    default_code = 'account_not_active'


class UsernameUsed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Username is already used'
    default_code = 'username_used'


class EmailUsed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Email is already used'
    default_code = 'email_used'


class PasswordNotMatch(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Passwords does not match'
    default_code = 'password_not_match'


class ActivationTokenWrong(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Activation token is incorrect'
    default_code = 'activation_token_wrong'


class ActivationTokenExpired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Activation token has expired'
    default_code = 'activation_token_expired'


class ActivationTokenUsed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Activation token is already used'
    default_code = 'activation_token_used'


class UsernameNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User with following username not found.'
    default_code = 'username_not_found'


class EmailNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User with following email not found.'
    default_code = 'email_not_found'
