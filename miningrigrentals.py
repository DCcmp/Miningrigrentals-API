"""
Python3 API WRAPPER CLASS FOR https://miningrigrentals,com
"""
import hmac
import hashlib
import time
import requests

__author__ = "DJC @ https://coinminingpool.org"


api_key = 'x'  # YOUR APIKEY
api_secret = 'x'  # YOUR APISECRET

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

    def _build_sign_string(self, method):
        string = '{}{}{}'.format(self.key, self.nonce, method)
        return hmac.new(key=self.secret.encode(),
                        msg=string.encode(),
                        digestmod=hashlib.sha1).hexdigest()

    def _build_headers(self, signature):
        return {XAPISIGN: signature,
                XAPIKEY: api_key,
                XAPINONCE: str(self.nonce)}

    def _api_call(self, endpoint, params=None, request=None):
        """
        BASE FUNCTION FOR MAKING API CALLS TO MRR

        :type endpoint: str
        :type params: dict
        :type request: str
        :return: JSON response
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

        return request(url=url, headers=headers, params=params).json()

    def whoami(self):
        """
        GET /whoami
        """
        return self._api_call(WHOAMI)

    def get_algos(self):
        """
        GET /info/algos
        """
        return self._api_call(ALGOS)

    def get_servers(self):
        """
        GET /info/servers
        """
        return self._api_call(SERVERS)

    def get_algo(self, algoname):
        """
        GET /info/algos/[NAME]
        """
        return self._api_call(ALGOS + algoname)

    def get_rig(self, algo_type, search_filter=None):
        """
        GET /rig
        """
        params = {TYPE: algo_type}
        if search_filter:
            params.update(search_filter)
        return self._api_call(RIGS, params=params)

    def get_rig_mine(self, algo_type=None, hashrate=None):
        """
        GET /rig/mine
        """
        params = {}
        if algo_type:
            params.update({TYPE: algo_type})
        if hashrate:
            params.update({HASHRATE: hashrate})

        return self._api_call(MINE, params=params)

    def get_rigs_by_id(self, rig_ids):
        """
        GET /rig/[ID1];[ID2];...
        """
        ENDPOINT = RIGS
        for i in rig_ids:
            ENDPOINT += '{};'.format(i)

        return self._api_call(ENDPOINT)

    def get_rental(self, algo=None, history=None, rig=None, start=None, limit=None):
        """
        GET /rental
        """
        params = {TYPE: 'renter'}

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

    def get_rentals_by_id(self, rig_ids):
        """
        GET /rental/[ID1];[ID2];...
        """
        ENDPOINT = RIGS
        for i in rig_ids:
            ENDPOINT += '{};'.format(i)

        return self._api_call(ENDPOINT)