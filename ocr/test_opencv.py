import cv2
import time

def cap_video(src):
    # 使用openCV中的VideoCapture函数，读取视频
    cap = cv2.VideoCapture(src)
    # 初始化定义frame_id，便于后面跳帧
    frame_id = 0
    print("hello,here")
    print(cap.isOpened())
    # 判断cap是否读取成功
    while cap.isOpened():
        # 因为视频采集，每秒可能会采集N帧，因此使用read函数，逐帧读取
        # ret 返回True或False，表示是否读取到图片
        ret, frame = cap.read()
        # 当ret为False时，not ret为True，表示没有读取到图片，说明采集结束
        if not ret:
            # 打印输出，提示信息
            print('Camera cap over')
            break
        # frame_id加1，便于跳帧
        frame_id += 1
        # 如果frame除以2，不等于0，则不断循环，只有等于0时，才进行到下面的显示步骤，这样可以达到跳帧的效果
        if not int(frame_id) % 2 == 0:
            continue
        # 便于观察，缩放图片，，比如（1000,800），即宽1000像素，高800像素
        frame = cv2.resize(frame, (1000,800))
        cv2.imshow('Image', frame)
        cv2.waitKey(20)


# cap_video('test_files/new.mp4')

frame = cv2.imread('test_files/ct_report.png')
cv2.imshow('Image',frame)