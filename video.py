import numpy as np
import cv2 as cv
import datetime

video = cv.VideoCapture(0)

# 비디오 저장을 위한 설정
fourcc = cv.VideoWriter_fourcc(*'XVID')  # 코덱 설정
output = None
recording = False
filename = ''

# 밝기 조정 값
brightness_value = 0

def adjust_brightness(image, value):

    if value == 0:
        return image
    
    # 양수면 밝게, 음수면 어둡게
    if value > 0:
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        
        # 밝기에 값을 더함
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        
        hsv = cv.merge((h, s, v))
        return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    else:
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        
        # 밝기에서 값을 뺌
        value = -value
        lim = value
        v[v < lim] = 0
        v[v >= lim] -= value
        
        hsv = cv.merge((h, s, v))
        return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

if video.isOpened():
    while True:
        ret, frame = video.read()
        
        # 프레임을 제대로 읽지 못한 경우 처리
        if not ret or frame is None:
            print("프레임을 읽을 수 없습니다. 종료합니다.")
            break
        
        # 밝기 조정 적용
        frame = adjust_brightness(frame, brightness_value)
        
        # 원본 프레임
        original_frame = frame.copy()
        
        # 녹화 중 빨간 점 표시
        if recording:
            cv.circle(frame, (30, 30), 10, (0, 0, 255), -1)  # 화면에만 빨간색 원 표시
            output.write(original_frame)
        
        # 현재 밝기 값 표시
        cv.putText(frame, f"Brightness: {brightness_value}", (frame.shape[1] - 150, 30), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        cv.imshow('Video', frame)
        pressed_key = cv.waitKey(1)
        
        match pressed_key:
            case 27:  # ESC누르면 종료
                break
            case 32:  # 스페이스바(32)를 누르면 모드 변경
                if not recording:
                    # 녹화 시작
                    # 현재 날짜와 시간을 파일명으로 사용
                    now = datetime.datetime.now()
                    filename = f"recording_{now.strftime('%Y%m%d_%H%M%S')}.avi"
                    
                    # 비디오 저장 설정
                    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
                    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
                    fps = video.get(cv.CAP_PROP_FPS)
                    
                    output = cv.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
                    recording = True
                    print(f'녹화 시작: {filename}')
                else:
                    # 녹화 종료
                    recording = False
                    output.release()
                    print(f'녹화 종료: {filename}')
            case 43:  # +를 누르면 밝기 증가
                if brightness_value <= 240:
                    brightness_value += 10
                    print(f'밝기 증가: {brightness_value}')
            case 45:  # -를 누르면 밝기 감소
                if brightness_value >= -240:
                    brightness_value -= 10
                    print(f'밝기 감소: {brightness_value}')

    # 모든 자원 해제
    if recording:
        output.release()
    video.release()
    cv.destroyAllWindows()