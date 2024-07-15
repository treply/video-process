import os

# 指定文件夹路径
folder_path = 'C:/Users/admin/Desktop/testDataset_7.10/frames_bili_label_s2'

# 获取文件夹中所有的文件列表
files = os.listdir(folder_path)

# 遍历文件列表
for file in files:
    # 检查文件是否为.txt文件
    if file.endswith('.txt'):
        # 构建对应.jpg文件的名称
        jpg_file = os.path.splitext(file)[0] + '.jpg'
        
        # 检查.jpg文件是否存在
        if not os.path.exists(os.path.join(folder_path, jpg_file)):
            # 如果不存在，删除.txt文件
            txt_file_path = os.path.join(folder_path, file)
            os.remove(txt_file_path)
            print(f"Deleted: {txt_file_path}")

print("Operation completed.")