import turicreate as tc

modelName = 'output'

# Load the data
data = tc.SFrame('training.sframe')

# Make a train-test split
train_data, test_data = data.random_split(0.8)

# Automatically picks the right model based on your data.
model = tc.object_detector.create(train_data, feature='image', annotations='annotations', max_iterations=1000)

# Save the model for later use in Turi Create
# Important to save in case something after breaks the script
model.save(modelName + '.model')

# Mean average Precision
scores = model.evaluate(data)
print(scores['mean_average_precision'])

# Export for use in CoreML
model.export_coreml(modelName.title() + 'Classifier.mlmodel')
