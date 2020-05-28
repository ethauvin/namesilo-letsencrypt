#!/usr/bin/env python3

#  authenticator.py
#
#  Copyright (c) 2019-2020, Erik C. Thauvin (erik@thauvin.net)
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#    Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#    Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#    Neither the name of this project nor the names of its contributors may be
#    used to endorse or promote products derived from this software without
#    specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#  THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import tempfile
import time
import urllib.request

import tldextract
import untangle

from config import apikey, wait


def sleep(minutes):
    if minutes < 16:
        minutes = 16
    time.sleep(minutes * 60)


domain = os.environ['CERTBOT_DOMAIN']
validation = os.environ['CERTBOT_VALIDATION']
tmpdir = os.path.join(tempfile.gettempdir(), "CERTBOT_" + domain)
rrhost = "_acme-challenge"

if "NAMESILO_API" in os.environ:
    apikey = os.environ['NAMESILO_API']

tld = tldextract.extract(domain)
nsdomain = tld.domain + "." + tld.suffix
if tld.subdomain:
    rrhost += "." + tld.subdomain

url = "https://www.namesilo.com/api/dnsAddRecord?\
version=1&type=xml&key=" + apikey + "&domain=" + nsdomain + "&rrtype=TXT\
&rrhost=" + rrhost + "&rrvalue=" + validation + "&rrttl=3600"

req = urllib.request.Request(
    url,
    data=None,
    headers={
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) '
                       'Gecko/20100101 Firefox/74.0')
    }
)

with urllib.request.urlopen(req) as response:
    html = response.read()
xml = untangle.parse(str(html, 'utf-8'))

if not os.path.exists(tmpdir):
    os.mkdir(tmpdir, 0o700)

if xml.namesilo.reply.code.cdata == '300':
    f = open(os.path.join(tmpdir, "RECORD_ID"), "a+")
    print(xml.namesilo.reply.record_id.cdata, file=f)
    f.close()
else:
    print("{}: {} ({})".format(domain,
                               xml.namesilo.reply.detail.cdata,
                               xml.namesilo.reply.code.cdata), file=sys.stderr)
    sys.exit(1)

# Sleep X minutes
sleep(wait)
