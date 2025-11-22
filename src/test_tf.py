import tensorflow as tf
print("TensorFlow version:", tf.__version__)
try:
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
except:
    print("Could not list GPUs")
