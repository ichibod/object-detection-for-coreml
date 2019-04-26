import turicreate as tc
from turicreate import SFrame
from turicreate import SArray
import pandas as pd
import math
import sys

if len(sys.argv) < 2:
    quit("Require input file")

fileIn = sys.argv[1]

pathToImages = 'images'

def findLabel(path):
    # pull label from image path i.e. images/_label_/image.jpg
    return path.split('/')[1]

def annotation(row):
    # create annotation
    height = row['yMax'] - row['yMin']
    width = row['xMax'] - row['xMin']
    x = row['xMin'] + math.floor(width / 2)
    y = row['yMin'] + math.floor(height / 2)

    props = {'label': item['label'], 'type': 'rectangle'}
    props['coordinates'] = {'height': height, 'width': width, 'x': x, 'y': y}
    return [props]

# Load images
data = tc.image_analysis.load_images(pathToImages, with_path=True)

csv = pd.read_csv(fileIn, names = ["image", "id", "label", "xMin", "xMax", "yMin", "yMax"])
# From the path-name, create a label column
data['label'] = list(map(findLabel, data['path']))

# the data is in no particular order, so we have to loop it to match
annotations = []
count = 0
prev = 0
for j, item in enumerate(data):
    prev = count
    label = str(item['path'].split('/')[2])
    for i, row in csv.iterrows():
        if str(row['image']) == label:
            # match image name in path
            annotations.append(annotation(row))
            count += 1
            break
    if prev == count:
        # Figure out which item did not match
        print(item)

# make an array from the annotations data, matching the data order
data['annotations'] = SArray(data=annotations, dtype=list)

# Save the data for future use
data.save('training.sframe')

data['image_with_ground_truth'] = tc.object_detector.util.draw_bounding_boxes(data["image"], data["annotations"])

# Explore interactively
data.explore()
