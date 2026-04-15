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
    clean_ip = re.sub(r"[A-Za-z]", "0", str(ip))
    parts = clean_ip.split(".")
    parts = [str(int(part)) for part in parts]
    clean_ip = ".".join(parts)
    ip_int = int(netaddr.IPAddress(clean_ip))
    idx = bisect(ips["low"], ip_int) - 1
    return ips.iloc[idx]["region"]


class Filing:
    def __init__(self, html):
        self.dates = []
        self.sic = None
        self.addresses = []

        self.dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", html)

        sic_match = re.search(r"SIC=(\d{3,4})", html)
        if sic_match:
            self.sic = int(sic_match.group(1))

        mailer_blocks = re.findall(
            r'<div class="mailer">(.*?)(?=<div class="mailer">|$)',
            html,
            re.DOTALL
        )

        for block in mailer_blocks:
            lines = re.findall(r'<span class="mailerAddress">(.*?)</span>', block, re.DOTALL)
            cleaned = [re.sub(r"\s+", " ", line).strip() for line in lines if line.strip()]
            if cleaned:
                self.addresses.append("\n".join(cleaned))

    def state(self):
        for address in self.addresses:
            match = re.search(r"\b([A-Z]{2})\s+\d{5}(?:-\d{4})?\b", address)
            if match:
                return match.group(1)
        return None