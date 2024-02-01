# -*- encoding: utf-8 -*-

import hashlib
import time
import urllib.parse
from typing import Union, Dict, Any
import requests
import re
import json
import execjs
import urllib.request
from crawl_utils import trace_error_decorator

no_proxy_handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(no_proxy_handler)


@trace_error_decorator
def get_douyin_live_list(url: str, cookies: Union[str, None] = None) -> Dict[str, Any]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://douyin.com/',
        'Cookie': 'ttwid=1%7C19g7ScRbfMB6eSqvQTGHSMao23ZymnWfC_-ba28HLiE%7C1683779600%7C96c67d19b20321e77c0cd1b653c3c555d330330ab8c4727d666b97101e89ac64'
    }
    if cookies:
        headers['Cookie'] = cookies

    # 使用更底层的urllib内置库，防止开启代理时导致的抖音录制SSL 443报错
    req = urllib.request.Request(url, headers=headers)
    response = opener.open(req, timeout=15)
    html_str = response.read().decode('utf-8')
    print(html_str)
    pattern = r'https://live\.douyin\.com/\d+'
    matches = re.findall(pattern, html_str)
    for match in matches:
        print(match)

get_douyin_live_list(r"https://www.douyin.com/search/vc?source=switch_tab&type=live")