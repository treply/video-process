import os
import fnmatch

def count_images_in_dir(directory):
    image_extensions = ['*.jpg', '*.png', '*.jpeg', '*.gif']  # 添加你想统计的图片格式
    image_count = 0
    
    for root, dirs, files in os.walk(directory):
        for extension in image_extensions:
            # 使用fnmatch.filter匹配当前目录下符合条件的文件
            images = fnmatch.filter(files, extension)
            image_count += len(images)
    
    return image_count

# 使用方法：指定你想要统计的目录路径
directory_path = "D:/images/"
print(f"Total images in directory and subdirectories: {count_images_in_dir(directory_path)}")