import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
sns.set_style(style="whitegrid")

#数据读取，清洗，处理
df = pd.read_csv('./data/new_data.csv')
def main1(x):
    x1 = str(x).split(" ")
    x1 = x1[-1]
    x2 = str(x1).split(":")
    x2 = x2[1]
    return x2

df['sum_time'] = df['sum_time'].apply(main1)
data = pd.DataFrame()
data['sum_time'] = df['sum_time']
data['distance(单位:km)'] = df['distance(单位:km)']
data['week'] = df['week']
data['hour'] = df['hour']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

# 用PCA进行降维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# 定义一个空列表，用来存储不同的簇类数目下的轮廓系数
sil_scores = []
# 定义一个范围，用来尝试不同的簇类数目，这里我们从2到10
range_n_clusters = range(2, 22)

# 对每个簇类数目，用K-MEANS进行聚类，并计算轮廓系数，然后添加到列表中
#轮廓系数（silhouette coefficient）来评估不同的簇类数目。轮廓系数是一个介于-1和1之间的值，它反映了每个数据点与自己所属的簇类和其他簇类的相似度。轮廓系数越高，表示聚类越好
for n_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(X_pca)
    y_pred = kmeans.predict(X_pca)
    sil_score = silhouette_score(X_pca, y_pred)
    sil_scores.append(sil_score)

# 绘制轮廓系数曲线
plt.plot(range_n_clusters, sil_scores)
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette coefficient')
plt.title('Silhouette coefficient curve for Iris dataset')
plt.show()

df1 = pd.DataFrame()
df1['簇类'] = range_n_clusters
df1['轮廓系数'] = sil_scores
df1.to_csv('./data/轮廓系数.csv',encoding='utf-8-sig',index=False)

# 用K-MEANS进行聚类
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(X_pca)
y_pred = kmeans.predict(X_pca)
df['聚类结果'] = y_pred
df.to_csv('./data/聚类结果.csv',encoding='utf-8-sig',index=False)
plt.figure(figsize=(16,9),dpi=500)
# 可视化结果
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_pred, cmap='viridis')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.title('K-MEANS')
plt.savefig('./data/k-means聚类效果图.png')
plt.show()