import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
import datetime as dt
from yellowbrick.cluster import KElbowVisualizer
from sklearn.preprocessing import MinMaxScaler
os.chdir(r"C:\Users\user\PycharmProjects\dsm\Data")

df = pd.read_excel("online_retail_II.xlsx",sheet_name="Year 2010-2011")

df["TotalPrice"] = df["Quantity"] * df["Price"]
df.dropna(inplace=True)
df = df[~df["Invoice"].str.contains("C", na=False)]

today_date = dt.datetime(2011, 12, 11)
metrics = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
metrics.columns = ['recency', 'frequency', "monetary"]
metrics = metrics[(metrics['monetary'] > 0)]

################################
# OPTİMUM CLASS NUMBER
################################

sc = MinMaxScaler((0, 1))
metrics = sc.fit_transform(metrics)

kmeans = KMeans()
ssd = []
K = range(1, 30)

for k in K:
    kmeans = KMeans(n_clusters=k).fit(metrics)
    ssd.append(kmeans.inertia_)

plt.plot(K, ssd, "bx-")
plt.xlabel("Farklı K Değerlerine Karşılık Uzaklık Artık Toplamları")
plt.title("Optimum Küme sayısı için Elbow Yöntemi")
plt.show()

kmeans = KMeans()
elbow = KElbowVisualizer(kmeans, k=(2, 20))
elbow.fit(metrics)
elbow.show()

# According to the elbow visualizer, the number of classes should be 6
# fit again

kmeans = KMeans(n_clusters=elbow.elbow_value_).fit(metrics)

kumeler = kmeans.labels_

metrics = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
metrics.columns = ['recency', 'frequency', "monetary"]
metrics = metrics[(metrics['monetary'] > 0)]

metrics["Classes"] = kumeler + 1

metrics.groupby(["Classes"]).agg(["mean", "count"])
metrics.to_excel("K-means.xlsx")