这是一个用于下载直播视频并进行实时分析的系统

## 添加监管直播链接
在 DouyinLiveRecorder/config/URL_config.ini 文件中, 每一行对应一个直播链接，如下所示：
```
https://live.douyin.com/815349576986,主播: VC官方旗舰店
https://live.douyin.com/484581718147,主播: 深海鱼油源头工厂

```
新增监管直播链接，直接新起一行加入链接即可，主播名称会在爬取过程中自动补全。

## 命令行运行方法
在本系统中，使用了tmux进行后台进程管理。因此在执行以下脚本前，需确保系统中已安装tmux。

通过脚本运行整个系统的方法如下所示：
```
# 开启系统工作
. recorder_and_analyzer_start.sh

# 关闭系统工作
. recorder_and_analyzer_end.sh
```

如果仅需运行直播视频获取模块，如下所示：
```
# 进入直播视频获取模块文件夹：
cd DouyinLiveRecorder

# 开启直播视频获取模块工作
. recorder_and_analyzer_start.sh

# 关闭直播视频获取模块工作
. recorder_and_analyzer_end.sh
```

## 直播获取模块
直播获取模块对应 DouyinLiveRecorder。其使用了ffmpeg进行视频的录制，需确保环境中已安装ffmpeg。

直播获取模块的配置文件为：DouyinLiveRecorder/config/config.ini ，在其中可以更改直播获取的相关选项，包括直播保存路径，视频保存格式，视频分段时间等等。

直播链接存放文件为：DouyinLiveRecorder/config/URL_config.ini



## 开发环境
ubuntu 22.04
python 3.11.7