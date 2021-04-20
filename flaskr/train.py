import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf
import random

import numpy as np
import pandas as pd

import tensorflow as tf

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split


def proccess_input(input_string, row_num, input_file):

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


# def csv_standardization(input_string, row_num, input_file):
#   lowercase = tf.strings.lower(input_data)
#   stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
#   return tf.strings.regex_replace(stripped_html,
#                                   '[%s]' % re.escape(string.punctuation),
#                                   '')

# vectorize_layer = TextVectorization(
#     standardize=csv_standardization,
#     max_tokens=10000,
#     output_mode='int',
#     output_sequence_length=250)

# # def learn(input_dictionary):

#     return