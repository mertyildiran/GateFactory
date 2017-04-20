import gate
import time
from itertools import repeat
import random

INPUT_SIZE = 4
OUTPUT_SIZE = 2

TRAINING_DURATION = 1

TRAINING_SAMPLE_SIZE = 4
TESTING_SAMPLE_SIZE = 20

def generate_list_bigger():
    generated_list = []
    for i in repeat(None, INPUT_SIZE):
        generated_list.append(round(random.uniform(0.6, 1.0), PRECISION))
    return generated_list

def generate_list_smaller():
    generated_list = []
    for i in repeat(None, INPUT_SIZE):
        generated_list.append(round(random.uniform(0.0, 0.4), PRECISION))
    return generated_list


print "\n___ GATEFACTORY EASY CLASSIFICATION EXAMPLE ___\n"

print "Create a new GateFactory with input size of " + str(INPUT_SIZE) + " and output size of " + str(OUTPUT_SIZE)
factory = gate.Factory(INPUT_SIZE,OUTPUT_SIZE)

print "\n*** LEARNING ***"

print "\nGenerate The Dataset (" + str(TRAINING_SAMPLE_SIZE) + " Items Long) To Classify The Numbers Bigger & Smaller Than 0.5 & Learn for " + str(TRAINING_DURATION) + " Seconds Each"
for i in range(1,TRAINING_SAMPLE_SIZE):
    if (i % 2) == 0:
        generated_list = generate_list_bigger()
        print "Load Input: " + str(generated_list) + "\tOutput: [1.0, 0.0]\tand wait " + str(TRAINING_DURATION) + " seconds"
        factory.load(generated_list, [1.0, 0.0])
    else:
        generated_list = generate_list_smaller()
        print "Load Input: " + str(generated_list) + "\tOutput: [0.0, 1.0]\tand wait " + str(TRAINING_DURATION) + " seconds"
        factory.load(generated_list, [0.0, 1.0])
    time.sleep(TRAINING_DURATION)



print "\n\n*** TESTING ***"

print "\nTest the factory with random data (" + str(TESTING_SAMPLE_SIZE) + " times)"
error = 0
error_divisor = 0
for i in repeat(None, TESTING_SAMPLE_SIZE):
    binary_random = random.randint(0,1)
    if binary_random == 0:
        generated_list = generate_list_bigger()
        expected = [1.0, 0.0]
    else:
        generated_list = generate_list_smaller()
        expected = [0.0, 1.0]

    factory.load(generated_list)
    time.sleep(TRAINING_DURATION)

    output = factory.output
    error += abs(expected[0] - output[0])
    error += abs(expected[1] - output[1])
    error_divisor += 2

    print "Load Input: " + str(generated_list) + "\tRESULT: " + str(output) + "\tExpected: " + str(expected)



print "\n"
factory.stop()

error = error / error_divisor
print "\nOverall error: " + str(error) + "\n"

print "Exit the program"
