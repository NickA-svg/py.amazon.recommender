import pandas as pd
from dfply import *

def small_data(products=50,users=20):
    df = pd.read_csv("/Users/nick.aristidou@convexin.com/Documents/Projects/Python/py.amazon.rec/data/ratings_Electronics.csv", names=['userId', 'productId','rating','timestamp'])

    #filter for products with 50 or more ratings 
    new_df=df.groupby("productId").filter(lambda x:x['rating'].count() >= products)

    #filter for users that have given 20 or more reviews
    new_df=new_df.groupby("userId").filter(lambda x:x['rating'].count() >= users)

    #export to csv
    new_df.to_csv("/Users/nick.aristidou@convexin.com/Documents/Projects/Python/py.amazon.rec/data/ratings_Electronics_small.csv",index=False)
    print("new small subset data saved, with products with > {} ratings and users with > {} ratings. Data shape is {}".format(products,users,new_df.shape))