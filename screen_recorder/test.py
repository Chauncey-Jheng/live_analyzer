def test_dotenv():
    from dotenv import load_dotenv
    load_dotenv()

    import os
    path = os.getenv("VIDEO_FILE_PATH")
    print(path)
    # with open(path+"test.txt", "w+") as f:
    #     f.write("hhhh")
    num = os.getenv('CACHE_VIDEO_NUM')
    print(type(num))
    print(num)
    int_num = int(num)
    print(type(int_num))
    print(int_num)


def test_selenium():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    url = "http://www.bilibili.com"
    driver.get(url)
    import time
    time.sleep(5)
    driver.quit()

def cmd_chromium():
    import subprocess
    cmd = "chromium www.bilibili.com"
    chrome_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import time
    time.sleep(5)
    subprocess.run(["pkill","chrome"])

def test_str_format():
    cmdstr = "{x}x{y}".format(x='123',y='456')
    print(cmdstr)

def test_datetime():
    from datetime import datetime

    # 获取当前日期和时间
    current_datetime = datetime.now()

    # 格式化日期和时间为指定格式
    formatted_datetime = current_datetime.strftime("%Y_%m%d_%H_%M_%S")

    # 你的原始字符串
    your_string = "file"

    # 加上格式化的时间戳
    result_string = f"{your_string}_{formatted_datetime}.mp4"

    # 打印结果
    print(result_string)


def test_create_dir():
    import os
    dir_path = "static/video/record/"
    video_name = "testvideo"
    video_dir_path = os.path.join(dir_path, video_name)
    if not os.path.isdir(video_dir_path):
        os.mkdir(video_dir_path)

if __name__ == "__main__":
    test_dotenv()
    # test_selenium()
    # cmd_chromium()
    # test_str_format()
    # test_datetime()
    # test_create_dir()
    pass