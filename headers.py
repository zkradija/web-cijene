import requests
import config_test
from fake_useragent import UserAgent

def headers(url,indProxy):
    ua = UserAgent()
    if indProxy == 0:
        s = requests.Session()
        headers_str = {
            'User-Agent': ua,
            'Accept-Encoding': '*',
            'Connection': 'keep-alive'
            }
        response = s.get(url, headers=headers_str)
        return response.text
    if indProxy == 1:
        response = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': config_test.scrapeops_api_key,
            'url': url, 
        },
        )
    return response.text