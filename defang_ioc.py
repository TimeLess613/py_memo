import re
from urllib.parse import urlparse

def defang(ioc):
    """
    Defangs the given IoC by replacing only the last '.' with '[.]'.
    Also replaces 'http' with 'hxxp' to prevent accidental clicks.
    """
    # Replace http/https with hxxp/hxxps
    ioc = re.sub(r'^http', 'hxxp', ioc, flags=re.IGNORECASE)

    # If it's a URL, defang only the last dot in the hostname
    if '://' in ioc:
        parsed = urlparse(ioc)
        hostname = parsed.hostname or ''
        if hostname.count('.') >= 1:
            parts = hostname.rsplit('.', 2)
            if len(parts) >= 2:
                hostname_defanged = '.'.join(parts[:-1]) + '[.]' + parts[-1]
                ioc = ioc.replace(hostname, hostname_defanged)

    else:
        # If it's an IP or domain, defang only the last dot
        if ioc.count('.') >= 1:
            parts = ioc.rsplit('.', 1)
            ioc = parts[0] + '[.]' + parts[1]

    return ioc

# Example usage
if __name__ == "__main__":
    iocs = [
        "http://malicious.com/path",
        "http://malicious.com:8080/path",
        "https://bad.domain.net",
        "1.2.3.4",
        "example.org",
        "abc.def.ghi.jkl"
    ]

    print("Defanged Results:")
    for ioc in iocs:
        print(defang(ioc))