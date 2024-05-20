# live_analyzer

这是一个用于下载直播视频并进行实时分析的系统。

## 部署方法

### python 环境安装

首先安装相关的python依赖包。

```bash
pip install -r requirements.txt
```

### asr 模型下载

本项目中使用的asr模型包括next-gen kaldi模型以及whisper模型，其中next-gen kaldi模型通过sherpa-ncnn推理框架进行部署，whisper模型采用faster-whisper的base版本。

kaidi模型的下载地址为： 链接：[夸克网盘](https://pan.quark.cn/s/276a8aa25309)  提取码：D2h6

faster-whisper模型的下载地址为：[faster-whisper-base](https://huggingface.co/Systran/faster-whisper-base)

下载完成后，如果为压缩包，请解压。将文件夹放入asr文件夹中。

### 大模型使用方式

本项目中有两种使用大模型的方法，第一种是通过spark api进行推理，第二种是通过本地部署大模型进行推理，使用http通信。
需要将两种方式的api ID和相关key添加到环境变量中，例如，可以在项目根目录创建一个.env文件，并在其中写入：

```text
# SparkApi information
SPARK_APPID=******
SPARK_API_SECRET=******
SPARK_API_KEY=******

# local llama information
LLAMA_BASE_URL=http://127.0.0.1:8080/v1
LLAMA_API_KEY=sk-no-key-required
```

本项目采用llama cpp进行预训练大模型的部署推理，采用http server的形式进行交互使用。具体的部署方式可以参考：<https://github.com/ggerganov/llama.cpp/tree/master/examples/server>

也可以使用llamafile打包预训练模型及其部署环境、http server，一键启动：

llamafile打包模型下载地址：[llama 3](https://huggingface.co/Mozilla/Meta-Llama-3-8B-Instruct-llamafile/resolve/main/Meta-Llama-3-8B-Instruct.Q5_K_M.llamafile?download=true)

```bash
./${llamafile} -ngl 9999 --host 127.0.0.1 --port 8080
```

## 添加监管直播链接

在 DouyinLiveRecorder/config/URL_config.ini 文件中, 每一行对应一个直播链接，如下所示：

```text
https://live.douyin.com/815349576986,主播: VC官方旗舰店
https://live.douyin.com/484581718147,主播: 深海鱼油源头工厂
……
```

新增监管直播链接，直接新起一行加入链接即可，主播名称会在爬取过程中自动补全。

## 命令行运行方法

在本系统中，使用了tmux进行后台进程管理。因此在执行以下脚本前，需确保系统中已安装tmux。

通过脚本运行整个系统的方法如下所示：

```bash
# 开启系统工作
. recorder_and_analyzer_start.sh

# 关闭系统工作
. recorder_and_analyzer_end.sh
```

如果仅需运行直播视频获取模块，如下所示：

```bash
# 进入直播视频获取模块文件夹：
cd DouyinLiveRecorder

# 开启直播视频获取模块工作
. live_recorder_start.sh

# 关闭直播视频获取模块工作
. live_recorder_end.sh
```

## 直播获取模块

直播获取模块对应 DouyinLiveRecorder。其使用了ffmpeg进行视频的录制，需确保环境中已安装ffmpeg。

直播获取模块的配置文件为：DouyinLiveRecorder/config/config.ini ，在其中可以更改直播获取的相关选项，包括直播保存路径，视频保存格式，视频分段时间等等。

直播链接存放文件为：DouyinLiveRecorder/config/URL_config.ini

## 开发环境

ubuntu 22.04

python 3.11.7
