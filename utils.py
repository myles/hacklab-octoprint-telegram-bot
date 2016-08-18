from collections import OrderedDict


def seconds_to_human(seconds):
    """
    Convert seconds to human readable format like 1M.

    From Thomas Sileo's blog post How to convert seconds to human readable
    interval back and forth with Python: <https://myl.be/d4>.

    :param seconds: Seconds to convert
    :type seconds: int
    
    :rtype: str
    :return: Human readable string
    """
    interval_dict = OrderedDict([("years", 365*86400),  # 1 year
                                 ("months", 30*86400),  # 1 month
                                 ("weeks", 7*86400),    # 1 week
                                 ("days", 86400),       # 1 day
                                 ("hours", 3600),       # 1 hour
                                 ("minutes", 60),       # 1 minute
                                 ("seconds", 1)])       # 1 second

    seconds = int(seconds)
    string = ""
    for unit, value in interval_dict.items():
        subres = seconds / value
        if subres:
            seconds -= value * subres
            if subres == 1:
                unit = unit.rstrip('s')
            string += "{0} {1} ".format(subres, unit)

    return string.rstrip()
