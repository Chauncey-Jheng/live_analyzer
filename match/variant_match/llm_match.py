import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket  # 使用websocket_client
answer = ""

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,one,two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain= ws.domain,question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        # print(content,end ="")
        global answer
        answer += content
        # print(1)
        if status == 2:
            ws.close()


def gen_params(appid, domain,question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 2048
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def main(appid, api_key, api_secret, Spark_url,domain, question):
    # print("星火:")
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


from dotenv import load_dotenv
import os
load_dotenv()
#以下密钥信息从控制台获取
appid = os.getenv('APPID')     #填写控制台中获取的 APPID 信息
api_secret = os.getenv('API_SECRET')   #填写控制台中获取的 APISecret 信息
api_key = os.getenv('API_KEY')    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
# domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本
domain = "generalv3" # v3.0版本
#云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"   # v3.0环境的地址

text =[]

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

import re
def variant_word_match(sentence):
    '''使用星火大模型对变体词进行识别匹配'''
    global answer


    mutli_prompt = """
    请识别出这段话中为了规避审查而表述的名词变体词，并给出对应原词。请注意，不要过度解读。你给出的反馈以以下形式给出：
    变体词：词1，原词：词1原词;
    变体词：词2，原词：词2原词;
    ……
    
    如果这段话中没有变体词，你只需返回“无”。
    
    要识别的话如下:\n
    """
    single_prompt = """
    请仅识别出这段话中第一个为了规避审查而表述的名词变体词，并给出对应原词。你给出的反馈以以下形式给出：
    (变体词：具体变体词，原词：具体原词)
    如果这段话中没有变体词，你只需返回“无”。
    
    要识别的话如下:\n
    """
    input = single_prompt + sentence
    text.clear
    question = checklen(getText("user",input))
    answer = ""
    main(appid,api_key,api_secret,Spark_url,domain,question)
    print(answer)
    pattern_variant = r'\(变体词：(.*?)，原词：(.*?)\)'
    matches = re.findall(pattern_variant, answer)
    if len(matches) == 0:
        return None
    match_case = matches[0]
    variant_word = match_case[0]
    origin_word = match_case[1]
    result = {"变体词":variant_word,"原词":origin_word}
    return result

def split_chinese_string(input_string, max_length=100):
    result = []
    current_chunk = ""
    current_length = 0

    for char in input_string:
        current_chunk += char
        current_length += len(char.encode('utf-8'))

        if current_length >= max_length:
            result.append(current_chunk)
            current_chunk = ""
            current_length = 0

    if current_chunk:
        result.append(current_chunk)

    return result

# if __name__ == '__main__':
# #     txt = """我家去了你车开不进来我操
# # 矿山突袭大金杯 暗区突围 突围·FAL上线 剩余时间 28:06 255 2 290 300 西北 330 23 msS 上场榜一：星 星雨晨风 108 禁止未成年消费 """
#     txt = "如果不是吃了我们的东西的话啊，他第二天就得去医院找白大褂了, 可见我们的产品具有显著的临某床意义, 对我们的心脑血某管都是很有好处的"
#     detected_variants = variant_word_match(txt)
#     print(detected_variants)