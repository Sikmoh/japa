#    Module Imports
# ------------------------------------------------
from basehandler import api_response
from auth.core import permission
#from restrictions.rate_limiting import limiter
from onewaytrip.data_access import *

from errors.v1.handlers import ApiError


#@limiter.limit("5 per day")
def oneway(**kwargs):
    """
            Fetch fare for onewaytrip
        :return: Fares
        :errors:
            raises an APIError
        """
    permission(kwargs['token_info'], access_role='basic')
    fare = FareDacc.onewaytrip(kwargs)
    return api_response({'result': fare})
