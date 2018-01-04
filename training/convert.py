import sys
import pandas as pd
import math
import os

if len(sys.argv) < 2:
    quit("Require input file")

fileIn = sys.argv[1]

objectLabel = 'Object'

csv = pd.read_csv(fileIn, names = ["image", "id", "label", "xMin", "xMax", "yMin", "yMax", "annotations"],
                  dtype={"annotations": str})

for i, item in csv.iterrows():
    height = csv.iat[i, 6] - csv.iat[i, 5]
    width = csv.iat[i, 4] - csv.iat[i, 3]
    x = csv.iat[i, 3] + math.floor(width / 2)
    y = csv.iat[i, 5] + math.floor(height / 2)

    props = {'label': objectLabel, 'type': 'rectangle'}
    props['coordinates'] = {'height': height, 'width': width, 'x': x, 'y': y}
    csv.iat[i, 7] = [props]

csv.to_csv('annotations.csv')
