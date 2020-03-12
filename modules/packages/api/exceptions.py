from rest_framework import status
from rest_framework.exceptions import APIException


class MissingSearchGetParam(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Missing "search" param in the request'
    default_code = 'missing_search_param'


class SearchGetParamMalformed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The "search" param in the request was malformed'
    default_code = 'search_param_malformed'


class MissingAggregationGetParam(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The "aggregation" param in the request was missing'
    default_code = 'missing_aggregation_field'
