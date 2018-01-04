import turicreate as tc
from turicreate import SFrame
from turicreate import SArray
import pandas as pd
import os

objectLabel = 'Object'
pathToImages = 'images'

# Load images
data = tc.image_analysis.load_images(pathToImages, with_path=True)
# data = data.add_row_number('row')
csv = pd.read_csv('annotations.csv')
# From the path-name, create a label column
data['label'] = data['path'].apply(lambda path: objectLabel if objectLabel in path else 'misc')

# the data is in no particular order, so we have to loop it to match
# we also have the 'misc' images, which won't have an annotation, to skip
annotations = []
for j, item in enumerate(data):
    if item['label'] != objectLabel:
        annotations.append([]) # use empty array for 'misc' folder
        continue
    for i, row in csv.iterrows():
        if str(row['image']) == str(os.path.split(item['path'])[1]):
            # match image name in path
            annotations.append(eval(row['annotations']))
            break

# print(data.num_rows())
# print(len(annotations))
# make an array from the annotations data, matching the data order
data['annotations'] = SArray(data=annotations, dtype=list)

# Save the data for future use
data.save('training.sframe')

data['image_with_ground_truth'] = tc.object_detector.util.draw_bounding_boxes(data["image"], data["annotations"])

# Explore interactively
data.explore()
