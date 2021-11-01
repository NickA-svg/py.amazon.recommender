import os
import csv
import sys
import re

from surprise import Dataset
from surprise import Reader

from collections import defaultdict
import numpy as np

class Electronics:

    productId_to_name = {}
    name_to_productId = {}
    ratingsPath = '/Users/nick.aristidou@convexin.com/Documents/Projects/Python/py.amazon.rec/data/ratings_Electronics_small.csv'
    productsPath = '/Users/nick.aristidou@convexin.com/Documents/Projects/Python/py.amazon.rec/data/products_small.csv'
    
    def loadElectronics(self):

        # Look for files relative to the directory we are running from
        os.chdir(os.path.dirname(sys.argv[0]))

        ratingsDataset = 0
        self.productId_to_name = {}
        self.name_to_productId = {}

        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)

        with open(self.productsPath, newline='', encoding='ISO-8859-1') as csvfile:
                productReader = csv.reader(csvfile)
                next(productReader)  #Skip header line
                for row in productReader:
                    productId = row[0]
                    productName = row[1]
                    self.productId_to_name[productId] = productName
                    self.name_to_productId[productName] = productId

        return ratingsDataset

    def getUserRatings(self, user):
        userRatings = []
        hitUser = False
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                userID = row[0]
                if (user == userID):
                    productId = row[1]
                    rating = float(row[2])
                    userRatings.append((productId, rating))
                    hitUser = True
                if (hitUser and (user != userID)):
                    break

        return userRatings

    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                productId = row[1]
                ratings[productId] += 1
        rank = 1
        for productId, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[productId] = rank
            rank += 1
        return rankings
    
    def getProductName(self, productId):
        if productId in self.productId_to_name:
            return self.productId_to_name[productId]
        else:
            return ""
        
    def getProductID(self, productName):
        if productName in self.name_to_productId:
            return self.name_to_productId[productName]
        else:
            return 0