import cv2
import os

video_counter = 38  # 添加全局计数器

def extract_frames(video_path, save_path, initial_interval=1, following_interval=10, video_number=None):
    global video_counter  # 使用全局计数器
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames < initial_interval:
        print(f"Video '{os.path.basename(video_path)}' has less than {initial_interval} frames. No images will be saved.")
        return
    
    base_video_name = f"video_{video_number:03d}"  # 使用视频序号作为基础名称
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_count < initial_interval or (frame_count >= initial_interval and frame_count % following_interval == 0):
            frame_name = f"{base_video_name}_frame_{frame_count}.jpg"
            print(frame_name)
            img_path = os.path.join(save_path, frame_name)
            cv2.imencode('.jpg', frame)[1].tofile(img_path) 
        
        frame_count += 1
    
    cap.release()
    print(f"Video processing complete.")
    video_counter += 1  # 处理完一个视频后，增加计数器


def process_videos_in_folder(folder_path, save_folder):
    global video_counter
    # video_counter = 0  # 每次开始处理文件夹时重置计数器
    for video_file in os.listdir(folder_path):
        if video_file.endswith(".mp4") or video_file.endswith(".avi"):
            video_path = os.path.join(folder_path, video_file)
            extract_frames(video_path, save_folder, video_number=video_counter)

video_folder = "C:/Users/admin/Desktop/test/ytxs"
save_images_to = "C:/Users/admin/Desktop/test/ytxs/tt" 
process_videos_in_folder(video_folder, save_images_to)