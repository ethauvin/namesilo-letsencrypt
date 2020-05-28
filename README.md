# NameSilo Let's Encrypt

[![License (3-Clause BSD)](https://img.shields.io/badge/license-BSD%203--Clause-blue.svg?style=flat-square)](http://opensource.org/licenses/BSD-3-Clause)
[![Python 3.4](https://img.shields.io/badge/python-3.4-blue.svg)](https://www.python.org/)

Python scripts (hook) to automate obtaining [Let's Encrypt](https://letsencrypt.org/) certificates,
using [Certbot](https://certbot.eff.org/) DNS-01 challenge validation for domains DNS hosted on
[NameSilo](https://www.namesilo.com/).

## Setup

The scripts use the [tldextract](https://github.com/john-kurkowski/tldextract) and [untangle](https://untangle.readthedocs.io/en/latest/) libraries, if not already installed on your system:

```
pip install tldextract untangle
```

Download the [latest release](https://github.com/ethauvin/namesilo-letsencrypt/releases) archive and expand it in the desired directory.


## Configuration

Add your [NameSilo API key](https://www.namesilo.com/account_api.php)
to the top of the `config.py` file:

```python
# Get your API Key from: https://www.namesilo.com/account_api.php
apikey = "YOUR_API_KEY"
```

Alternatively, the API key can be set in the `NAMESILO_API` environment variable.

## Using with Certbot

To issue or renew a certificate using the hook scripts, try something like:

<pre>
certbot certonly --manual --email you@example.com \
--agree-tos --manual-public-ip-logging-ok \
--preferred-challenges=dns \
--manual-auth-hook <em>/path/to/authenticator.py</em> \
--manual-cleanup-hook <em>/path/to/cleanup.py</em> \
-d *.example.com -d example.com
</pre>

Please note that NameSilo DNS propagation takes up to **15 minutes**. The scripts will wait **25 minutes** before completing, just to be safe.
