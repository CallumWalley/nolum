import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf
import random

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization


def proccessInput(input_string, row_num, input_file):

    input_list = input_string.split(",")
    output_dictionary = {
        "raw_string":input_string,
        "date":input_list[6],
        "time":"",
        "amount":input_list[5],
        "from":input_list[2],
        "thing":"",
        "type":input_list[0],
        "category":"",
        "tags":"",
        "confidence":random.uniform(0, 1),
        "input":input_file,
        "valid":True
    }
    return output_dictionary


def learn(input_dictionary):

    return