import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import roc_curve,auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

df = pd.read_csv('./data/情感标签.csv')
def main(x):
    x1 = str(x)
    if x1 == 'pos':
        return 1
    else:
        return 0

df['情感类型'] = df['情感类型'].apply(main)
stop_words = []
with open("./data/stopwords_cn.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        stop_words.append(line.strip())

train_x, test_x, train_y, test_y = train_test_split(df['分词'], df['情感类型'], test_size=0.3, random_state=8675309)

# 计算单词权重
tf = TfidfVectorizer(stop_words=stop_words, max_df=0.5)

train_features = tf.fit_transform(train_x)
# 上面fit过了，这里transform
test_features = tf.transform(test_x)

# 多项式贝叶斯分类器
clf_nb = MultinomialNB(alpha=0.001).fit(train_features, train_y)
nb_labels = clf_nb.predict(test_features)

#svm分类器
clf_svm = svm.SVC().fit(train_features, train_y)
svm_labels = clf_svm.predict(test_features)

#决策树分类器 ID3决策树
clf_tree = DecisionTreeClassifier(criterion='entropy').fit(train_features, train_y)
tree_labels = clf_tree.predict(test_features)

clf_random = RandomForestClassifier(n_estimators=10000, n_jobs=-1).fit(train_features, train_y)
random_labels = clf_random.predict(test_features)
accuracy1 = round(metrics.accuracy_score(test_y,nb_labels),4)
accuracy2 = round(metrics.accuracy_score(test_y,svm_labels), 4)
accuracy3 = round(metrics.accuracy_score(test_y,tree_labels), 4)
accuracy4 = round(metrics.accuracy_score(test_y,random_labels), 4)

precision1 = round(metrics.precision_score(test_y,nb_labels, average='micro'), 4)
precision2 = round(metrics.precision_score(test_y,svm_labels, average='micro'), 4)
precision3 = round(metrics.precision_score(test_y,tree_labels, average='micro'), 4)
precision4 = round(metrics.precision_score(test_y,random_labels, average='micro'), 4)

recall1 = round(metrics.recall_score(test_y,nb_labels, average='micro'), 4)
recall2 = round(metrics.recall_score(test_y,svm_labels, average='micro'), 4)
recall3 = round(metrics.recall_score(test_y,tree_labels, average='micro'), 4)
recall4 = round(metrics.recall_score(test_y,random_labels, average='micro'), 4)

f1_1 = round(metrics.f1_score(test_y,nb_labels, average='weighted'), 4)
f1_2 = round(metrics.f1_score(test_y,svm_labels, average='weighted'), 4)
f1_3 = round(metrics.f1_score(test_y,tree_labels, average='weighted'), 4)
f1_4 = round(metrics.f1_score(test_y,random_labels, average='weighted'), 4)


fpr1, tpr1, thresholds1 = roc_curve(test_y,nb_labels)
fpr2, tpr2, thresholds2 = roc_curve(test_y,svm_labels)
fpr3, tpr3, thresholds3 = roc_curve(test_y,tree_labels)
fpr4, tpr4, thresholds4 = roc_curve(test_y,random_labels)
roc_auc1 = auc(fpr1, tpr1)
roc_auc2 = auc(fpr2, tpr2)
roc_auc3 = auc(fpr3, tpr3)
roc_auc4 = auc(fpr4, tpr4)


#绘制多组对比roc曲线
color=["darkorange","navy","red","green"]
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(12,12),dpi=500)
lw = 2
plt.plot(fpr1, tpr1, color=color[0], lw=lw, label='贝叶斯'+' (AUC = %0.3f)' % roc_auc1)
plt.plot(fpr2, tpr2, color=color[1], lw=lw, label='SVM'+' (AUC = %0.3f)' % roc_auc2)
plt.plot(fpr3, tpr3, color=color[2], lw=lw, label='决策树'+' (AUC = %0.3f)' % roc_auc3)
plt.plot(fpr4, tpr4, color=color[3], lw=lw, label='随机森林'+' (AUC = %0.3f)' % roc_auc4)
plt.plot([0, 1], [0, 1], color='black', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate',fontsize=20)
plt.ylabel('True Positive Rate',fontsize=20)
plt.title('Receiver operating characteristic Curve',fontsize=20)
plt.legend(loc="lower right",fontsize=20)
plt.savefig("./static/img/roc_curve.png")



data = pd.DataFrame()
data['准确率'] = ['贝叶斯准确率', 'SVM准确率', '决策树准确率', '随机森林准确率']
data['准确率_score'] = [accuracy1, accuracy2, accuracy3, accuracy4]
data['精确率'] = ['贝叶斯精确率', 'SVM精确率', '决策树精确率', '随机森林精确率']
data['精确率_score'] = [precision1, precision2, precision3, precision4]
data['召回率'] = ['贝叶斯召回率', 'SVM召回率', '决策树召回率', '随机森林召回率']
data['召回率_score'] = [recall1, recall2, recall3, recall4]
data['F1值'] = ['贝叶斯F1值', 'SVMF1值', '决策树F1值', '随机森林F1值']
data['F1值_score'] = [f1_1, f1_2, f1_3, f1_4]

data.to_csv('./data/score.csv',encoding='utf-8-sig')