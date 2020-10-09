import gate
import time
from itertools import repeat
import random

INPUT_SIZE = 16
OUTPUT_SIZE = 1
HEAD_START = 20

TRAINING_DURATION = 3

TRAINING_SAMPLE_SIZE = 40
TESTING_SAMPLE_SIZE = 20

def generate_list_class1():
    generated_list = []
    for i in range(1,INPUT_SIZE+1):
        mod = random.randint(2,4)
        if i%mod == 0:
            generated_list.append(1)
        else:
            generated_list.append(0)
    return generated_list
    #return [random.randint(0,1) for b in range(1,INPUT_SIZE+1)]

def generate_list_class2():
    generated_list = []
    for i in range(1,INPUT_SIZE+1):
        mod = random.randint(5,7)
        if i%mod == 0:
            generated_list.append(1)
        else:
            generated_list.append(0)
    return generated_list
    #return [random.randint(0,1) for b in range(1,INPUT_SIZE+1)]


print("\n___ GATEFACTORY EASY CLASSIFICATION EXAMPLE ___\n")

print("Create a new GateFactory with input size of " + str(INPUT_SIZE) + " and output size of " + str(OUTPUT_SIZE))
factory = gate.Factory(INPUT_SIZE,OUTPUT_SIZE,HEAD_START)

print("\n*** LEARNING ***")

print("\nGenerate The Dataset (" + str(TRAINING_SAMPLE_SIZE) + " Items Long) To Classify The Numbers Bigger & Smaller Than 0.5 & Learn for " + str(TRAINING_DURATION) + " Seconds Each")
for i in range(1,TRAINING_SAMPLE_SIZE):
    if (i % 2) == 0:
        generated_list = generate_list_class1()
        print("Load Input: " + str(generated_list) + "\tOutput: [1]\tand wait " + str(TRAINING_DURATION) + " seconds")
        factory.load(generated_list, [1])
    else:
        generated_list = generate_list_class2()
        print("Load Input: " + str(generated_list) + "\tOutput: [0]\tand wait " + str(TRAINING_DURATION) + " seconds")
        factory.load(generated_list, [0])
    time.sleep(TRAINING_DURATION)



print("\n\n*** TESTING ***")

print("\nTest the factory with random data (" + str(TESTING_SAMPLE_SIZE) + " times)")
error = 0
error_divisor = 0
for i in repeat(None, TESTING_SAMPLE_SIZE):
    binary_random = random.randint(0,1)
    if binary_random == 0:
        generated_list = generate_list_class1()
        expected = [1]
    else:
        generated_list = generate_list_class2()
        expected = [0]

    factory.load(generated_list)
    time.sleep(TRAINING_DURATION/2)

    output = factory.output
    #error += abs(expected[0] - output)
    if expected[0] != output:
        error += 1
    error_divisor += 1
    print("Load Input: " + str(generated_list) + "\tRESULT: " + str(output) + "\tExpected: " + str(expected))



print("\n")
factory.stop()

print("\nGateFactory searched the solution over " + str(factory.combination_counter) + " different boolean combinations by going " + str(factory.level_counter) + " levels of deepness\n")

error = float(error) / error_divisor
print("\nOverall error: " + str(error) + "\n")

print("\nThe best boolean expression has been found for your problem is:\n\t" + str(factory.best) + "\n")

print("Depth of this boolean expression is: " + str(factory.best_depth) + "\n")

factory.generate_tex_file()
