import cv2
import os
import sys
import numpy as np

def crop_image(image_path):
    # 이미지 로드
    img = cv2.imread(image_path)
    if img is None:
        return None

    height, width = img.shape[:2]
    print(f"원본 크기: {width}x{height}")

    # 중심점을 기준으로 가로세로 400px씩 잘라내기
    # crop_w, crop_h = 200, 200
    
    # start_x = max(0, width // 2 - crop_w // 2)
    # start_y = max(0, height // 2 - crop_h // 2)
    
    # center_cropped = img[start_y : start_y + crop_h, start_x : start_x + crop_w]
    # small_img = cv2.resize(img, (800, 450)) # 다운사이징
    
    
    # cv2.imwrite("output.jpg", center_cropped)
    
    # print("크롭 완료: output.jpg으로 저장.")
    # return center_cropped

if __name__ == "__main__":
    crop_image("input.jpg")