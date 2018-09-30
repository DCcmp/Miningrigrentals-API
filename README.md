# Miningrigrentals-API
Python3 API wrapper class for https://miningrigrentals.com

<b>How-To:<b><br>

example:
<code>



from miningrigrentals import miningrigrentals

mrr = miningrigrentals('<API-KEY>','<API-SECRET>')

servers = mrr.get_info_servers() #  Get a list of MRR rig servers.

x11_servers = mrr.get_info_algo('x11'') #  Get statistics for an algo (suggested price, unit information, current rented hash/etc)



</code>
