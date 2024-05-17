import sys
import sherpa_ncnn
import wave
import numpy as np
import subprocess
import os

def create_recognizer():
    # Please replace the model files if needed.
    # See https://k2-fsa.github.io/sherpa/ncnn/pretrained_models/index.html
    # for download links.
    recognizer = sherpa_ncnn.Recognizer(
        tokens="asr/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-09-30/tokens.txt",
        encoder_param="asr/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-09-30/encoder_jit_trace-pnnx.ncnn.param",
        encoder_bin="asr/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-09-30/encoder_jit_trace-pnnx.ncnn.bin",
        decoder_param="asr/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-09-30/decoder_jit_trace-pnnx.ncnn.param",
        decoder_bin="asr/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-09-30/decoder_jit_trace-pnnx.ncnn.bin",
        joiner_param="asr/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-09-30/joiner_jit_trace-pnnx.ncnn.param",
        joiner_bin="asr/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-09-30/joiner_jit_trace-pnnx.ncnn.bin",
        num_threads=4,
    )
    return recognizer



def wave_file_translation(filename:str, asr_file_path:str):
    import os
    if os.path.exists(asr_file_path):
        return
    # import time
    # print("initialize start time",time.time())
    recognizer = create_recognizer()
    # print("initialize end time", time.time())

    with wave.open(filename) as f:
        assert f.getframerate() == recognizer.sample_rate, (
            f.getframerate(),
            recognizer.sample_rate,
        )
        assert f.getnchannels() == 1, f.getnchannels()
        assert f.getsampwidth() == 2, f.getsampwidth()
        num_samples = f.getnframes()
        # samples_per_read = int(5 * f.getframerate())  # 1 second = 1000 ms
        this_sample = 0
        result = ""
        while(this_sample < num_samples):
            # samples = f.readframes(samples_per_read)
            # this_sample += samples_per_read
            samples = f.readframes(num_samples)
            this_sample += num_samples
            samples_int16 = np.frombuffer(samples, dtype=np.int16)
            samples_float32 = samples_int16.astype(np.float32)
            samples_float32 = samples_float32 /32768
            recognizer.accept_waveform(recognizer.sample_rate, samples_float32)
            tail_paddings = np.zeros(
                int(recognizer.sample_rate * 0.5), dtype=np.float32
            )
            recognizer.accept_waveform(recognizer.sample_rate, tail_paddings)
            if result != recognizer.text:
                # sys.stdout.write(recognizer.text[len(result):])
                # sys.stdout.flush()
                result = recognizer.text

        recognizer.input_finished()
        with open(asr_file_path, 'w') as f:
            f.write(recognizer.text)
        # print(recognizer.text)

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

def run_kaldi_asr(video_file_path:str, asr_file_path:str):
    audio_file_path = video_file_path[:-3] + "wav"
    Extract_video_audio(video_file_path, audio_file_path)
    try:
        wave_file_translation(audio_file_path, asr_file_path)
        os.remove(audio_file_path)
    except:
        print("Something wrong in wave file translation...")

if __name__ == "__main__":

    video_file_path = "test_files/999柚美保健品专卖店_2024-04-02_21-56-39_000.mp4"
    asr_file_path = "test_files/999柚美保健品专卖店_2024-04-02_21-56-39_000_asr.txt"

    run_kaldi_asr(video_file_path, asr_file_path)