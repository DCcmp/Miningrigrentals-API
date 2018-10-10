"""
Python3 API WRAPPER CLASS FOR https://miningrigrentals,com
"""
import hmac
import hashlib
import time
import requests

__author__ = "DJC @ https://coinminingpool.org"

BASEURL = 'https://www.miningrigrentals.com/api/v2'

# API ENDPOINTS
WHOAMI = "/whoami"
SERVERS = '/info/servers'
ALGOS = '/info/algos/'
ACCOUNT = '/account'
BALANCE = '/account/balance'
TRANSACTIONS = '/account/transactions'
PROFILE = '/account/profile'
MINE = '/rig/mine'
RIGS = '/rig/'
RENTAL = '/rental'

# REQUEST HEADER VARIABLES
XAPISIGN = 'x-api-sign'
XAPIKEY = 'x-api-key'
XAPINONCE = 'x-api-nonce'

# REQUEST TYPES
GET = 'GET'
PUT = 'PUT'
DELETE = 'DELETE'

# PARAMETER VARIABLES
MIN = 'min'
MAX = 'max'
TYPE = 'type'
RPI = 'rpi'
MINHOURS = 'minhours'
MAXHOURS = 'maxhours'
PRICE = 'price'
HASH = 'hash'
HASHRATE = 'hashrate'
OFFLINE = 'offline'
RENTED = 'rented'
REGION = 'region'
COUNT = 'count'
OFFSET = 'offset'
ORDERBY = 'orderby'
ORDERDIR = 'orderdir'
ALGO = "algo"
HISTORY = "history"
RIG = "rig"
START = "start"
LIMIT = "limit"


class API:

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.nonce = time.time() * 1000

    def _build_sign_string(self, method: str) -> str:
        string = '{}{}{}'.format(self.key, self.nonce, method)
        return hmac.new(key=self.secret.encode(),
                        msg=string.encode(),
                        digestmod=hashlib.sha1).hexdigest()

    def _build_headers(self, signature: str) -> dict:
        return {XAPISIGN: signature,
                XAPIKEY: self.key,
                XAPINONCE: str(self.nonce)}

    def _api_call(self, endpoint: str,
                  params: dict=None,
                  request: str=None) -> dict:
        """
        BASE FUNCTION FOR MAKING API CALLS TO MRR
        """
        if not params:
            params = {}

        if request is PUT:
            request = requests.put
        elif request is DELETE:
            request = requests.delete
        else:
            request = requests.get

        self.nonce += 1

        url = BASEURL + endpoint

        signature = self._build_sign_string(endpoint)

        headers = self._build_headers(signature)

        response = request(url=url, headers=headers, params=params).json()
        if not response.get("success"):
            raise Exception("API CALL WAS NOT SUCCESSFULL")
        else:
            return response.get("data")

    def whoami(self) -> dict:
        """
        GET /whoami
        :return: Test connectivity and return information about you
        """
        return self._api_call(WHOAMI)

    def get_info_algos(self) -> dict:
        """
        GET /info/algos
        :return: Get all algos and statistics for them (suggested price, unit information, current rented hash/etc)
        """
        return self._api_call(ALGOS)

    def get_info_servers(self) -> dict:
        """
        GET /info/servers
        :return: Get a list of MRR rig servers.
        """
        return self._api_call(SERVERS)

    def get_rig(self, algo_type: str,
                minhours_min: int = None,
                minhours_max: int = None,
                maxhours_min: int = None,
                maxhours_max: int = None,
                rpi_min: int = None,
                rpi_max: int = None,
                hash_min: int = None,
                hash_max: int = None,
                hash_type: str = None,
                price_min: int = None,
                price_max: int = None,
                offline: bool = False,
                rented: bool = False,
                region_type: str = None,
                region: bool = None,
                count: int = 100,
                offset: int = 0,
                orderby: str = 'score',
                orderdir: str = 'asc'
                ) -> dict:
        """
        GET /rig
        :param algo_type: 	Rig type, eg: sha256, scrypt, x11, etc
        :param minhours_min: Filter the minmum hours of the rig > Minimum value to filter
        :param minhours_max: Filter the minmum hours of the rig > Maximum value to filter
        :param maxhours_min: Filter the maximum hours of the rig Minimum value to filter
        :param maxhours_max: Filter the maximum hours of the rig > Maximum value to filter
        :param rpi_min: Filter the RPI score > Minimum value to filter
        :param rpi_max:	Filter the RPI score > Maximum value to filter
        :param hash_min: Filter the hashrate > Minimum value to filter
        :param hash_max: Filter the hashrate > Maximum value to filter
        :param hash_type: The hash type of min/max. defaults to "mh", possible values: [hash,kh,mh,gh,th]
        :param price_min: Filter the price > Minimum value to filter
        :param price_max: Filter the price > Maximum value to filter
        :param offline: To show or not to show offline rigs
        :param rented: to show or not to show rented rigs
        :param region_type: Determines if this filter is an inclusive or exclusive filter.. possible options are [include,exclude]
        :param region: A region to include/exclude
        :param count: Number of results to return, max is 100
        :param offset: What result number to start with, returning COUNT results
        :param orderby: Field to order the results by. Default is "score", Possible values: [rpi,hash,price,minhrs,maxhrs,score]
        :param orderdir: Order direction
        :return: Search for rigs on a specified algo. This is identical to the main rig list pages.
        """
        params = {TYPE: algo_type,
                  OFFLINE: offline,
                  RENTED: rented,
                  COUNT: count,
                  OFFSET: offset,
                  ORDERBY: orderby,
                  ORDERDIR: orderdir}
        if minhours_min:
            params.update({MINHOURS: {MIN: minhours_min}})
        if minhours_max:
            params.update({MINHOURS: {MAX: minhours_max}})
        if maxhours_min:
            params.update({MAXHOURS: {MIN: maxhours_min}})
        if maxhours_max:
            params.update({MAXHOURS: {MAX: maxhours_max}})
        if rpi_min:
            params.update({RPI: {MIN: rpi_min}})
        if rpi_max:
            params.update({RPI: {MAX: rpi_max}})
        if hash_min:
            params.update({HASH: {MIN: hash_min}})
        if hash_max:
            params.update({HASH: {MAX: hash_max}})
        if hash_type:
            params.update({HASH: {TYPE: hash_type}})
        if price_min:
            params.update({PRICE: {MIN: price_min}})
        if price_max:
            params.update({PRICE: {MAX: price_max}})
        if region_type:
            params.update({REGION: {TYPE: region_type}})
        if region:
            params.update({REGION: {REGION: region}})

        return self._api_call(RIGS, params=params)

    def get_info_algo(self, algoname) -> dict:
        """
        GET /info/algos/[NAME]
        :return: Get statistics for an algo (suggested price, unit information, current rented hash/etc)

        """
        return self._api_call(ALGOS + algoname)

    def get_rig_mine(self, algo_type: str=None,
                     hashrate: bool=None
                     ) -> dict:
        """
        GET /rig/mine
        :param algo_type: Filter on algo -- see /info/algos
        :param hashrate: Calculate and display hashrates
        :return: List my rigs
        """
        params = {}
        if algo_type:
            params.update({TYPE: algo_type})
        if hashrate:
            params.update({HASHRATE: hashrate})

        return self._api_call(MINE, params=params)

    def get_rigs_by_id(self, rig_ids: list) -> dict:
        """
        GET /rig/[ID1];[ID2];...
        :param rig_ids:
        :return: Get 1 or more rigs by ID
        """
        ENDPOINT = RIGS
        for i in rig_ids:
            ENDPOINT += '{};'.format(i)

        return self._api_call(ENDPOINT)

    def get_rental(self, rental_type: str=None,
                   algo: str=None,
                   history: bool=None,
                   rig: int=None,
                   start: int=None,
                   limit: int=None
                   ) -> dict:
        """
        GET /rental
        :param rental_type: Type is one of [owner,renter] -- owner means rentals on your rigs, renter means rentals you purchased
        :param algo: Filter by algo, see /info/algos
        :param history: true = Show completed rentals, false = Active rentals
        :param rig: Show rentals related to a specific rig ID
        :param start: Start number (for pagination)
        :param limit: Limit number (for pagination)
        :return: Lists rentals
        """
        params = {}
        if rental_type:
            params.update({TYPE: rental_type})
        if algo:
            params.update({ALGO: algo})
        if history:
            params.update({HISTORY: history})
        if rig:
            params.update({RIG: rig})
        if start:
            params.update({START: start})
        if limit:
            params.update({LIMIT: limit})

        return self._api_call(RENTAL, params=params)

    def get_rentals_by_id(self, rental_ids: list
                          ) -> dict:
        """
        GET /rental/[ID1];[ID2];...
        :param rental_ids:
        :return: Get information on rentals by rental ID.
        """
        ENDPOINT = RENTAL
        for i in rental_ids:
            ENDPOINT += '{};'.format(i)

        return self._api_call(ENDPOINT)

    def put_rig(self, rigname: str,
                servername: str,
                status: str = str,
                btc_price: str = str,
                btc_autoprice: bool = None,
                btc_minimum: str = None,
                btc_modifier: str = None,
                ltc_enabled: bool = True,
                ltc_price: str = None,
                ltc_autoprice: bool = None,
                eth_enabled: bool = True,
                eth_price: str = None,
                eth_autoprice: bool = None,
                dash_enabled: bool = True,
                dash_price: str = None,
                dash_autoprice: bool = None,
                price_type: str = 'mh',
                minhours: float = None,
                maxhours: float = None,
                hash_amount: str = None,
                hash_type: str = 'mh') -> dict:
        """

        :param rigname: Name of rig
        :param servername: Server name -- see /info/servers
        :param status: "enabled","disabled"
        :param btc_price: Price of the rig per price.type per day (BTC)
        :param btc_autoprice: Enable BTC autopricing
        :param btc_minimum: Minimum price for the autopricer -- 0 to disable
        :param btc_modifier: Percent +/- to modify the autopricing (eg: +10 or -5.13 is 10% over or 5.13% under market rates, respectively), 0 to disable
        :param ltc_enabled:
        :param ltc_price: Price of the rig per price.type per day (LTC)
        :param ltc_autoprice: Enable LTC autopricing -- adjusts the LTC rate based on your BTC price and the GDAX market rate
        :param eth_enabled:
        :param eth_price: Price of the rig per price.type per day (ETH)
        :param eth_autoprice: Enable ETH autopricing -- adjusts the ETH rate based on your BTC price and the GDAX market rate
        :param dash_enabled:
        :param dash_price: 	Price of the rig per price.type per day (DASH)
        :param dash_autoprice: Enable DASH autopricing -- adjusts the DASH rate based on your BTC price and the BITTREX market rate
        :param price_type: The hash type of hash.. defaults to "mh" possible values: [hash,kh,mh,gh,th]
        :param minhours: Minimum number of hours available
        :param maxhours: Maximum number of hours available
        :param hash_amount: Amount of hash to advertise
        :param hash_type: The hash type of hash.. defaults to "mh" possible values: [hash,kh,mh,gh,th]
        """
        pass
