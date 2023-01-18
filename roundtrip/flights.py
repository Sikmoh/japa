# -*- coding: utf-8 -*-

# ------------------------------------------------
#    External imports
# ------------------------------------------------

import asyncio
import aiohttp
import requests

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#     Module Imports
# ------------------------------------------------
from errors.v1.handlers import ApiError

# ------------------------------------------------
#    Script Wide Variables
# ------------------------------------------------
URL = 'https://api.flightapi.io'


# ------------------------------------------------
#          CLASSES START HERE
# ------------------------------------------------


class Fares(object):

    def __init__(self, **kwargs):

        # Variables used for each instance of the class.
        self.fare_data = []

    async def fetch_json(self, session: aiohttp.ClientSession(), url: str, **kwargs):
        """
            Async function to make multiple api calls and fetch json data for each call
            Adding the data when received to the self.facts_data list
        """
        # import pdb;
        # pdb.set_trace()
        print(f"Requesting {url}")
        resp = await session.request('GET', url=url, **kwargs)

        if resp.status != 200:
            error = f"problem with url {url}"
            raise ApiError(message=error, status_code=resp.status)

        data = await resp.json(content_type=None)
        print(f"Received data for {url}")
        print(type(data['fares']))
        # Put the result's data on the end of the list
        self.fare_data.append(data['fares'])

    async def api_query(self, urls, **kwargs):
        """
            Set up an async task for each url in urls and call the urls asynchronously.
            Asyncio sets up a client connection to handle all the calls to the cat api.
            Calls fetch_json after each task/url call gets a response
        """
        # Single client session for all the api calls. We use an open HTTP connection for simplicity here. The
        # data is open source...
        client = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

        async with client as session:
            # Create fetch tasks from the urls
            tasks = []

            for url in urls:
                tasks.append(self.fetch_json(session=session, url=url, **kwargs))

            # waits for asyncio.gather() to be completed, required because we want to sort when all data has arrived
            await asyncio.gather(*tasks, return_exceptions=True)

    def request_data_async(self, query, departure=None, arrival=None, departure_date=None, return_date=None, adults=None, children=None,
                           infants=None, cabin=None, currency=None):
        """
            This method formats n number of urls with the parameter 'query'
        """
        # Create the initial url
        urls = []
        urls_append = urls.append

        if departure:
            urls_append(f"{URL}{query}/{departure}/{arrival}/{departure_date}/{return_date}/{adults}/{children}/{infants}/{cabin}/{currency}")
        else:
            urls.append(f"{URL}{query}/")

        # Call the api query function
        asyncio.run(self.api_query(urls))

    def request_data_sync(self, query, departure=None, arrival=None, departure_date=None, return_date=None, adults=None, children=None,
                           infants=None, cabin=None, currency=None):
        """
            Request and wait for our data to return
            In this method we are using the requests package to make a simple synchronous API call
            The code is blocked until the response is received.

        :return:
        """
        status = ""

        try:
            # Format the URL from the main cat URL plus the query/queries
            link = 'https://api.flightapi.io'
            URL = f"{link}{query}/{departure}/{arrival}/{departure_date}/{return_date}/{adults}/{children}/{infants}/{cabin}/{currency}"


            # make the request
            r = requests.get(url=URL)
            # Raise the status to make sure it was successful. If it is not the below exception will occur
            status = r.status_code
            r.raise_for_status()

            # We have success - let's return the data
            # extracting data in JSON format
            self.fare_data = r.json()
        except requests.ConnectionError as e:
            msg = "OOPS!! Connection Error. Make sure you are connected to a live Internet connection."
            raise ApiError(message=msg, status_code=status)
        except requests.Timeout as e:
            msg = "timeout-error"
            raise ApiError(message=msg, status_code=status)
        except requests.HTTPError as e:
            if status == 404:
                msg = "not-found"
            elif status == 400:
                msg = "bad-request"
            elif status == 500:
                msg = "server-error-"
            else:
                msg = "something-went-wrong"
            raise ApiError(message=msg, status_code=status)
        except KeyboardInterrupt:
            msg = "program-closed"
            raise ApiError(message=msg, status_code=status)
