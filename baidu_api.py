import base64
import urllib
import os
import cv2
import requests
import numpy as np
# API_KEY = "fzQ1PdnkxqvEo0yfZyQ39DAa"
# SECRET_KEY = "CGwARylILCXDR4XyxaUPOegRKceobWrX"

# xyy
API_KEY = "TNDBbAGV8535Dr8Gnq0vcKId"
SECRET_KEY = "LcdmD4xAn1PgRERcgz9ygdQQznYDmfGU"

pose_labels = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle"
]

# pose_labels = [
#     "left_shoulder",
#     "right_shoulder",
#     "left_elbow",
#     "right_elbow",
#     "left_wrist",
#     "right_wrist",
#     "left_hip",
#     "right_hip",
#     "left_knee",
#     "right_knee",
#     "left_ankle",
#     "right_ankle"
# ]

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

        
url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis?access_token=" + get_access_token()
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}


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

# def draw_image(image, pose_landmark):
#     height, width, _ = image.shape
#     pose_landmark_sl = []
#     for index in select_index:
#          pose_landmark_sl.append(pose_landmark[index])

#     for edge in KEYPOINT_EDGE_INDS_TO_COLOR.keys():
#         point_s_x = pose_landmark_sl[edge[0]].x * width
#         point_s_y = pose_landmark_sl[edge[0]].y * height

#         point_e_x = pose_landmark_sl[edge[1]].x * width
#         point_e_y = pose_landmark_sl[edge[1]].y * height
#         cv2.line(image, (int(point_s_x), int(point_s_y)), (int(point_e_x), int(point_e_y)),  (128, 0, 0), 1)
#     return image

#image_dir = "E:/DataSet/SPORTE/dataset/images_s/"1
#save_dir = "E:/DataSet/SPORTE/dataset/images_labels_s1/"
# image_dir = "D:/images/"
# save_dir = "D:/images_labels_s1/"

#image_dir = "C:/Users/admin/Desktop/testDataset/frames_bili" 
image_dir = "C:/Users/admin/Desktop/testDataset_7.10/frames" 
save_dir = "C:/Users/admin/Desktop/testDataset_7.10/frames_label" 

image_list = os.listdir(image_dir)

for image_name in image_list[0:]:
    # if image_name != "obj365_train_000000000075.jpg":
    #     continue
    print(image_name)

    image_path = os.path.join(image_dir, image_name)
    im = cv2.imread(image_path)
    height, width, _ = im.shape
    # plt_im = np.zeros([height, width, 3], np.int8)
    payload = {}
    payload["image"] = get_file_content_as_base64(image_path)
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        info_dict = eval(response.text)
        person_num = info_dict["person_num"]
    except:
        continue
    person_infoes = info_dict["person_info"]
    with open(os.path.join(save_dir,image_name.replace(".jpg", ".txt")), "w") as f:
        for i in range(person_num):
            person_info = person_infoes[i]
            location = person_info["location"]
            body_parts = person_info["body_parts"]
            xmin = location["left"]
            ymin = location["top"]
            xmax = location["width"] + xmin
            ymax = location["height"] + ymin
            cv2.rectangle(im,(int(xmin), int(ymin)), (int(xmax), int(ymax)), (0,128, 0), 2)
            loc_str = str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax) + " "
            f.write(loc_str)
            points_list = []
            for pose_name in pose_labels:
                part_info = body_parts[pose_name]
                x = part_info["x"]
                y = part_info["y"]
                score = part_info["score"]
                points_list.append({"x": x, "y":y})
                if score > 0.2:
                    part_str = str(x) + " " + str(y) + " " + str(1) + " "
                else:
                    part_str = str(0) + " " + str(0) + " " + str(0) + " "
                f.write(part_str)
                if (pose_name == "left_shoulder"):
                    cv2.circle(im, (int(x), int(y)), 6, (128, 0, 0), 10)
            f.write("\n")
            # print(points_list[0])
            for edge in KEYPOINT_EDGE_INDS_TO_COLOR.keys():
                point_s_x = points_list[edge[0]]["x"]
                point_s_y = points_list[edge[0]]["y"]

                point_e_x = points_list[edge[1]]["x"]
                point_e_y = points_list[edge[1]]["y"]
                cv2.line(im, (int(point_s_x), int(point_s_y)), (int(point_e_x), int(point_e_y)),  (128, 128, 0), 2)
    cv2.imwrite(os.path.join(save_dir, image_name), im)
