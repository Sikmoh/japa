from flights import Fares


class FareDacc(object):
    """
            Abstract Fare Data Access Class
        """

    @staticmethod
    def onewaytrip(kwargs: dict):
        """
             Retrieve a flight fare
        :param kwargs:
        :return: flight fares
        """

        fare = Fares()
        # Build and request the URL by adding the animal_type and amount
        fare.request_data_async('/onewaytrip/634e9cd0046255a726227fc5', kwargs['departure'], kwargs['arrival'],
                               kwargs['departure_date'], kwargs['adults'], kwargs['children'], kwargs['infants'],
                               kwargs['cabin'], kwargs['currency'])
        return fare.fare_data[0]['fares'][:10]
