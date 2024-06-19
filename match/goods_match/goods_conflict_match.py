# 从数据库中读取特定类别的商品列表，形成一个二元组列表，（商品名，商品介绍）
# 如果商品出现在二元组列表的商品名中，那么就将直播文本内容与对应的商品介绍进行矛盾性检测

from dao.dao import DAO
dao = DAO()

# 构建不同的商品类别的商品列表
保健品 = dao.get_保健品()
保健品字段名 = dao.get_字段名("保健品")
保健品_merged = []
for i in 保健品:
    good_name = i[保健品字段名.index("产品名称")]
    good_content = ''
    for j in 保健品字段名:
        if j == "保健功能":
            good_content += j + ":" + i[保健品字段名.index(j)] + ". "
    good_turple = (good_name, good_content)
    保健品_merged.append(good_turple)


国产化妆品 = dao.get_国产化妆品()
国产化妆品字段名 = dao.get_字段名("国产化妆品")
进口化妆品 = dao.get_进口化妆品()
进口化妆品字段名 = dao.get_字段名("进口化妆品")
化妆品_merged = []
for i in 国产化妆品:
    good_name = i[国产化妆品字段名.index("产品名称中文")]
    good_content = ''
    for j in 国产化妆品字段名:
        if j == "产品类别":
            good_content += j + ":" + i[国产化妆品字段名.index(j)] + ". "
        if j == "产品性状":
            good_content += j + ":" + i[国产化妆品字段名.index(j)] + ". "
        if j == "使用部位":
            good_content += j + ":" + i[国产化妆品字段名.index(j)] + ". "
        if j == "产品功效":
            good_content += j + ":" + i[国产化妆品字段名.index(j)] + ". "        
        if j == "状态":
            good_content += j + ":" + i[国产化妆品字段名.index(j)] + ". "    
    good_turple = (good_name, good_content)    
    化妆品_merged.append(good_turple)

for i in 进口化妆品:
    good_name = i[进口化妆品字段名.index("产品名称中文")]
    good_content = ''
    for j in 进口化妆品字段名:
        if j == "产品类别":
            good_content += j + ":" + i[进口化妆品字段名.index(j)] + ". "
        if j == "产品性状":
            good_content += j + ":" + i[进口化妆品字段名.index(j)] + ". "
        if j == "使用部位":
            good_content += j + ":" + i[进口化妆品字段名.index(j)] + ". "
        if j == "产品功效":
            good_content += j + ":" + i[进口化妆品字段名.index(j)] + ". "        
        if j == "状态":
            good_content += j + ":" + i[进口化妆品字段名.index(j)] + ". "   
    good_turple = (good_name, good_content)       
    化妆品_merged.append(good_turple)

国产药品 = dao.get_国产药品()
国产药品字段名 = dao.get_字段名("国产药品")
进口药品 = dao.get_进口药品()
进口药品字段名 = dao.get_字段名("进口药品")
药品_merged = []
for i in 国产药品:
    good_name = i[国产药品字段名.index("产品名称")]
    good_content = ''
    for j in 国产药品字段名:
        if j == "剂型":
            good_content += j + ":" + i[国产药品字段名.index(j)] + ". "
        if j == "规格":
            good_content += j + ":" + i[国产药品字段名.index(j)] + ". "    
    good_turple = (good_name, good_content)         
    药品_merged.append(good_turple)
for i in 进口药品:
    good_name = i[进口药品字段名.index("商品名（中文）")]
    if good_name == "":
        continue
    good_content = ''
    for j in 进口药品字段名:
        if j == "产品类别":
            good_content += j + ":" + i[进口药品字段名.index(j)] + ". "
        if j == "剂型（中文）":
            good_content += j + ":" + i[进口药品字段名.index(j)] + ". "
        if j == "规格（中文）":
            good_content += j + ":" + i[进口药品字段名.index(j)] + ". "
        if j == "包装规格（中文）":
            good_content += j + ":" + i[进口药品字段名.index(j)] + ". "  
    good_turple = (good_name, good_content)             
    药品_merged.append(good_turple)

国产医疗器械注册 = dao.get_国产医疗器械注册()
国产医疗器械注册字段名 = dao.get_字段名("国产医疗器械注册")
国产医疗器械备案 = dao.get_国产医疗器械备案()
国产医疗器械备案字段名 = dao.get_字段名("国产医疗器械备案")
进口医疗器械注册 = dao.get_进口医疗器械注册()
进口医疗器械注册字段名 = dao.get_字段名("进口医疗器械注册")
进口医疗器械备案 = dao.get_进口医疗器械备案()
进口医疗器械备案字段名 = dao.get_字段名("进口医疗器械备案")
医疗器械_merged = []
for i in 国产医疗器械注册:
    good_name = i[国产医疗器械注册字段名.index("产品名称")]
    good_content = ''
    for j in 国产医疗器械注册字段名:
        if j == "管理类别":
            good_content += j + ":" + i[国产医疗器械注册字段名.index(j)] + ". "
        if j == "型号规格":
            good_content += j + ":" + i[国产医疗器械注册字段名.index(j)] + ". "      
        if j == "结构及组成/主要组成成分":
            good_content += j + ":" + i[国产医疗器械注册字段名.index(j)] + ". "
        if j == "适用范围/预期用途":
            good_content += j + ":" + i[国产医疗器械注册字段名.index(j)] + ". "  
    good_turple = (good_name, good_content)  
    医疗器械_merged.append(good_turple)
for i in 国产医疗器械备案:
    good_name = i[国产医疗器械备案字段名.index("产品名称/产品分类名称")]
    good_content = ''
    for j in 国产医疗器械备案字段名:
        if j == "型号规格/包装规格":
            good_content += j + ":" + i[国产医疗器械备案字段名.index(j)] + ". "
        if j == "产品描述/主要组成成分":
            good_content += j + ":" + i[国产医疗器械备案字段名.index(j)] + ". "      
        if j == "预期用途":
            good_content += j + ":" + i[国产医疗器械备案字段名.index(j)] + ". "   
    good_turple = (good_name, good_content)  
    医疗器械_merged.append(good_turple)
for i in 进口医疗器械注册:
    good_name = i[进口医疗器械注册字段名.index("产品名称")]
    good_content = ''
    for j in 进口医疗器械注册字段名:
        if j == "管理类别":
            good_content += j + ":" + i[进口医疗器械注册字段名.index(j)] + ". "
        if j == "型号规格":
            good_content += j + ":" + i[进口医疗器械注册字段名.index(j)] + ". "      
        if j == "结构及组成/主要组成成分":
            good_content += j + ":" + i[进口医疗器械注册字段名.index(j)] + ". "
        if j == "适用范围/预期用途":
            good_content += j + ":" + i[进口医疗器械注册字段名.index(j)] + ". "    
    good_turple = (good_name, good_content)  
    医疗器械_merged.append(good_turple)
for i in 进口医疗器械备案:
    good_name = i[进口医疗器械备案字段名.index("产品名称/产品分类名称")]
    good_content = ''
    for j in 进口医疗器械备案字段名:
        if j == "型号规格/包装规格":
            good_content += j + ":" + i[进口医疗器械备案字段名.index(j)] + ". "
        if j == "产品描述/主要组成成分":
            good_content += j + ":" + i[进口医疗器械备案字段名.index(j)] + ". "      
        if j == "预期用途":
            good_content += j + ":" + i[进口医疗器械备案字段名.index(j)] + ". "   
    good_turple = (good_name, good_content)  
    医疗器械_merged.append(good_turple)

dao.close()

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
def conflict_match_with_spark(sentence,goods_content):
    '''使用星火大模型对直播内容文本以及对应的商品内容描述进行矛盾性检测'''
    global answer
    prompt = """
    接下来将给出一段直播内容文本以及对应的商品内容描述，请对两者进行矛盾性检测。如果检测发现没有矛盾，不用解释，仅需回复None
    
    直播内容文本如下:\n
    """
    input = prompt + sentence + "商品内容描述如下:\n" + goods_content
    text.clear
    question = checklen(getText("user",input))
    answer = ""
    main(appid,api_key,api_secret,Spark_url,domain,question)
    print(answer)
    if "None" in answer:
        return None
    return answer


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


llama_base_url = os.getenv('LLAMA_BASE_URL')     #填写控制台中获取的base_url 信息
llama_api_key = os.getenv('LLAMA_API_KEY')    #填写控制台中获取的 APIKey 信息

from openai import OpenAI
client = OpenAI(
    base_url = llama_base_url, # "http://<Your api-server IP>:port"
    api_key = llama_api_key
)

def conflict_match_with_llama(sentence,goods_content):

    # prompt = """
    # 接下来将给出一段直播内容文本以及对应的商品内容描述，请对两者进行矛盾性检测。如果检测发现没有矛盾，不用解释，仅需回复None
    
    # 要识别的内容文本如下:\n
    # """
    prompt = ""
    # system_prompt = "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."
    system_prompt = "你是一个文本内容矛盾检测器。接下来将给出一段直播内容文本以及对应的商品内容描述，请对两者进行矛盾性检测。如果检测发现没有矛盾，不用解释，仅需回复None。直播内容文本如下:\n"
    input = prompt + sentence + "商品内容描述如下:\n" + goods_content
    split_chs_str = split_chinese_string(input_string=input)
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": split_chs_str[0]}
        ]
    )
    # print(completion.choices[0].message)
    result = completion.choices[0].message.content.strip()

    if "None" in result:
        return None
    return result


def match_goods_conflict_match(str):
    '''检测直播文本内容中是否出现在数据库中的商品，如果出现，则对其进行矛盾性检测'''
    import configparser
    config_file = './config.ini'
    encoding = 'utf-8-sig'
    config = configparser.RawConfigParser()
    config.read(config_file, encoding=encoding)
    llm_name = config.get('商品内容匹配设置','大语言模型采用')
    if llm_name == "llama":
        conflict_match = conflict_match_with_llama
    elif llm_name == "spark":
        conflict_match = conflict_match_with_spark

    result = {}
    result["type"] = 0
    result['content'] = None

    for i in 保健品_merged:
        if i[0] in str:
            ret = conflict_match(str,i[1])
            if ret != None:
                result["type"] = 4
                result["content"] = {"商品名称":i[0],"商品类别":"保健品","矛盾":ret} 
                return result
            else:
                break

    for i in 化妆品_merged:
        if i[0] in str:
            ret = conflict_match(str,i[1])
            if ret != None:
                result["type"] = 4
                result["content"] = {"商品名称":i[0],"商品类别":"化妆品","矛盾":ret} 
                return result
            else:
                break
            
    for i in 药品_merged:
        if i[0] in str:
            ret = conflict_match(str,i[1])
            if ret != None:
                result["type"] = 4
                result["content"] = {"商品名称":i[0],"商品类别":"药品","矛盾":ret} 
                return result
            else:
                break

    for i in 医疗器械_merged:
        if i[0] in str:
            ret = conflict_match(str,i[1])
            if ret != None:
                result["type"] = 4
                result["content"] = {"商品名称":i[0],"商品类别":"医疗器械","矛盾":ret} 
                return result    
            else:
                break      

    return result