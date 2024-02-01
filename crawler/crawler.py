# -*- encoding: utf-8 -*-

import random
import os
import sys
import urllib.parse
import urllib.request
import configparser
import subprocess
import threading
import datetime
import time
import json
import re
import signal
from typing import Union, Dict, Any

if __name__ == "__main__":
    from web_rid import (
        get_live_room_id,
        get_sec_user_id
    )
    from crawl_utils import (
        logger, check_md5,
        trace_error_decorator
    )
else:
    from crawler.web_rid import (
        get_live_room_id,
        get_sec_user_id
    )
    from crawler.crawl_utils import (
        logger, check_md5,
        trace_error_decorator
    )

# --------------------------全局变量-------------------------------------
recording = set()
unrecording = set()
warning_count = 0
monitoring = 0
runing_list = []
url_tuples_list = []
text_no_repeat_url = []
create_var = locals()
name_list = []
live_list = []
not_record_list = []
start_display_time = datetime.datetime.now()
global_proxy = False
recording_time_list = {}
config_file = './crawler/config/config.ini'
url_config_file = './crawler/config/URL_config.ini'
encoding = 'utf-8-sig'
rstr = r"[\/\\\:\*\?\"\<\>\|&u]"
ffmpeg_path = "ffmpeg"  # ffmpeg文件路径
default_path = os.getcwd()

options = {"是": True, "否": False}
video_save_path = ""
video_save_type = "mp4"
video_quality = "标清"
max_request = 3
semaphore = threading.Semaphore(max_request)
delay_default = 120
local_delay_default = 0
loop_time = False
split_video_by_time = False
split_time = str(3600)
tsconvert_to_mp4 = False
tsconvert_to_m4a = False
delete_origin_file = False
create_time_file = False

dy_cookie = ''
max_record_time = 30

no_proxy_handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(no_proxy_handler)

# --------------------------用到的函数-------------------------------------
def signal_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)

def update_file(file, old_str, new_str):
    # TODO: 更新文件操作
    file_data = ""
    with open(file, "r", encoding="utf-8-sig") as f:
        for text_line in f:
            if old_str in text_line:
                text_line = text_line.replace(old_str, new_str)
            file_data += text_line
    with open(file, "w", encoding="utf-8-sig") as f:
        f.write(file_data)

def transform_int_to_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}"

def converts_mp4(address):
    if tsconvert_to_mp4:
        _output = subprocess.check_output([
            "ffmpeg", "-i", address,
            "-c:v", "copy",
            "-c:a", "copy",
            "-f", "mp4", address.split('.')[0] + ".mp4",
        ], stderr=subprocess.STDOUT)
        if delete_origin_file:
            time.sleep(1)
            if os.path.exists(address):
                os.remove(address)


def converts_m4a(address):
    if tsconvert_to_m4a:
        _output = subprocess.check_output([
            "ffmpeg", "-i", address,
            "-n", "-vn",
            "-c:a", "aac", "-bsf:a", "aac_adtstoasc", "-ab", "320k",
            address.split('.')[0] + ".m4a",
        ], stderr=subprocess.STDOUT)
        if delete_origin_file:
            time.sleep(1)
            if os.path.exists(address):
                os.remove(address)


def create_ass_file(filegroup):
    # TODO:  录制时生成ass格式的字幕文件
    anchor_name = filegroup[0]
    ass_filename = filegroup[1]
    index_time = -1
    finish = 0
    today = datetime.datetime.now()
    re_datatime = today.strftime('%Y-%m-%d %H:%M:%S')

    while True:
        index_time += 1
        txt = str(index_time) + "\n" + transform_int_to_time(index_time) + ',000 --> ' + transform_int_to_time(
            index_time + 1) + ',000' + "\n" + str(re_datatime) + "\n"

        with open(ass_filename + ".ass", 'a', encoding='utf8') as f:
            f.write(txt)

        if anchor_name not in recording:
            finish += 1
            offset = datetime.timedelta(seconds=1)
            # 获取修改后的时间并格式化
            re_datatime = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
            today = today + offset
        else:
            time.sleep(1)
            today = datetime.datetime.now()
            re_datatime = today.strftime('%Y-%m-%d %H:%M:%S')

        if finish > 15:
            break


def change_max_connect():
    global max_request
    global warning_count
    # 动态控制连接次数
    preset = max_request
    # 记录当前时间
    start_time = time.time()

    while True:
        time.sleep(5)
        if 10 <= warning_count <= 20:
            if preset > 5:
                max_request = 5
            else:
                max_request //= 2  # 将max_request除以2（向下取整）
                if max_request > 0:  # 如果得到的结果大于0，则直接取该结果
                    max_request = preset
                else:  # 否则将其设置为1
                    preset = 1

            print("同一时间访问网络的线程数动态改为", max_request)
            warning_count = 0
            time.sleep(5)

        elif 20 < warning_count:
            max_request = 1
            print("同一时间访问网络的线程数动态改为", max_request)
            warning_count = 0
            time.sleep(10)

        elif warning_count < 10 and time.time() - start_time > 60:
            max_request = preset
            warning_count = 0
            start_time = time.time()
            print("同一时间访问网络的线程数动态改为", max_request)

@trace_error_decorator
def get_douyin_stream_data(url: str, cookies: Union[str, None] = None) -> Dict[str, Any]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://live.douyin.com/',
        'Cookie': 'ttwid=1%7CB1qls3GdnZhUov9o2NxOMxxYS2ff6OSvEWbv0ytbES4%7C1680522049%7C280d802d6d478e3e78d0c807f7c487e7ffec0ae4e5fdd6a0fe74c3c6af149511; my_rd=1; passport_csrf_token=3ab34460fa656183fccfb904b16ff742; passport_csrf_token_default=3ab34460fa656183fccfb904b16ff742; d_ticket=9f562383ac0547d0b561904513229d76c9c21; n_mh=hvnJEQ4Q5eiH74-84kTFUyv4VK8xtSrpRZG1AhCeFNI; store-region=cn-fj; store-region-src=uid; LOGIN_STATUS=1; __security_server_data_status=1; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; pwa2=%223%7C0%7C3%7C0%22; download_guide=%223%2F20230729%2F0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.6%7D; strategyABtestKey=%221690824679.923%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1691443863751%2C%22type%22%3Anull%7D; home_can_add_dy_2_desktop=%221%22; __live_version__=%221.1.1.2169%22; device_web_cpu_core=8; device_web_memory_size=8; xgplayer_user_id=346045893336; csrf_session_id=2e00356b5cd8544d17a0e66484946f28; odin_tt=724eb4dd23bc6ffaed9a1571ac4c757ef597768a70c75fef695b95845b7ffcd8b1524278c2ac31c2587996d058e03414595f0a4e856c53bd0d5e5f56dc6d82e24004dc77773e6b83ced6f80f1bb70627; __ac_nonce=064caded4009deafd8b89; __ac_signature=_02B4Z6wo00f01HLUuwwAAIDBh6tRkVLvBQBy9L-AAHiHf7; ttcid=2e9619ebbb8449eaa3d5a42d8ce88ec835; webcast_leading_last_show_time=1691016922379; webcast_leading_total_show_times=1; webcast_local_quality=sd; live_can_add_dy_2_desktop=%221%22; msToken=1JDHnVPw_9yTvzIrwb7cQj8dCMNOoesXbA_IooV8cezcOdpe4pzusZE7NB7tZn9TBXPr0ylxmv-KMs5rqbNUBHP4P7VBFUu0ZAht_BEylqrLpzgt3y5ne_38hXDOX8o=; msToken=jV_yeN1IQKUd9PlNtpL7k5vthGKcHo0dEh_QPUQhr8G3cuYv-Jbb4NnIxGDmhVOkZOCSihNpA2kvYtHiTW25XNNX_yrsv5FN8O6zm3qmCIXcEe0LywLn7oBO2gITEeg=; tt_scid=mYfqpfbDjqXrIGJuQ7q-DlQJfUSG51qG.KUdzztuGP83OjuVLXnQHjsz-BRHRJu4e986'
    }
    if cookies:
        headers['Cookie'] = cookies

    try:
        # 使用更底层的urllib内置库，防止开启代理时导致的抖音录制SSL 443报错
        req = urllib.request.Request(url, headers=headers)
        response = opener.open(req, timeout=15)
        html_str = response.read().decode('utf-8')
        match_json_str = re.search(r'(\{\\"state\\":.*?)]\\n"]\)', html_str)
        if not match_json_str:
            match_json_str = re.search(r'(\{\\"common\\":.*?)]\\n"]\)</script><div hidden', html_str)
        json_str = match_json_str.group(1)
        cleaned_string = json_str.replace('\\', '').replace(r'u0026', r'&')
        room_store = re.search('"roomStore":(.*?),"linkmicStore"', cleaned_string, re.S).group(1)
        anchor_name = re.search('"nickname":"(.*?)","avatar_thumb', room_store, re.S).group(1)
        room_store = room_store.split(',"has_commerce_goods"')[0] + '}}}'
        json_data = json.loads(room_store)['roomInfo']['room']
        json_data['anchor_name'] = anchor_name
        return json_data

    except Exception as e:
        print(f'失败地址：{url} 准备切换解析方法{e}')
        web_rid = re.match('https://live.douyin.com/(\d+)', url).group(1)
        headers['Cookie'] = 'sessionid=73d300f837f261eaa8ffc69d50162700'
        url2 = f'https://live.douyin.com/webcast/room/web/enter/?aid=6383&app_name=douyin_web&live_id=1&web_rid={web_rid}'
        req = urllib.request.Request(url2, headers=headers)
        response = opener.open(req, timeout=15)
        json_str = response.read().decode('utf-8')
        if json_str == "":
            return {}
        json_data = json.loads(json_str)['data']
        room_data = json_data['data'][0]
        room_data['anchor_name'] = json_data['user']['nickname']
        print("room_data")
        return room_data

@trace_error_decorator
def get_douyin_stream_url(json_data):
    # TODO: 获取抖音直播源地址
    global video_quality
    anchor_name = json_data.get('anchor_name', None)

    result = {
        "anchor_name": anchor_name,
        "is_live": False,
    }

    status = json_data.get("status", 4)  # 直播状态 2 是正在直播、4 是未开播

    if status == 2:
        stream_url = json_data['stream_url']
        flv_url_list = stream_url['flv_pull_url']
        m3u8_url_list = stream_url['hls_pull_url_map']

        # video_qualities = {
        #     "原画": "FULL_HD1",
        #     "蓝光": "FULL_HD1",
        #     "超清": "HD1",
        #     "高清": "SD1",
        #     "标清": "SD2",
        # }

        quality_list = list(m3u8_url_list.keys())
        while len(quality_list) < 4:
            quality_list.append(quality_list[-1])
        video_qualities = {"原画": 0, "蓝光": 0, "超清": 1, "高清": 2, "标清": 3}
        quality_index = video_qualities.get(video_quality)
        quality_key = quality_list[quality_index]
        m3u8_url = m3u8_url_list.get(quality_key)
        flv_url = flv_url_list.get(quality_key)

        result['m3u8_url'] = m3u8_url
        result['flv_url'] = flv_url
        result['is_live'] = True
        result['record_url'] = m3u8_url  # 使用 m3u8 链接进行录制

    return result

def start_record(url_tuple, count_variable, stop_signal:threading.Event):
    global warning_count
    global video_save_path
    global video_save_type
    global create_var
    global live_list
    global not_record_list
    global recording_time_list

    while not stop_signal.is_set():
        try:
            record_finished = False
            record_finished_2 = False
            run_once = False
            is_long_url = False
            no_error = True
            new_record_url = ''
            count_time = time.time()
            record_url = url_tuple[0]
            anchor_name = url_tuple[1]
            print(f"\r运行新线程,传入地址 {record_url}")

            while not stop_signal.is_set():
                try:
                    port_info = {}
                    if record_url.find("https://live.douyin.com/") > -1:
                        # 判断如果是浏览器长链接
                        with semaphore:
                            # 使用semaphore来控制同时访问资源的线程数量
                            json_data = get_douyin_stream_data(record_url, dy_cookie)
                            port_info = get_douyin_stream_url(json_data)
                    elif record_url.find("https://v.douyin.com/") > -1:
                        # 判断如果是app分享链接
                        is_long_url = True
                        room_id, sec_user_id = get_sec_user_id(record_url)
                        web_rid = get_live_room_id(room_id, sec_user_id)
                        if len(web_rid) == 0:
                            print('web_rid 获取失败，若多次失败请联系作者修复或者使用浏览器打开后的长链接')
                        new_record_url = "https://live.douyin.com/" + str(web_rid)
                        not_record_list.append(new_record_url)
                        with semaphore:
                            json_data = get_douyin_stream_data(new_record_url, dy_cookie)
                            port_info = get_douyin_stream_url(json_data)
                    if anchor_name:
                        anchor_split = anchor_name.split('主播:')
                        if len(anchor_split) > 1 and anchor_split[1].strip():
                            anchor_name = anchor_split[1].strip()
                        else:
                            anchor_name = port_info.get("anchor_name", '')
                    else:
                        anchor_name = port_info.get("anchor_name", '')

                    if anchor_name == '':
                        print(f'序号{count_variable} 网址内容获取失败,进行重试中...获取失败的地址是:{url_tuple}')
                        warning_count += 1
                    else:
                        anchor_name = re.sub(rstr, "_", anchor_name)  # 过滤不能作为文件名的字符，替换为下划线
                        record_name = f'序号{count_variable} {anchor_name}'

                        if anchor_name in recording:
                            print(f"新增的地址: {anchor_name} 已经存在,本条线程将会退出")
                            name_list.append(f'{record_url}|#{record_url}')
                            return

                        if url_tuple[1] == "" and run_once is False:
                            if is_long_url:
                                name_list.append(f'{record_url}|{new_record_url},主播: {anchor_name.strip()}')
                            else:
                                name_list.append(f'{record_url}|{record_url},主播: {anchor_name.strip()}')
                            run_once = True

                        if port_info['is_live'] is False:
                            print(f"{record_name} 等待直播... ")
                        else:
                            content = f"{record_name} 正在直播中..."
                            print(content)

                            real_url = port_info['record_url']
                            full_path = f'{default_path}/{anchor_name}'
                            if real_url != "":
                                live_list.append(anchor_name)
                                now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))

                                try:
                                    if len(video_save_path) > 0:
                                        if video_save_path[-1] != "/":
                                            video_save_path = video_save_path + "/"
                                    else:
                                        video_save_path = default_path + '/'

                                    video_save_path = video_save_path.replace("\\", "/")
                                    full_path = f'{video_save_path}{anchor_name}'
                                    if not os.path.exists(full_path):
                                        os.makedirs(full_path)
                                except Exception as e:
                                    logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")

                                if not os.path.exists(full_path):
                                    logger.warning(
                                        "错误信息: 保存路径不存在,不能生成录制.请避免把本程序放在c盘,桌面,下载文件夹,qq默认传输目录.请重新检查设置")

                                user_agent = ("Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 ("
                                              "KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile "
                                              "Safari/537.36")
                                ffmpeg_command = [
                                    ffmpeg_path, "-y",
                                    "-v", "verbose",
                                    "-rw_timeout", "30000000",  # 改为30s
                                    "-loglevel", "error",
                                    "-hide_banner",
                                    "-user_agent", user_agent,
                                    "-protocol_whitelist", "rtmp,crypto,file,http,https,tcp,tls,udp,rtp",
                                    "-thread_queue_size", "512",
                                    "-analyzeduration", "5000000",
                                    "-probesize", "10000000",
                                    "-fflags", "+discardcorrupt",
                                    "-i", real_url,
                                    "-bufsize", "9000k",  # 适当增加输入缓冲区大小
                                    "-sn", "-dn",
                                    "-reconnect_delay_max", "60",  # 适当增加最大重连延迟
                                    "-reconnect_streamed", "-reconnect_at_eof",
                                    "-max_muxing_queue_size", "128",  # 适当增加输出复用器的最大队列大小
                                    "-correct_ts_overflow", "1",
                                    # "-t", "{time}".format(time=max_record_time),
                                ]

                                recording.add(record_name)
                                start_record_time = datetime.datetime.now()
                                recording_time_list[record_name] = start_record_time
                                rec_info = f"\r{anchor_name} 录制视频中: {full_path}"
                                filename_short = full_path + '/' + anchor_name + '_' + now

                                if video_save_type == "FLV":
                                    filename = anchor_name + '_' + now + '.flv'
                                    print(f'{rec_info}/{filename}')

                                    if create_time_file:
                                        filename_gruop = [anchor_name, filename_short]
                                        create_var[str(filename_short)] = threading.Thread(target=create_ass_file,
                                                                                           args=(filename_gruop,))
                                        create_var[str(filename_short)].daemon = True
                                        create_var[str(filename_short)].start()

                                    try:
                                        flv_url = port_info.get('flv_url', None)
                                        if flv_url:
                                            _filepath, _ = urllib.request.urlretrieve(real_url,
                                                                                      full_path + '/' + filename)

                                        else:
                                            raise Exception('该直播无flv直播流，请切换视频保存类型')

                                    except Exception as e:
                                        logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
                                        warning_count += 1
                                        no_error = False

                                elif video_save_type == "MKV":
                                    filename = anchor_name + '_' + now + ".mkv"
                                    print(f'{rec_info}/{filename}')
                                    save_file_path = full_path + '/' + filename

                                    try:
                                        if split_video_by_time:
                                            now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                                            save_file_path = f"{full_path}/{anchor_name}_{now}_%03d.mkv"
                                            command = [
                                                "-c:v", "copy",
                                                "-c:a", "aac",
                                                "-map", "0",
                                                "-f", "segment",
                                                "-segment_time", split_time,
                                                "-segment_format", "matroska",
                                                "-reset_timestamps", "1",
                                                save_file_path,
                                            ]

                                        else:
                                            if create_time_file:
                                                filename_gruop = [anchor_name, filename_short]
                                                create_var[str(filename_short)] = threading.Thread(
                                                    target=create_ass_file,
                                                    args=(filename_gruop,))
                                                create_var[str(filename_short)].daemon = True
                                                create_var[str(filename_short)].start()

                                            command = [
                                                "-map", "0",
                                                "-c:v", "copy",
                                                "-c:a", "copy",
                                                "-f", "matroska",
                                                "{path}".format(path=save_file_path),
                                            ]
                                        ffmpeg_command.extend(command)

                                        _output = subprocess.check_output(ffmpeg_command, stderr=subprocess.STDOUT)

                                    except subprocess.CalledProcessError as e:
                                        logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
                                        warning_count += 1
                                        no_error = False

                                elif video_save_type == "MP4":
                                    filename = anchor_name + '_' + now + ".mp4"
                                    print(f'{rec_info}/{filename}')
                                    save_file_path = full_path + '/' + filename

                                    try:
                                        if split_video_by_time:
                                            now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                                            save_file_path = f"{full_path}/{anchor_name}_{now}_%03d.mp4"
                                            print(save_file_path)
                                            command = [
                                                "-c:v", "copy",
                                                "-c:a", "aac",
                                                "-map", "0",
                                                "-f", "segment",
                                                "-segment_time", split_time,
                                                "-segment_format", "mp4",
                                                "-movflags", "+faststart",
                                                "-reset_timestamps", "1",
                                                save_file_path,
                                            ]
                                        else:
                                            if create_time_file:
                                                filename_gruop = [anchor_name, filename_short]
                                                create_var[str(filename_short)] = threading.Thread(
                                                    target=create_ass_file,
                                                    args=(filename_gruop,))
                                                create_var[str(filename_short)].daemon = True
                                                create_var[str(filename_short)].start()

                                            command = [
                                                "-map", "0",
                                                "-c:v", "copy",
                                                "-c:a", "copy",
                                                "-f", "mp4",
                                                "{path}".format(path=save_file_path),
                                            ]

                                        ffmpeg_command.extend(command)
                                        _output = subprocess.check_output(ffmpeg_command, stderr=subprocess.STDOUT)

                                    except subprocess.CalledProcessError as e:
                                        logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
                                        warning_count += 1
                                        no_error = False

                                elif video_save_type == "MKV音频":
                                    filename = anchor_name + '_' + now + ".mkv"
                                    print(f'{rec_info}/{filename}')
                                    save_file_path = full_path + '/' + filename

                                    try:
                                        command = [
                                            "-map", "0:a",
                                            "-c:a", "copy",
                                            "-f", "matroska",
                                            "{path}".format(path=save_file_path),
                                        ]
                                        ffmpeg_command.extend(command)
                                        _output = subprocess.check_output(ffmpeg_command, stderr=subprocess.STDOUT)

                                        if tsconvert_to_m4a:
                                            threading.Thread(target=converts_m4a, args=(save_file_path,)).start()
                                    except subprocess.CalledProcessError as e:
                                        logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
                                        warning_count += 1
                                        no_error = False

                                elif video_save_type == "TS音频":
                                    filename = anchor_name + '_' + now + ".ts"
                                    print(f'{rec_info}/{filename}')
                                    save_file_path = full_path + '/' + filename

                                    try:
                                        command = [
                                            "-map", "0:a",
                                            "-c:a", "copy",
                                            "-f", "mpegts",
                                            "{path}".format(path=save_file_path),
                                        ]
                                        ffmpeg_command.extend(command)
                                        _output = subprocess.check_output(ffmpeg_command, stderr=subprocess.STDOUT)

                                        if tsconvert_to_m4a:
                                            threading.Thread(target=converts_m4a, args=(save_file_path,)).start()
                                    except subprocess.CalledProcessError as e:
                                        logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
                                        warning_count += 1
                                        no_error = False

                                else:
                                    if split_video_by_time:
                                        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                                        filename = anchor_name + '_' + now + ".ts"
                                        print(f'{rec_info}/{filename}')

                                        try:
                                            if tsconvert_to_mp4:
                                                save_path_name = f"{full_path}/{anchor_name}_{now}_%03d.mp4"
                                                audio_code = 'aac'
                                                segment_format = 'mp4'
                                            else:
                                                save_path_name = f"{full_path}/{anchor_name}_{now}_%03d.ts"
                                                audio_code = 'copy'
                                                segment_format = 'mpegts'

                                            command = [
                                                "-c:v", "copy",
                                                "-c:a", audio_code,
                                                "-map", "0",
                                                "-f", "segment",
                                                "-segment_time", split_time,
                                                "-segment_format", segment_format,
                                                "-reset_timestamps", "1",
                                                save_path_name,
                                            ]

                                            ffmpeg_command.extend(command)
                                            _output = subprocess.check_output(ffmpeg_command,
                                                                              stderr=subprocess.STDOUT)

                                        except subprocess.CalledProcessError as e:
                                            logger.warning(
                                                f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
                                            warning_count += 1
                                            no_error = False

                                    else:
                                        filename = anchor_name + '_' + now + ".ts"

                                        print(f'{rec_info}/{filename}')
                                        save_file_path = full_path + '/' + filename

                                        if create_time_file:
                                            filename_gruop = [anchor_name, filename_short]
                                            create_var[str(filename_short)] = threading.Thread(target=create_ass_file,
                                                                                               args=(filename_gruop,))
                                            create_var[str(filename_short)].daemon = True
                                            create_var[str(filename_short)].start()

                                        try:
                                            command = [
                                                "-c:v", "copy",
                                                "-c:a", "copy",
                                                "-map", "0",
                                                "-f", "mpegts",
                                                "{path}".format(path=save_file_path),
                                            ]

                                            ffmpeg_command.extend(command)
                                            _output = subprocess.check_output(ffmpeg_command, stderr=subprocess.STDOUT)

                                            if tsconvert_to_mp4:
                                                threading.Thread(target=converts_mp4, args=(save_file_path,)).start()
                                            if tsconvert_to_m4a:
                                                threading.Thread(target=converts_m4a, args=(save_file_path,)).start()

                                        except subprocess.CalledProcessError as e:
                                            logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
                                            warning_count += 1
                                            no_error = False

                                record_finished = True
                                record_finished_2 = True
                                count_time = time.time()

                            if record_finished_2:
                                if record_name in recording:
                                    recording.remove(record_name)
                                if anchor_name in unrecording:
                                    unrecording.add(anchor_name)

                                if no_error:
                                    print(f"\n{anchor_name} {time.strftime('%Y-%m-%d %H:%M:%S')} 直播录制完成\n")
                                else:
                                    print(
                                        f"\n{anchor_name} {time.strftime('%Y-%m-%d %H:%M:%S')} 直播录制出错,请检查网络\n")

                                record_finished_2 = False

                except Exception as e:
                    logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
                    warning_count += 1

                num = random.randint(-5, 5) + delay_default  # 生成-5到5的随机数，加上delay_default
                if num < 0:  # 如果得到的结果小于0，则将其设置为0
                    num = 0
                x = num

                # 如果出错太多,就加秒数
                if warning_count > 100:
                    x = x + 60
                    print("瞬时错误太多,延迟加60秒")

                # 这里是.如果录制结束后,循环时间会暂时变成30s后检测一遍. 这样一定程度上防止主播卡顿造成少录
                # 当30秒过后检测一遍后. 会回归正常设置的循环秒数
                if record_finished:
                    count_time_end = time.time() - count_time
                    if count_time_end < 60:
                        x = 30
                    record_finished = False

                else:
                    x = num

                # 这里是正常循环
                while x:
                    x = x - 1
                    if loop_time:
                        print(f'\r{anchor_name}循环等待{x}秒 ', end="")
                    time.sleep(1)
                if loop_time:
                    print('\r检测直播间中...', end="")
        except Exception as e:
            logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")
            warning_count += 1
            time.sleep(2)

def check_ffmpeg():
    """检测是否存在ffmpeg"""
    ffmpeg_file_check = subprocess.getoutput("ffmpeg")
    if ffmpeg_file_check.find("run") > -1:
        # print("ffmpeg存在")
        pass
    else:
        print("重要提示:")
        print("检测到ffmpeg不存在,请将ffmpeg设置为环境变量,没有ffmpeg将无法录制")
        sys.exit(0)

def read_config_value(config, section, option, default_value):
    try:
        config.read(config_file, encoding=encoding)
        if '录制设置' not in config.sections():
            config.add_section('录制设置')
        if 'Cookie' not in config.sections():
            config.add_section('Cookie')
        return config.get(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        config.set(section, option, str(default_value))
        with open(config_file, 'w', encoding=encoding) as f:
            config.write(f)
        return default_value

def update_config():
    global video_save_path, video_save_type, video_quality, max_request, semaphore
    global delay_default, local_delay_default, loop_time, split_video_by_time, split_time
    global tsconvert_to_mp4, tsconvert_to_m4a, delete_origin_file, create_time_file, dy_cookie
    global max_record_time
    config = configparser.RawConfigParser()

    try:
        with open(config_file, 'r', encoding=encoding) as f:
            config.read_file(f)
    except IOError:
        with open(config_file, 'w', encoding=encoding) as f:
            pass

    if os.path.isfile(url_config_file):
        with open(url_config_file, 'r', encoding=encoding) as f:
            ini_content = f.read()
    else:
        print("重要提示:")
        print("检测到URL_config文件不存在，请创建！")
        sys.exit(0)

    video_save_path = read_config_value(config, '录制设置', '直播保存路径（不填则默认）', "")
    video_save_type = read_config_value(config, '录制设置', '视频保存格式TS|MKV|FLV|MP4|TS音频|MKV音频', "mp4")
    video_quality = read_config_value(config, '录制设置', '原画|超清|高清|标清', "标清")
    max_request = int(read_config_value(config, '录制设置', '同一时间访问网络的线程数', 3))
    semaphore = threading.Semaphore(max_request)
    delay_default = int(read_config_value(config, '录制设置', '循环时间(秒)', 120))
    local_delay_default = int(read_config_value(config, '录制设置', '排队读取网址时间(秒)', 0))
    loop_time = options.get(read_config_value(config, '录制设置', '是否显示循环秒数', "否"), False)
    split_video_by_time = options.get(read_config_value(config, '录制设置', '分段录制是否开启', "否"), False)
    split_time = str(read_config_value(config, '录制设置', '视频分段时间(秒)', 3600))
    tsconvert_to_mp4 = options.get(read_config_value(config, '录制设置', 'TS录制完成后自动转为mp4格式', "否"),
                                   False)
    tsconvert_to_m4a = options.get(read_config_value(config, '录制设置', 'TS录制完成后自动增加生成m4a格式', "否"),
                                   False)
    delete_origin_file = options.get(read_config_value(config, '录制设置', '追加格式后删除原文件', "否"), False)
    create_time_file = options.get(read_config_value(config, '录制设置', '生成时间文件', "否"), False)

    dy_cookie = read_config_value(config, 'Cookie', '抖音cookie(录制抖音必须要有)', '')
    max_record_time = int(read_config_value(config, '录制设置','最长录制时间(秒)', 30))

    if len(video_save_type) > 0:
        if video_save_type.upper().lower() == "FLV".lower():
            video_save_type = "FLV"
        elif video_save_type.upper().lower() == "MKV".lower():
            video_save_type = "MKV"
        elif video_save_type.upper().lower() == "TS".lower():
            video_save_type = "TS"
        elif video_save_type.upper().lower() == "MP4".lower():
            video_save_type = "MP4"
        elif video_save_type.upper().lower() == "TS音频".lower():
            video_save_type = "TS音频"
        elif video_save_type.upper().lower() == "MKV音频".lower():
            video_save_type = "MKV音频"
        else:
            video_save_type = "TS"
            print("直播视频保存格式设置有问题,这次录制重置为默认的TS格式")
    else:
        video_save_type = "TS"
        print("直播视频保存为TS格式")

def parallel_download():
    # 读取url_config.ini文件
    global monitoring
    global runing_list
    global url_tuples_list
    global text_no_repeat_url
    global create_var
    global name_list
    global not_record_list
    global url_config_file
    global encoding
    try:
        with open(url_config_file, "r", encoding=encoding) as file:
            for line in file:
                line = line.strip()
                if line.startswith("#") or len(line) < 20:
                    continue

                if re.search('[,，]', line):
                    split_line = re.split('[,，]', line)
                else:
                    split_line = [line, '']
                url = split_line[0]

                if ('http://' not in url) and ('https://' not in url):
                    url = 'https://' + url

                url_host = url.split('/')[2]
                host_list = [
                    'live.douyin.com',
                    'v.douyin.com'
                ]
                if url_host in host_list:
                    new_line = (url, split_line[1])
                    url_tuples_list.append(new_line)
                else:
                    print(f"{url} 未知链接.此条跳过")

        while len(name_list):
            a = name_list.pop()
            replace_words = a.split('|')
            if replace_words[0] != replace_words[1]:
                update_file(url_config_file, replace_words[0], replace_words[1])

        if len(url_tuples_list) > 0:
            text_no_repeat_url = list(set(url_tuples_list))
        if len(text_no_repeat_url) > 0:
            for url_tuple in text_no_repeat_url:
                if url_tuple[0] in not_record_list:
                    continue

                if url_tuple[0] not in runing_list:
                    monitoring += 1
                    create_var["stop_signal"+ str(url_tuple[0])] = threading.Event()
                    args = [url_tuple, monitoring, create_var["stop_signal"+ str(url_tuple[0])]]
                    # TODO: 执行开始录制的操作
                    create_var['thread' + str(url_tuple[0])] = threading.Thread(target=start_record, args=args)
                    create_var['thread' + str(url_tuple[0])].daemon = True
                    create_var['thread' + str(url_tuple[0])].start()
                    runing_list.append(url_tuple[0])
                    time.sleep(local_delay_default)

        # 关闭不在url_config.ini文件中的线程
        no_repeat_url = [url_tuple[0] for url_tuple in text_no_repeat_url]
        # print("runing_list",runing_list)
        # print("no_repeat_url",no_repeat_url)
        for item in runing_list:
            if item not in no_repeat_url:
                create_var['stop_signal' + str(item)].set()
                print('thread' + str(item) + "stopped.")
                runing_list.remove(item)

        url_tuples_list = []
        text_no_repeat_url = []

    except Exception as e:
        logger.warning(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")

def crawl_loop():
    while True:
        update_config()
        parallel_download()
        time.sleep(1)

if __name__ == "__main__":
    crawl_loop()