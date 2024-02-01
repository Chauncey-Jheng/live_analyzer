import subprocess
import time
from tqdm import tqdm

class ScreenRecorder:
    '''
    用于录制视频
    '''
    def __init__(self, 
                 video_file_path,
                 audio_file_path,
                 final_file_path,
                 screen_start_pos=(0,0), 
                 screen_size=(1920,1080), 
                 time=30,
                ) -> None:
        '''
        初始化一些参数

        video_file_path: 不带声音的屏幕录制视频存放路径
        
        audio_file_path: 应用播放音频存放路径

        final_file_path: 合成了音频的最终视频存放路径

        screen_start_pos: 录制屏幕起始位置（左上角点位置）,example:(0,0)

        screen_size: 录制屏幕大小,example:(1920,1080)

        time: 录制视频片段时间，单位为秒

        '''
        self.video_file_path = video_file_path
        self.audio_file_path = audio_file_path
        self.final_file_path = final_file_path
        self.screen_start_pos = screen_start_pos
        self.screen_size = screen_size
        self.time = time
        pass

    def open_url(self, url):
        '''
        控制浏览器，打开视频链接

        url: 视频网址链接,例如: https://live.bilibili.com/21696950
        '''
        cmd = "chromium " + url
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pass
    
    def kill_chrome():
        subprocess.run(["pkill","chrome"])
        pass

    def recording(self):
        '''
        开始录制
        '''
        
        cmdstr_video = "ffmpeg -y -f x11grab -s {x}x{y} -framerate 25 -i :0.0+{a},{b} -t {t} {path}".format(
            x = self.screen_size[0], y = self.screen_size[1],
            a = self.screen_start_pos[0], b=self.screen_start_pos[1],
            t = self.time,
            path = self.video_file_path
            )
        cmdstr_audio = "ffmpeg -y -f alsa -channels 2 -sample_rate 48000 -i hw:Loopback,1,0 -t {t} {path}".format(
            t = self.time,
            path = self.audio_file_path
        )
        cmdstr_final = "ffmpeg -i {path1} -i {path2} {path3}".format(
            path1 = self.video_file_path,
            path2 = self.audio_file_path,
            path3 = self.final_file_path
        )
        subprocess.Popen(cmdstr_video, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(cmdstr_audio, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Recording...")
        for _ in tqdm(range(self.time)):
            time.sleep(1)
        print("Recording finish!")
        subprocess.Popen(cmdstr_final, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pass


def test_record():
    cmdstr_video = "ffmpeg -y -f x11grab -s 1920x1080 -framerate 25 -i :0.0+0,0 -t 30 test_files/out.avi" 
    cmdstr_audio = "ffmpeg -y -f alsa -channels 2 -sample_rate 48000 -i hw:Loopback,1,0 -t 30 test_files/out.aac"
    cmdstr_concat = "ffmpeg -y -i test_files/out.avi -i test_files/out.aac test_files/new.mp4"
    subprocess.Popen(cmdstr_video, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen(cmdstr_audio, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Recording...")
    for i in tqdm(range(30)):
        time.sleep(1)
    print("Recording finish!")
    subprocess.Popen(cmdstr_concat, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    test_record()