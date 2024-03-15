# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# initialize the database access object
from dao.dao import DAO

# the crawler url config file
url_config = "crawler/config/URL_config.ini"

from flask import Flask, render_template, request, jsonify
from jinja2 import TemplateNotFound
from flask_socketio import SocketIO,emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route('/index')
@app.route('/')
def index():
    return render_template('home/index.html', segment='index')

@app.route('/submit_live_url', methods=['POST'])
def submit_live_url():
    data = request.json
    liveURL = data["liveURL"]
    print(liveURL)
    with open(url_config, "a") as f:
        f.write("\n"+liveURL)
    
    return jsonify({'message':'Live data received successfully!'})

@app.route('/get_biantici', methods=['GET'])
def get_biantici():
    dao = DAO()
    table_a = dao.get_专项变体词()
    field_names = dao.get_字段名("专项变体词")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_minganci', methods=['GET'])
def get_minganci():
    dao = DAO()
    table_a = dao.get_通用敏感词()
    field_names = dao.get_字段名("通用敏感词")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_zhengjushipin', methods=['GET'])
def get_zhengjushipin():
    dao = DAO()
    table_a = dao.get_证据视频()
    field_names = dao.get_字段名("证据视频")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_jinxianshou', methods=['GET'])
def get_jinxianshou():
    dao = DAO()
    table_a = dao.get_禁限售()
    field_names = dao.get_字段名("禁限售")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_baojianpin', methods=['GET'])
def get_baojianpin():
    dao = DAO()
    table_a = dao.get_保健品()
    field_names = dao.get_字段名("保健品")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_guochanyaopin', methods=['GET'])
def get_guochanyaopin():
    dao = DAO()
    table_a = dao.get_国产药品()
    field_names = dao.get_字段名("国产药品")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_jinkouyaopin', methods=['GET'])
def get_jinkouyaopin():
    dao = DAO()
    table_a = dao.get_进口药品()
    field_names = dao.get_字段名("进口药品")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_guochanhuazhuangpin', methods=['GET'])
def get_guochanhuazhuangpin():
    dao = DAO()
    table_a = dao.get_国产化妆品()
    field_names = dao.get_字段名("国产化妆品")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_jinkouhuazhuangpin', methods=['GET'])
def get_jinkouhuazhuangpin():
    dao = DAO()
    table_a = dao.get_进口化妆品()
    field_names = dao.get_字段名("进口化妆品")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_guochanyiliaoqixiezhuce', methods=['GET'])
def get_guochanyiliaoqixiezhuce():
    dao = DAO()
    table_a = dao.get_国产医疗器械注册()
    field_names = dao.get_字段名("国产医疗器械注册")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_guochanyiliaoqixiebeian', methods=['GET'])
def get_guochanyiliaoqixiebeian():
    dao = DAO()
    table_a = dao.get_国产医疗器械备案()
    field_names = dao.get_字段名("国产医疗器械备案")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_jinkouyiliaoqixiezhuce', methods=['GET'])
def get_jinkouyiliaoqixiezhuce():
    dao = DAO()
    table_a = dao.get_进口医疗器械注册()
    field_names = dao.get_字段名("进口医疗器械注册")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_jinkouyiliaoqixiebeian', methods=['GET'])
def get_jinkouyiliaoqixiebeian():
    dao = DAO()
    table_a = dao.get_进口医疗器械备案()
    field_names = dao.get_字段名("进口医疗器械备案")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_zhiboshitichi',methods=['GET'])
def get_zhiboshitichi():
    dao = DAO()
    table_a = dao.get_直播实体池()
    field_names = dao.get_字段名("直播实体池")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_zhiboshitichi_field',methods=['GET'])
def get_zhiboshitichi_field():
    dao = DAO()
    field_names = dao.get_字段名("直播实体池")
    dao.close()
    return jsonify(data = field_names)

@app.route('/get_dingzhizhiboshiti',methods=['GET'])
def get_dingzhizhiboshiti():
    dao = DAO()
    table_a = dao.get_定制直播实体()
    field_names = dao.get_字段名("定制直播实体")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_xunjianzhiboshiti',methods=['GET'])
def get_xunjianzhiboshiti():
    dao = DAO()
    table_a = dao.get_巡检直播实体()
    field_names = dao.get_字段名("巡检直播实体")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_dingzhizhibolishi',methods=['GET'])
def get_dingzhizhibolishi():
    dao = DAO()
    table_a = dao.get_定制直播历史()
    field_names = dao.get_字段名("定制直播历史")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/get_xunjianzhibolishi',methods=['GET'])
def get_xunjianzhibolishi():
    dao = DAO()
    table_a = dao.get_巡检直播历史()
    field_names = dao.get_字段名("巡检直播历史")
    table_b = [dict(zip(field_names, i)) for i in table_a]
    dao.close()
    return jsonify(data = table_b)

@app.route('/insert',methods=['POST'])
def insert():
    data = request.json
    print(data)
    tableName = data['tableName']
    record = data['record']
    dao = DAO()
    dao.insert(tableName,**record)
    return jsonify({'message':'Live data received successfully!'})

@app.route('/delete',methods=['POST'])
def delete():
    data = request.json
    print(data)
    tableName = data['tableName']
    record = data['record']
    dao = DAO()
    dao.delete(tableName,**record)
    return jsonify({'message':'Live data received successfully!'})


@app.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    emit('message_from_server', json)


@socketio.on('liveplay_client')
def handle_liveplay_event(info):
    print('received info: ' + str(info))
    # 将收到的链接名写入url_config.ini文件,如果其中已经存在该链接则不写入
    with open(url_config, "r") as f:
        contents = f.read()
    
    print(info["liveURL"] in contents)
    if info["liveURL"] not in contents:
        with open(url_config, "a+") as f:
            f.write("\n" + info["liveURL"])

    # 等待一秒后，读取url_config.ini文件中，对应链接逗号后面的内容作为ahchor_name
    import time
    time.sleep(1)
    anchor_name = ''

    with open(url_config,"r") as f:
        lines = f.readlines()
        for line in lines:
            if info["liveURL"] in line:
                print(line.strip('\n'))
                anchor_name = line.strip('\n').split("主播: ")[-1]
                print(anchor_name)
    
    # 读取所有视频文件中含有anchor_name的文件
    import os
    live_video_path_list = []
    cache_path = "static/video/record"
    for root, dirs, files in os.walk(cache_path):
        for file in files:
            if file[-3:].lower() == "mp4" and anchor_name in file:
                file_path = os.path.join(root,file)
                live_video_path_list.append(file_path)


    # 将该文件进行ocr和asr识别
    from live_analyzer import video_to_txt
    from match import match
    for live_video_path in live_video_path_list:
        print(live_video_path)
        analysis_start_time = time.time()
        asr_result, ocr_result = video_to_txt(live_video_path)
        dao = DAO()
        analysis_result = dao.get_证据视频_by_name(live_video_path)
        if len(analysis_result) != 0:
            txt = analysis_result[0][4]
            result = txt
        else:
            txt = asr_result +"\n" + ocr_result
            print(txt)
            result = match.text_analysis(txt)
            print(result)
            from datetime import datetime 
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d_%H:%M:%S")
            dao.insert_证据视频(live_video_path,ocr_result, asr_result, result, formatted_time, info["liveURL"])
        dao.close()
        analysis_end_time = time.time()
        result = eval(result)
        if result["type"] == 0:
            result = "直播内容正常"
        emit('liveplay_server', {"live_video_path":live_video_path, "ocr_result":ocr_result, "asr_result":asr_result, "analysis":result})
        time.sleep(30-analysis_end_time+analysis_start_time)

@socketio.on('stopliveplay')
def handle_stopliveplay_event(txt):
    print("receive txt: " + txt)


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",port=5000)