import requests

class OctoPrint(object):

    def __init__(self, api_url, api_key):
        """
        :param api_url: OctoPrint API URL
        :param api_key: OctoPrint API Key
        """
        self.api_url = api_url
        self.api_key = api_key

    def get(self, endpoint):
        """
        An internal method for doing the HTTP GET request.
        """
        req = requests.get('{0}/{1}?apikey={2}'.format(api_url, endpoint,
                                                       api_key))
        return req

    def connection(self):
        """
        Retrieve the current connection settings, including information
        regarding the available baudrates and serial ports and the current
        connection state.
        """
        req = self.get('connection')
        return req.json()

    def printer_sd(self):
        """
        Retrieves the current state of the printer's SD card.
        """
        req = self.get('printer/sd')

        if req.status_code == 404:
            raise Exception("SD Support Disabled", "SD support has been "
                            "disabled in OctoPrint's config.")

        resp = req.json()
        return resp.get('ready', False)

    def job(self):
        """
        Retrieve information about the current job (if there is one).
        """
        req = self.get('job')
        return resp.json()