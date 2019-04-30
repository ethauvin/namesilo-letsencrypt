# NameSilo Let's Encrypt

Python scripts (hook) to automate obtaining [Let's Encrypt](https://letsencrypt.org/) certificates,
using [Certbot](https://certbot.eff.org/) DNS-01 challenge validation for domains DNS hosted on
[NameSilo](https://www.namesilo.com/).

## Configuration

Add you [NameSilo API key](https://www.namesilo.com/account_api.php)
to the top of the `config.py` file:

```python
# Get your API Key from: https://www.namesilo.com/account_api.php
apikey = "YOUR_API_KEY"
```

Alternatively, the API key can be set in the `NAMESILO_API` environment variable.

## Using with Certbot

To issue a new certificate using the hook scripts, try something like:

<pre>
certbot certonly --manual --email you@example.com \
--agree-tos --manual-public-ip-logging-ok \
--preferred-challenges=dns \
--manual-auth-hook <em>/path/to/authenticator.py</em> \
--manual-cleanup-hook <em>/path/to/cleanup.py</em> \
-d *.example.com -d example.com
</pre>

Or to renew an existing certificate:

<pre>
certbot renew --manual --email you@example.com \
--agree-tos --manual-public-ip-logging-ok \
--preferred-challenges=dns \
--manual-auth-hook <em>/path/to/authenticator.py</em> \
--manual-cleanup-hook <em>/path/to/cleanup.py</em> \
-d *.example.com -d example.com
</pre>

Please note that NameSilo DNS propagation takes up to **15 minutes**,
so the scripts will wait 16 minutes before completing.

