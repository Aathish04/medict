from os import path
import numpy as np
import tensorflow as tf
import pandas as pd

if __name__=="__main__":
    from csvmanager import CSVManager # PLS DO ALL IMPORTS SIMILARLY
else:
    from .csvmanager import CSVManager

csvmanager=CSVManager(CSVFILE=path.abspath(__file__ + "/../../data.csv"))

np.set_printoptions(precision=3, suppress=True)

data=pd.DataFrame(csvmanager.expanded_dataset())
labels=data.pop("MORTALITY")
tf.data.Dataset.from_tensor_slices((dict(data),labels))

