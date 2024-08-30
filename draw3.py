import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置支持中文的字体，例如SimHei（黑体）
zh_font = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')

# 数据
data1 = [0.0348,
0.0368,
0.0410,
0.0122,
0.0155,
0.0482,
0.0442,
0.1054,
0.0560,
0.0124,
0.0428]
data2 = [0.0161,
0.0185,
0.0188,
0.0048,
0.0067,
0.0191,
0.0216,
0.0427,
0.0216,
0.0075,
0.0179]
x_labels = range(1, 12)  # x轴标签从1到10

# 创建折线图，并设置图形大小
plt.figure(figsize=(11, 6))  # 调整图形大小，x轴长度为10，y轴长度为6
plt.plot(x_labels, data1, marker='o', markersize=5, label='UV', color='#fc9600')  # 调整markersize参数
plt.plot(x_labels, data2, marker='o', markersize=5, label='PV',color='#e6b800')  # 调整markersize参数

# 设置x轴刻度和标签
plt.xticks(x_labels, [])  # 传递空列表以去掉x轴上的数字
plt.tick_params(axis='x', which='both', bottom=False, top=False)  # 去掉x轴的刻度线

# 设置y轴范围
plt.ylim(0, 0.11)  # y轴从0到0.013

# 添加标题和标签，并设置字体
plt.title('页面产出', fontproperties=zh_font, fontsize=16, fontweight='bold', y=1.05)  # 加大加粗标题并调高位置


# 添加水平虚线
plt.plot([1, 5], [0.0281, 0.0281], color='#fc9600', linestyle='--')  # 0.002的虚线在x轴的1-6
plt.plot([6, 11], [0.0533, 0.0533], color='#fc9600', linestyle='--')  # 0.0067的虚线在x轴的6-12



# 添加水平虚线
plt.plot([1, 5], [0.0130, 0.0130], color='#e6b800', linestyle='--')  # 0.002的虚线在x轴的1-6
plt.plot([6, 11], [0.0217, 0.0217], color='#e6b800', linestyle='--')  # 0.0067的虚线在x轴的6-12




# 在每个数据点上显示乘以100后的数值
for i, (x, y) in enumerate(zip(x_labels, data1)):
    y_offset = 0.0002  # 其他数据点向上偏移
    plt.text(x, y + y_offset, f'{y:.4f}', ha='center', va='bottom', fontsize=10)


for i, (x, y) in enumerate(zip(x_labels, data2)):
    y_offset = 0.0002  # 数据点向上偏移
    plt.text(x, y + y_offset, f'{y:.4f}', ha='center', va='bottom', fontsize=10)

# 添加图例
plt.legend()

# 保存为PDF
plt.savefig('页面产出.png')

# 显示图形
plt.show()