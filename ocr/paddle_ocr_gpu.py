import cv2

from paddleocr import PaddleOCR
det_model="ocr/model/ch_PP-OCRv4_det_infer"
rec_model="ocr/model/ch_PP-OCRv4_rec_infer"
cls_model="ocr/model/ch_ppocr_mobile_v2.0_cls_infer"

ocr = PaddleOCR(det_model_dir=det_model, 
                rec_model_dir=rec_model, 
                cls_model_dir=cls_model,
                use_angle_cls=True,
                use_gpu=True,
                gpu_mem=500,
                # gpu_id=0,
                precision='fp32',
                use_mp=True,
                total_process_num=4,
                show_log=False)

def run_paddle_ocr_gpu(source, ocr_file_path, skip_frames=30):
    """
    Main function to run the paddleOCR inference:
    1. Create a video player to play with target fps      .
    2. Prepare a set of frames for text detection and recognition.
    3. Run AI inference for both text detection and recognition.

    Parameters:
        source: The video path.  
        ocr_file_path: The path ro save ocr result text
        skip_frames: Number of frames to skip per frame to ocr. 
    """
    import os
    if os.path.exists(ocr_file_path):
        return
        # pass
    try:
        # player = ocr_utils.VideoPlayer(source=source, flip=flip, fps=30, skip_first_frames=skip_first_frames)
        # Start video capturing.
        # player.start()
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise RuntimeError("Could not open the video file.")
        
        frame_id = 0
        all_txts = []
        while True:
            # Grab the frame.
            # frame = player.next()
            ret, frame = cap.read()
            if not ret:
                print('Camera cap over')
                break
            frame_id += 1
            if frame_id % skip_frames != 0:
                continue
            
            result  = ocr.ocr(frame)[0]
            txts = [line[1][0] for line in result]
            for txt in txts:
                if txt not in all_txts:
                    all_txts.append(txt)

            # Record the ocr txt result
        with open(ocr_file_path,"w") as f:
            for i in all_txts:
               f.write(i+" ")
            
    # ctrl-c
    except KeyboardInterrupt:
        print("Interrupted")
    # any different error
    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    source = "test_files/999柚美保健品专卖店_2024-04-02_21-56-39_000.mp4"
    ocr_file_path = "test_files/999柚美保健品专卖店_2024-04-02_21-56-39_000_ocr_gpu.txt"
    run_paddle_ocr_gpu(source=source, ocr_file_path=ocr_file_path)