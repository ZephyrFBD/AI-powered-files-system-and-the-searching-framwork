import pandas as pd
from gensim.models import Doc2Vec
import umap
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import seaborn as sns

# 加载 CSV 文件
csv_path = 'text_files.csv'
df = pd.read_csv(csv_path)

# 加载 Doc2Vec 模型
model_path = './doc2vec_model'
model = Doc2Vec.load(model_path)

# 获取所有文档向量并转换为 NumPy 数组，添加进度条显示
doc_vectors = []
num_documents = len(model.dv)
with tqdm(total=num_documents, desc='Extracting document vectors') as pbar:
    for i in range(num_documents):
        doc_vectors.append(model.dv[i])
        pbar.update(1)  # 更新进度条

doc_vectors = np.array(doc_vectors)

# 使用 UMAP 进行降维
umap_model = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)
umap_vectors = umap_model.fit_transform(doc_vectors)

# 获取标签（使用文件路径作为标签）
labels = df['File Path'].tolist()

# 为标签创建颜色字典
unique_labels = list(set(labels))
color_palette = sns.color_palette("hsv", len(unique_labels))
label_to_color = {label: color_palette[i] for i, label in enumerate(unique_labels)}

# 根据标签分配颜色
colors = [label_to_color[label] for label in labels]

# 绘制带颜色区分的 UMAP 可视化图
plt.figure(figsize=(10, 8))
plt.scatter(umap_vectors[:, 0], umap_vectors[:, 1], c=colors, marker='.')
plt.title('UMAP Visualization of Document Vectors with Color-Coded Labels')
plt.xlabel('UMAP Component 1')
plt.ylabel('UMAP Component 2')
plt.show()