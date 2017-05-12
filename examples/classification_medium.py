import pickle
import numpy as np
import os
import cv2
import random
import gate
from itertools import repeat
import sys
import time

INPUT_SIZE = 32 * 32 * 3
OUTPUT_SIZE = 1
HEAD_START = 10

TRAINING_DURATION = 3

TRAINING_SAMPLE_SIZE = 200
TESTING_SAMPLE_SIZE = 100

def load_batch(fpath, label_key='labels'):
    # Internal utility for parsing CIFAR data
    f = open(fpath, 'rb')
    d = pickle.load(f)
    f.close()
    data = d['data']
    labels = d[label_key]

    data = data.reshape(data.shape[0], 3, 32, 32)
    return data, labels

def show_output(factory,testing=False):
    global error
    global error_divisor

    if testing:
        time.sleep(TRAINING_DURATION/2)
        output = factory.output

        error += abs(testing[0] - output)
        error_divisor += 1
        print "RESULT: " + str(output) + "\tExpected: " + str(testing)
    else:
        time.sleep(TRAINING_DURATION)
        output = factory.output
        #print "Output: " + str(output)


print "\n___ GATEFACTORY MEDIUM CLASSIFICATION (CATDOG) EXAMPLE ___\n"

print "Load CIFAR-10 dataset"
print "Pick random " + str(TRAINING_SAMPLE_SIZE) + " cat and " + str(TRAINING_SAMPLE_SIZE) + " dog images from the CIFAR-10 data batch to TRAIN the factory"
print "Pick random " + str(TESTING_SAMPLE_SIZE) + " cat and " + str(TESTING_SAMPLE_SIZE) + " dog images from the CIFAR-10 test batch to TEST the factory"

# Load CIFAR-10 dataset
path = './examples/cifar-10-batches-py/'
num_train_samples = 50000

x_train = np.zeros((num_train_samples, 3, 32, 32), dtype='uint8')
y_train = np.zeros((num_train_samples,), dtype='uint8')

for i in range(1, 6):
    fpath = os.path.join(path, 'data_batch_' + str(i))
    data, labels = load_batch(fpath)
    x_train[(i - 1) * 10000: i * 10000, :, :, :] = data
    y_train[(i - 1) * 10000: i * 10000] = labels

fpath = os.path.join(path, 'test_batch')
x_test, y_test = load_batch(fpath)

y_train = np.reshape(y_train, (len(y_train), 1))
y_test = np.reshape(y_test, (len(y_test), 1))

# channels last
x_train = x_train.transpose(0, 2, 3, 1)
x_test = x_test.transpose(0, 2, 3, 1)

# Generate the training data
cats = []
for i in range(0, num_train_samples - 1):
    if y_train[i] == 3:
        cats.append(x_train[i])

dogs = []
for i in range(0, num_train_samples - 1):
    if y_train[i] == 5:
        dogs.append(x_train[i])


# Generate the testing data
test_cats = []
for i in range(0, num_train_samples/5 - 1):
    if y_test[i] == 3:
        test_cats.append(x_test[i])

test_dogs = []
for i in range(0, num_train_samples/5 - 1):
    if y_test[i] == 5:
        test_dogs.append(x_test[i])


print "Create a new GateFactory with input size of " + str(INPUT_SIZE) + " and output size of " + str(OUTPUT_SIZE)
factory = gate.Factory(INPUT_SIZE,OUTPUT_SIZE,HEAD_START)

error = 0
error_divisor = 0

print "\n*** LEARNING ***"

print "\nMap " + str(TRAINING_SAMPLE_SIZE/2) + " Different Cat Images to Color Blue & " + str(TRAINING_SAMPLE_SIZE/2) + " Different Dog Images to Color Red - Training Duration: " + str(TRAINING_DURATION * TRAINING_SAMPLE_SIZE) + " seconds (OpenCV latency not included)"
for i in range(0,TRAINING_SAMPLE_SIZE):
    if (i % 2) == 0:
        cat = random.sample(cats, 1)[0]
        cat_normalized = np.true_divide(cat, 255).flatten()
        cat_binary = (cat_normalized > 0.5).astype(int)
        factory.load(cat_binary,[1])
    else:
        dog = random.sample(dogs, 1)[0]
        dog_normalized = np.true_divide(dog, 255).flatten()
        dog_binary = (dog_normalized > 0.5).astype(int)
        factory.load(dog_binary,[0])
    show_output(factory)


print "\nTest " + str(TESTING_SAMPLE_SIZE/2) + " Different Cat Images & " + str(TESTING_SAMPLE_SIZE/2) + " Different Dog Images - Testing Duration: " + str(TRAINING_DURATION * TESTING_SAMPLE_SIZE) + " seconds (OpenCV latency not included)"
for i in range(0,TESTING_SAMPLE_SIZE):
    binary_random = random.randint(0,1)
    if binary_random == 0:
        cat = random.sample(test_cats, 1)[0]
        cat_normalized = np.true_divide(cat, 255).flatten()
        cat_binary = (cat_normalized > 0.5).astype(int)
        factory.load(cat_binary)
        show_output(factory,[1])
    else:
        dog = random.sample(test_dogs, 1)[0]
        dog_normalized = np.true_divide(dog, 255).flatten()
        dog_binary = (dog_normalized > 0.5).astype(int)
        factory.load(dog_binary)
        show_output(factory,[0])


print ""

factory.stop()
cv2.destroyAllWindows()

print "\nGateFactory searched the solution over " + str(factory.combination_counter) + " different boolean combinations by going " + str(factory.level_counter) + " levels of deepness\n"

print "\nOverall error: " + str(float(error)/error_divisor) + "\n"

print "\nThe best boolean expression has been found for your problem is:\n\t" + str(factory.best) + "\n"

print "Depth of this boolean expression is: " + str(factory.best_depth) + "\n"

factory.generate_tex_file()
