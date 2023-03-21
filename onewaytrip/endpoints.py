#    Module Imports
# ------------------------------------------------
from basehandler import api_response
from auth.core import permission
from onewaytrip.data_access import *

from errors.v1.handlers import ApiError


def oneway(**kwargs):
    """
            Fetch fare for onewaytrip
        :return: Fares
        :errors:
            raises an APIError
        """
    permission(kwargs['token_info'], access_role='basic')
    fare = FareDacc.onewaytrip(kwargs)
    if fare is None:
        raise ApiError('No fare found', 404)
    return api_response({'result': fare})
