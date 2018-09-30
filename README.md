# Miningrigrentals-API
Python3 API wrapper class for https://miningrigrentals.com

<b>How-To:<b><br>

example:
<code>



from miningrigrentals import miningrigrentals

mrr = miningrigrentals('<API-KEY>','<API-SECRET>')

servers = mrr.get_servers() #  To get a list of servers

x11_servers = mrr.get_algo('x11'') #  To list all x11 mining rigs

</code>
