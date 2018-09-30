# Miningrigrentals-API
Python3 API wrapper class for https://miningrigrentals.com

<b>How-To:</b></br>

example:

```python
from miningrigrentals import miningrigrentals

APIKEY = "YOUR API KEY"
APISECRET = "YOUR API SECRET"

mrr = miningrigrentals.API(APIKEY, APISECRET)

servers = mrr.get_info_servers() #  Get a list of MRR rig servers.

x11_algo = mrr.get_info_algo('x11') #  Get statistics for an algo (suggested price, unit information, current rented hash/etc)

```
