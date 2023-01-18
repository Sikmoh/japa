
# *-* coding: UTF-8 *-*

# ------------------------------------------------
#     Python Library Imports
# ------------------------------------------------

# ------------------------------------------------
#    External Python Library Imports
# ------------------------------------------------

# ------------------------------------------------
#     Module Imports
# ------------------------------------------------

# ------------------------------------------------
#    Base Handling Functions Begin Here
# ------------------------------------------------

def api_response(payload=None):
    """
       Generate and return an appropriate response to the API request

    :param payload:
    :return:
    """
    if isinstance(payload, dict):
        # If something in dict return with data else just status
        return payload
    else:
        return {}
