import requests
import config_test

import random

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) '
        'AppleWebKit/605.1.15 (KHTML, like Gecko) '
        'Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
]


def fake_headers(url, indProxy, headers_str=None, indVerify=True):
    
    # 0 - my fake headers (fake user agents)
    # 1 - fake headers via proxy

    session = requests.Session()

    if indProxy == 0:
        if headers_str is None:
            headers_str = {
                'User-Agent': random.choice(user_agent_list),
                'Accept-Encoding': '*',
                'Connection': 'keep-alive'
                }
        # print(headers_str)
        response = session.get(url, headers=headers_str, verify=indVerify)
        return response.text
    if indProxy == 1:
        response = session.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': config_test.scrapeops_api_key,
            'url': url,
            'render_js': 'true', 
            'residential': 'true', 
            'country': 'hr'
        },
        )
    return response.text

