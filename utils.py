# -*- coding: utf-8 -*-

# ------------------------------------------------
#    External imports
# ------------------------------------------------

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#    Module Imports
# ------------------------------------------------
import smtplib

from config.app_config import SMTP


def read_json_file(json_file):
    import json

    # Opening JSON file
    with open(json_file) as jf:
        # returns JSON object as
        # a dictionary
        data = json.load(jf)

    return data


def options_filter(data, options):
    """
        Filters through a list of dictionaries or a single dictionary and removes any data from the options dict that is set to false

    :param data: maybe a list of dicts or a single dict
    :param options: The options to filter on
    :return: Filtered data
    """

    # Define an empty list to hold all our filtered dictionaries
    fl = []

    def filter_options(data_set, options):
        new_dict = {}
        for k, _ in data_set.items():
            # The following line is a dictionary comprehension. It is used to filter optional data specified in the kwargs argument.
            # which is passed into the API by the client request as a JSON dictionary of options.
            # The way it works is to filter key-value pairs from the returned film_entity dictionary against the kwargs dictionary.
            # Any key-value pair in the film_entity dictionary that is in the options dictionary of kwargs and set to False should be excluded from the returned data.
            filtered_dict = {k: v for (k, v) in data_set.items() if k not in options or options[k] is True}
            new_dict.update(filtered_dict)
        return new_dict

    if isinstance(data, list):

        for item in data:
            if isinstance(item, dict):
                fd = filter_options(item, options)
                fl.append(fd)

    elif isinstance(data, dict):

        fd = filter_options(data, options)
        fl.append(fd)

    else:
        return data

    return fl


def dict_sort(data, sort_by: str, sort_order: str):
    """
        param: data: The data to sort
        param: sort_by: A string to sort by
        param: sort_order: Ascending or Descending order - asc  or desc
        returns: sorted data by key sort_by
    """

    # See below for the use of this flag
    int_convert = False

    # TODO - LET'S LEAVE THIS LINE COMMENTED AND LET STUDENTS SEE THAT THE HEIGHT IS NOT SORTED CORRECTLY AS A STRING THEN APPLY THE FOLLOWING LINE
    # TODO TRYING TO FIGURE OUT NICE COMPREHENSION FOR ABOVE cd = [i for i in data if i.get(sort_by) and int(i[sort_by])]
    if data[0][sort_by].isdigit():

        for d in data:
            d[sort_by] = int(d[sort_by])

        int_convert = True
    # Using a lambda for the sort routine - For every item in data lambda d applies the sort_by string in a default of ascending order
    sorted_list = sorted(data, key=lambda x: x[sort_by])

    if sort_order == "desc":
        sorted_list.reverse()

    # If we converted the sort values to integers, we need to convert them back here.

    # WHY - well because the API spec states that these should be returned as strings.
    # They are received as strings from the data source and as such are specified in the API as strings
    # Therefore anyone reading the api assumes that they are returned as strings and not integers.

    # WHY do we not convert all stringed numbers to integers, well that could take a lot of time. If it was our
    # own data source we would store them as integers in the first place.
    if int_convert:
        for d in data:
            d[sort_by] = str(d[sort_by])

    return sorted_list


def dict_excludes(data: dict, excludes: list) -> dict:
    """
        Exclude a set of keys from a dictionary dict - using
        keys from the excludes list.
        Exercise - Write this as a one liner comprehension.
    """
    new_dict = {}

    for k, v in data.items():
        if k not in excludes:
            new_dict[k] = v

    return new_dict


def send_email(receiver_email, subject, message_body):
    """
        Sends a plain-text email to receiver_email address with
        subject and message body

    :param receiver_email Email address of the receiver (To)
    :param subject Subject field of the email
    :param message_body Body of the email.
    """
    message = f"""\
    Subject: {subject}

    {message_body}."""

    with smtplib.SMTP(SMTP['host'], SMTP['port']) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP['sender_email'], SMTP['sender_password'])
        server.sendmail(SMTP['sender_email'], receiver_email, message)
        server.quit()
