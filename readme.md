这是一个用于实时分析视频的系统

## 添加监管直播链接
在 DouyinLiveRecorder/config/URL_config.ini 文件中, 每一行对应一个直播链接，如下所示：
```
https://live.douyin.com/815349576986,主播: VC官方旗舰店
https://live.douyin.com/484581718147,主播: 深海鱼油源头工厂

```
新增监管直播链接，直接新起一行加入链接即可，主播名称会在爬取过程中自动补全。

## 命令行运行方法
```
# 开启系统工作
. recorder_and_analyzer_start.sh

# 关闭系统工作
. recorder_and_analyzer_end.sh
```

## 开发环境
ubuntu 22.04
python 3.11.7