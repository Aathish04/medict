from os import path
import numpy as np
import pandas as pd

import tensorflow as tf

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

if __name__=="__main__":
    from csvmanager import CSVManager # PLS DO ALL IMPORTS SIMILARLY
else:
    from .csvmanager import CSVManager

csvmanager=CSVManager(CSVFILE=path.abspath(__file__ + "/../../data.csv"))
expanded_dataset=csvmanager.expanded_dataset()
expanded_csv_path=path.abspath(__file__ + "/../expandeddata.csv")
csvmanager.write_list_od_to_csv(expanded_dataset,datafile=expanded_csv_path)

dataframe=pd.read_csv(expanded_csv_path)
dataframe.columns = dataframe.columns.str.strip().str.replace(' ', '-').str.replace('(', '').str.replace(')', '')
train, test = train_test_split(dataframe, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)

print(len(train), 'train examples')
print(len(val), 'validation examples')
print(len(test), 'test examples')


def df_to_dataset(dataframe, shuffle=True, batch_size=55):
    dataframe = dataframe.copy()
    labels = dataframe.pop('MORTALITY')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds

batch_size = 55
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)


for feature_batch, label_batch in train_ds.take(1):
    print('Every feature:', list(feature_batch.keys()))
    print('A batch of ages:', feature_batch['AGE'])
    print('A batch of targets:', label_batch )

example_batch = next(iter(train_ds))[0]

feature_columns=[feature_column.indicator_column(feature_column.categorical_column_with_vocabulary_list('GENDER', ['MALE', 'FEMALE']))]

NUMERIC_FEATURES = ['AGE','TEMPERATURE',"FEVER","CHEST-TIGHTNESS","DYSPNEA",
"COUGH","CHEST-PAIN","DIARRHEA","FLU","HYPERPYREXIA","HEADACHE",
"BODY-WEAKNESS","APIRETIC","WHEEZING","HYPERPYROXIA","ASTHENIA",
"VOMIT","APYRETIC","PARACETAMOL","AMOXICILLIN","MULTI-DRUG-THERAPY",
"O2-THERAPY","INTUBATION","CPAP-THERAPY","ANTIVIRALS","LEVOFLOXACIN",
"LACTIC-FERMENTS","TOCILIZUMAB","CORTISONE","CEPHALOSPORIN","EBPM",
"LEVOXACIN","ACCLOVIRN","CHOLECALCIFOREL","PLAQUENIL","RITONAVIR-THERAPY",
"HYDROXYCHLOROQUINE","CORTICOSTEROID","ALENOLOL","AZITHROMYCIN","ZITROMAX",
"TACHIPIRINE","ANTIBIOTICS","TAZIOCINBIS"]

for header in NUMERIC_FEATURES:
    feature_columns.append(feature_column.numeric_column(header))

feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

model = tf.keras.Sequential([
  feature_layer,
  layers.Dense(128, activation='relu'),
  layers.Dense(128, activation='relu'),
  layers.Dense(1)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_ds,
          validation_data=val_ds,
          epochs=55)
loss, accuracy = model.evaluate(test_ds)
print("Accuracy", accuracy)