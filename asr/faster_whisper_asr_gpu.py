import subprocess
from faster_whisper import WhisperModel
# import torch
# device = "cuda:0" if torch.cuda.is_available() else "cpu"  

base_model_dir = "asr/faster-whisper-base"
large_v3_model_dir = "asr/faster-distil-whisper-large-v3"

model = WhisperModel(base_model_dir)

def transcribe(audio_path):

    # init_prompt = "以下是中文普通话的语句："
    segments, info = model.transcribe(audio_path, beam_size=5, language="zh")

    # print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    all_text = ""
    all_text_with_timestamp = ""
    for segment in segments:
        text_with_timestamp = "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
        # print(text_with_timestamp)
        all_text += segment.text
        all_text_with_timestamp += text_with_timestamp + "\n"
    
    result = all_text + "\n" + all_text_with_timestamp
    return result

def Extract_video_audio(video_path, audio_path):
    desired_sample_rate = 16000
    desired_bit_depth = 16
    desired_channels = 1
    ffmpeg_cmd = f"ffmpeg -y -i {video_path} -ac {desired_channels} -ar {desired_sample_rate} -sample_fmt s{desired_bit_depth} {audio_path}"
    subprocess.run(ffmpeg_cmd,shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def format_audio(audio_path, format_audio_path):
    desired_sample_rate = 16000
    desired_bit_depth = 16
    desired_channels = 1
    ffmpeg_cmd = f"ffmpeg -y -i {audio_path} -ac {desired_channels} -ar {desired_sample_rate} -sample_fmt s{desired_bit_depth} {format_audio_path}"
    subprocess.run(ffmpeg_cmd,shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_whisper_asr(video_file_path:str, asr_file_path:str):
    import os
    if os.path.exists(asr_file_path):
        # return
        pass
    audio_file_path = video_file_path[:-3] + "wav"
    Extract_video_audio(video_file_path, audio_file_path)
    try:
        result = transcribe(audio_file_path)
        print(result)
        import os
        os.remove(audio_file_path)
        with open(asr_file_path, 'w') as f:
            f.write(result)
    except:
        print("Something wrong in wave file translation...")

if __name__ == "__main__":
    video_file_path = "test_files/999柚美保健品专卖店_2024-04-02_21-56-39_000.mp4"
    asr_file_path = "test_files/999柚美保健品专卖店_2024-04-02_21-56-39_000_asr_gpu.txt"
    run_whisper_asr(video_file_path, asr_file_path)