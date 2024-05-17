import subprocess
import whisper

# import torch
# device = "cuda:0" if torch.cuda.is_available() else "cpu"  

model = whisper.load_model("large-v2",download_root="./asr/whisper/")

def transcribe(audio_path):
    audio = whisper.load_audio(audio_path)  
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(beam_size=5,prompt="请注意，下面是普通话的语句：")
    result = whisper.decode(model, mel, options)  
    # print(result.text)
    return result.text

def Extract_video_audio(video_path, audio_path):
    desired_sample_rate = 16000
    desired_bit_depth = 16
    desired_channels = 1
    ffmpeg_cmd = f"ffmpeg -y -i {video_path} -ac {desired_channels} -ar {desired_sample_rate} -sample_fmt s{desired_bit_depth} {audio_path}"
    subprocess.run(ffmpeg_cmd,shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_whisper_asr(video_file_path:str, asr_file_path:str):
    import os
    if os.path.exists(asr_file_path):
        return
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