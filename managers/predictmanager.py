from os import path
import numpy as np
import tensorflow as tf
import functools

if __name__=="__main__":
    from csvmanager import CSVManager # PLS DO ALL IMPORTS SIMILARLY
else:
    from .csvmanager import CSVManager
csvmanager=CSVManager(CSVFILE=path.abspath(__file__ + "/../../data.csv"))

class PackNumericFeatures(object):
  def __init__(self, names):
    self.names = names

  def __call__(self, features, labels):
    numeric_features = [features.pop(name) for name in self.names]
    numeric_features = [tf.cast(feat, tf.float32) for feat in numeric_features]
    numeric_features = tf.stack(numeric_features, axis=-1)
    features['numeric'] = numeric_features

    return features, labels

def show_batch(dataset):
  for batch, label in dataset.take(1):
    for key, value in batch.items():
      print("{:20s}: {}".format(key,value.numpy()))

def normalize_numeric_data(data, mean, std):
    return (data-mean)/std

expanded_dataset=csvmanager.expanded_dataset()
expanded_csv_path=path.abspath(__file__ + "/../expandeddata.csv")
csvmanager.write_list_od_to_csv(expanded_dataset,datafile=expanded_csv_path)

raw_train_data = tf.data.experimental.make_csv_dataset(
      expanded_csv_path,
      batch_size=len(csvmanager.records_from_csv()),
      label_name="MORTALITY",
      na_value="UNKNOWN",
      num_epochs=1,
      ignore_errors=True)

raw_test_data = tf.data.experimental.make_csv_dataset(
      expanded_csv_path,
      batch_size=len(csvmanager.records_from_csv()),
      label_name="MORTALITY",
      na_value="UNKNOWN",
      num_epochs=1,
      ignore_errors=True)

NUMERIC_FEATURES = ['AGE','TEMPERATURE',"FEVER","CHEST TIGHTNESS","DYSPNEA",
"COUGH","CHEST PAIN","DIARRHEA","FLU","HYPERPYREXIA","HEADACHE",
"BODY WEAKNESS","APIRETIC","WHEEZING","HYPERPYROXIA","ASTHENIA",
"VOMIT","APYRETIC","PARACETAMOL","AMOXICILLIN","MULTI-DRUG THERAPY",
"O2 THERAPY","INTUBATION","CPAP THERAPY","ANTIVIRALS","LEVOFLOXACIN",
"LACTIC FERMENTS","TOCILIZUMAB","CORTISONE","CEPHALOSPORIN","EBPM",
"LEVOXACIN","ACCLOVIRN","CHOLECALCIFOREL","PLAQUENIL","RITONAVIR THERAPY",
"HYDROXYCHLOROQUINE","CORTICOSTEROID","ALENOLOL","AZITHROMYCIN","ZITROMAX",
"TACHIPIRINE","ANTIBIOTICS","TAZIOCINBIS"]

packed_train_data = raw_train_data.map(
    PackNumericFeatures(NUMERIC_FEATURES))

packed_test_data = raw_test_data.map(
    PackNumericFeatures(NUMERIC_FEATURES))

example_batch, labels_batch = next(iter(raw_train_data))

MEAN=[sum(example_batch[entry].numpy())/len(example_batch[entry].numpy())
    for entry in example_batch if entry in NUMERIC_FEATURES]

STD=[np.std(example_batch[entry].numpy())
    for entry in example_batch if entry in NUMERIC_FEATURES]

normalizer = functools.partial(normalize_numeric_data, mean=MEAN, std=STD)

numeric_column = tf.feature_column.numeric_column('numeric', normalizer_fn=normalizer, shape=[len(NUMERIC_FEATURES)])

numeric_columns = [numeric_column]

CATEGORIES = {
    'GENDER': ['MALE', 'FEMALE']
}
categorical_columns = []

for feature, vocab in CATEGORIES.items():
    cat_col = tf.feature_column.categorical_column_with_vocabulary_list(
        key=feature, vocabulary_list=vocab)
    categorical_columns.append(tf.feature_column.indicator_column(cat_col))

preprocessing_layer = tf.keras.layers.DenseFeatures(categorical_columns+numeric_columns)

