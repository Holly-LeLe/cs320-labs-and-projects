# Add additional imports if needed

from bisect import bisect
import re
import netaddr
import pandas as pd

# Load IP-to-location data
ips = pd.read_csv("ip2location.csv")


def lookup_region(ip):
    """
    Given an IP address (string), return its region.
    Steps:
    - Clean the IP (replace letters with 0)
    - Convert to integer using netaddr.IPAddress
    - Use bisect on ips["low"] to find the index
    - Return the corresponding region
    """
    # TODO: implement IP lookup
    pass


class Filing:
    def __init__(self, html):
        self.dates = None
        self.sic = None
        self.addresses = []

        # TODO: extract dates using regex (format: YYYY-MM-DD)
        # TODO: extract SIC (3–4 digit number after "SIC=")
        # TODO: extract addresses inside <div class="mailer"> ... </div>

    def state(self):
        """
        Return the 2-letter state code found in addresses, or None if not found.
        Hint: Look for patterns like 'WI 53706'.
        """
        # TODO: implement state extraction using regex
        pass