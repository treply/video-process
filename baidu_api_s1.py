import os
import cv2
import numpy as np

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

def draw_keypoint_connections(image, keypoints, edge_colors):
    """根据给定的连接规则在图像上绘制关键点之间的连线"""
    for edge, color in edge_colors.items():
        start_point = keypoints[edge[0]]
        end_point = keypoints[edge[1]]
        if start_point[0] != 0 and end_point[0] != 0:
            cv2.line(image, (int(start_point[0]), int(start_point[1])), (int(end_point[0]), int(end_point[1])), (128, 128, 0), 2)

def read_txt(file_path):
    """从TXT文件读取所有行数据，每行数据转换为一个对象的描述列表"""
    objects_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # 假设每行数据格式为：[xmin, ymin, xmax, ymax, p1x, p1y, p2x, p2y, ...]
            # 分割并转换为浮点数，然后添加到当前行的对象数据列表中
            data = [float(i) for i in line.strip().split()]
            objects_data.append(data)
    return objects_data

def calculate_iou(box1, box2):

    # 将坐标转为float进行精确计算
    box1 = [float(coord) for coord in box1]
    box2 = [float(coord) for coord in box2]

    # 计算每个box的宽度和高度
    width_box1 = box1[2] - box1[0]
    height_box1 = box1[3] - box1[1]
    width_box2 = box2[2] - box2[0]
    height_box2 = box2[3] - box2[1]

    # 计算两个box的交集矩形的左下角和右上角坐标
    intersect_xmin = max(box1[0], box2[0])
    intersect_ymin = max(box1[1], box2[1])
    intersect_xmax = min(box1[2], box2[2])
    intersect_ymax = min(box1[3], box2[3])

    # 计算交集的宽度和高度，如果为负，则说明没有交集
    intersect_width = max(0, intersect_xmax - intersect_xmin)
    intersect_height = max(0, intersect_ymax - intersect_ymin)

    # 计算交集面积
    area_intersect = intersect_width * intersect_height

    # 仅返回交集面积而非IoU，根据题目要求调整
    return area_intersect

def calculate_box_area(box):
    """计算单个box的面积"""
    width = box[2] - box[0]
    height = box[3] - box[1]
    return width * height

def draw_objects(image_path, objects_data):
    """在图片上绘制所有对象的检测框和关键点"""
    image = cv2.imread(image_path)
    save_txt = image_path.replace(".jpg", ".txt")
    save_txt = save_txt.replace("frames", "frames_label_s1")
    ff = open(save_txt, 'w')
    bboxs=[]
    for obj_data in objects_data:
        box = obj_data[:4]
        bboxs.append(box);

    overlapping_areas = []
    for box1 in bboxs:
        overlapping_area_list = []
        for box2 in bboxs:
            overlap_area = calculate_iou(box1, box2)
            overlapping_area_list.append(overlap_area)
        overlapping_areas.append(overlapping_area_list)
    overlapping_areas_sums = [sum(row) for row in overlapping_areas]
    
    areas_objects_data = [calculate_box_area(obj_data[:4]) for obj_data in objects_data]

    resultant_areas = [sum_areas - area_obj for sum_areas, area_obj in zip(overlapping_areas_sums, areas_objects_data)]

    ratios = [resultant_area / area_obj for resultant_area, area_obj in zip(resultant_areas, areas_objects_data)]


    for idx, obj_data in enumerate(objects_data):
        # 绘制检测框
        bbox = obj_data[:4]
        if bbox[2]-bbox[0]>50 and bbox[3]-bbox[1]>100 and ratios[idx] < 0.7:
            ff.write(str(bbox[0]))
            ff.write(" ")
            ff.write(str(bbox[1]))
            ff.write(" ")
            ff.write(str(bbox[2]))
            ff.write(" ")
            ff.write(str(bbox[3]))
            ff.write(" ")
            cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), 
                      (int(bbox[2]), int(bbox[3])), (0, 128, 0), 2)
            
            
            keypointss = np.array(obj_data[4:]).reshape(-1, 3)
            for kp in keypointss:
                ff.write(str(kp[0]))
                ff.write(" ")
                ff.write(str(kp[1]))
                ff.write(" ")
                ff.write(str(kp[2]))
                ff.write(" ")
            ff.write("\n")
            # 绘制关键点
            keypoints = [(obj_data[i], obj_data[i+1]) for i in range(4, len(obj_data), 3)]
            keypoint = keypoints[5]
            cv2.circle(image, (int(keypoint[0]), int(keypoint[1])), 6, (128, 0, 0), 10)
            # 连接关键点
            draw_keypoint_connections(image, keypoints, KEYPOINT_EDGE_INDS_TO_COLOR)
    
    return image

def process_folder(folder_path):
    """处理文件夹中的所有TXT文件"""
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            txt_path = os.path.join(folder_path, filename)
            image_path = txt_path.replace("frames_label", "frames")
            image_path = image_path.replace(".txt", ".jpg")
            image_name = filename[:-4] + '.jpg'  # 假设图片与TXT文件名相同，只是扩展名不同

           
            
            if os.path.exists(image_path):
                data = read_txt(txt_path)
                result_img = draw_objects(image_path, data)
                
                # 保存或显示结果图片，这里仅作为示例保存图片
                cv2.imwrite(os.path.join(save_dir, image_name), result_img)
            else:
                print(f"Image {image_name} not found.")


image_dir = "C:/Users/admin/Desktop/testDataset_7.10/frames_label"
save_dir = "C:/Users/admin/Desktop/testDataset_7.10/frames_label_s1"

process_folder(image_dir)

print("Processing completed.")