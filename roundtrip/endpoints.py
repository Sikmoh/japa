#    Module Imports
# ------------------------------------------------
from basehandler import api_response
from auth.core import permission
# from restrictions.rate_limiting import limiter
from roundtrip.data_access import *

from errors.v1.handlers import ApiError


# @limiter.limit("5 per day")
def roundtrip(**kwargs):
    """
            Fetch fare for roundtrip
        :return: Fares
        :errors:
            raises an APIError
        """
    permission(kwargs['token_info'], access_role='basic')
    fare = FareDacc.roundtrip(kwargs)
    return fare















