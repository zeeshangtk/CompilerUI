import json
import logging

import requests

from .apps import CompilerConfig

logger = logging.getLogger('django')

class CompilerService():

    def __init__(self, rest_client):
        self.rest_client = rest_client

    def run_code(self, code, type):
        logger.info("Executing code"+str(code))
        data = {'code': code, 'type': type}
        response = self.rest_client.post_data(CompilerConfig.compiler_url,
                                              json.dumps(data))
        logger.info("output of the executed code is "+str(response.content)+"--"+str(response.status_code))
        if (response.status_code != 200):
            logger.error("Got a error while executing the code "+str(code))
            raise RuntimeError("Error while executing the program " + str(response.content))

        return response.content


class RestClient(object):
    def __init__(self):
        self.requests = requests

    def post_data(self,url, json_data) :
        try:
            headers = {'Content-type': 'application/json'}
            return requests.post(url=url, data=json_data, headers=headers,timeout=2)
        except Exception as e:
            logger.error("Error while performing post request"+str(e))
            raise RuntimeError("Error"+str(e))