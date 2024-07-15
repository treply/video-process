import os
import shutil

# 指定源目录和目标目录
source_dir = 'C:/Users/admin/Desktop/testDataset_7.10/frames_bili'
label_dir = 'C:/Users/admin/Desktop/frames_label'
target_dir = 'C:/Users/admin/Desktop/frames'

# 创建目标目录，如果它还不存在的话
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 获取label目录下的所有.jpg文件名
label_files = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.endswith('.jpg')}

# 遍历source目录中的所有文件
for filename in os.listdir(source_dir):
    # 检查文件是否为.jpg格式并且在label_files集合中
    if filename.endswith('.jpg') and os.path.splitext(filename)[0] in label_files:
        # 构建完整的源文件路径和目标文件路径
        src_file = os.path.join(source_dir, filename)
        dst_file = os.path.join(target_dir, filename)
        
        # 复制文件
        shutil.copy(src_file, dst_file)

print("所有匹配的文件已复制到'frames'目录。")