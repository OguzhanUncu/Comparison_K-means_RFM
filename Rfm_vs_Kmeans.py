import numpy as np
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from yellowbrick.cluster import KElbowVisualizer
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from sklearn.preprocessing import StandardScaler
import argparse

import warnings
pd.pandas.set_option('display.max_columns', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr',False)

df_ = pd.read_excel("online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")
df = df_.copy()

parser = argparse.ArgumentParser()
parser.add_argument("--save", dest="save" , action="store_true" , help="for saving the output")
parser.set_defaults(save=False)

args = parser.parse_args()

def rfm_vs_kmean(dataframe):
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True) # we will focus on classes
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    today_date = dt.datetime(2011, 12, 11)
    metrics = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    metrics.columns = ['recency', 'frequency', "monetary"]
    metrics = metrics[(metrics['monetary'] > 0)]

    rfm = pd.DataFrame()
    rfm["recency_score"] = pd.qcut(metrics['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(metrics["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(metrics['monetary'], 5, labels=[1, 2, 3, 4, 5])

    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))

    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm[["recency", "frequency", "monetary"]] = metrics[["recency", "frequency", "monetary"]]

    #############################################################
    # K-MEANS
    #############################################################

    k_means = metrics.copy()

    sc = MinMaxScaler((0, 1))
    k_means = sc.fit_transform(k_means)

    k_means = KMeans(n_clusters=10).fit(k_means)

    kumeler = k_means.labels_ + 1

    final_k_means = metrics[["recency", "frequency", "monetary"]]
    final_k_means["kumeler"] = kumeler

    rfm.drop(["recency_score", "frequency_score", "monetary_score", "RFM_SCORE"], inplace=True, axis=1)
    rfm_vs_kmean = pd.DataFrame()
    rfm_vs_kmean = rfm.copy()
    rfm_vs_kmean["K_means_classes"] = final_k_means["kumeler"]

    return rfm_vs_kmean

rfm_vs_kmean = rfm_vs_kmean(df)

#rfm_vs_kmean.groupby(["segment","K_means_classes"]).agg(["mean", "count"])

if args.save:
    rfm_vs_kmean.to_excel("rfm_vs_kmean.xlsx")
# We can save our final data to excel with argparse