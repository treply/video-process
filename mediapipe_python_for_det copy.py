import cv2
import json
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
model_path = 'D:/set-up/pose_landmarker_heavy.task'

KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

def draw_image(image, pose_landmark):
    height, width, _ = image.shape
    pose_landmark_sl = []
    for index in select_index:
         pose_landmark_sl.append(pose_landmark[index])

    for edge in KEYPOINT_EDGE_INDS_TO_COLOR.keys():
        point_s_x = pose_landmark_sl[edge[0]].x * width
        point_s_y = pose_landmark_sl[edge[0]].y * height

        point_e_x = pose_landmark_sl[edge[1]].x * width
        point_e_y = pose_landmark_sl[edge[1]].y * height
        cv2.line(image, (int(point_s_x), int(point_s_y)), (int(point_e_x), int(point_e_y)),  (128, 0, 0), 2)
    return image

select_index = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

points_label = ["nose", "left eye1", "left eye2", "left eye3", "right eye1", "right eye2", "right eye3", "left ear", "right ear",
                "mouth_left", "mouth_right", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist",
                "left_pinky", "right_pinky", "left_index", "right_index", "left_thumb", "right_thumb", "left_hip", "right_hip", 
                "left_knee", "right_knee", "left_ankle", "right_ankle", "left_heel", "right_heel", "left foot index", "right foot index"]
print(len(points_label))
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def bbox_iom(box1, box2):
    left = max(box1[0], box2[0])
    top = max(box1[1], box2[1])
    right = min(box1[2], box2[2])
    bottom = min(box1[3], box2[3])

    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    if left >= right or top >= bottom:
        return 0
    inter_area = (right - left) * (bottom - top)
    union_area = min(box1_area, box2_area)

    iom = inter_area * 1.0 / union_area
    return iom

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE)

landmarker = PoseLandmarker.create_from_options(options)

image_dir = "D:/set-up/images/"
save_dir = "D:/set-up/media/"
image_list = os.listdir(image_dir)
for image_name in image_list:
    if os.path.exists(os.path.join(save_dir, image_name)):
        continue
    image_path = os.path.join(image_dir, image_name)
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image.astype(np.uint8))
    pose_landmarker_result = landmarker.detect(mp_image)
    if not pose_landmarker_result.pose_landmarks:
        continue
    ff = open(os.path.join(save_dir, image_name.replace(".jpg", ".txt")), "w")
    pose_=[]

    for index, pose_landmark in enumerate(pose_landmarker_result.pose_landmarks[0]):
        if index in select_index:
            x=pose_landmark.x * width
            y=pose_landmark.y * height
            if pose_landmark.presence < 0.5 and pose_landmark.visibility < 0.5:
                pose_.append(0)
                pose_.append(0)
                pose_.append(0)
            else:
                pose_.append(x)
                pose_.append(y)
                pose_.append(1)
    keypoints = np.array(pose_[0:]).reshape(-1, 3)
    for kp in keypoints:
        ff.write(str(kp[0]))
        ff.write(" ")
        ff.write(str(kp[1]))
        ff.write(" ")
        ff.write(str(kp[2]))
        ff.write(" ")
    for edge in KEYPOINT_EDGE_INDS_TO_COLOR.keys():
        point_s_x = keypoints[edge[0]][0]
        point_s_y = keypoints[edge[0]][1]
        point_s_v = keypoints[edge[0]][2]

        point_e_x = keypoints[edge[1]][0]
        point_e_y = keypoints[edge[1]][1]
        point_e_v = keypoints[edge[1]][2]
        if point_s_v == 0 or point_e_v == 0:
            continue
        cv2.line(image, (int(point_s_x), int(point_s_y)), (int(point_e_x), int(point_e_y)),  (128, 128, 0), 2)
    cv2.imwrite(os.path.join(save_dir, image_name), image)
    