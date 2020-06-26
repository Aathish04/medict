from os import path,remove
import numpy as np
import pandas as pd
import PySimpleGUI as sg
import tensorflow as tf

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

if __name__=="__main__":
    from csvmanager import CSVManager # PLS DO ALL IMPORTS SIMILARLY
else:
    from .csvmanager import CSVManager

class Predictor(object):
    TEXTFONT="serif"
    FONTSIZE=14
    FIELDS=[]
    FIELDS=["mAGE","mGENDER","mSYMPTOMS","mTIMES","mTEMPERATURE","mMEDICATION"]
    layout=[
        [
            sg.Frame(
                "Data",[
                [sg.Text("AGE:",font=(TEXTFONT,FONTSIZE)), sg.Input(key="mAGE",font=(TEXTFONT,FONTSIZE))],
                [sg.Text("GENDER:",font=(TEXTFONT,FONTSIZE)),sg.Input(key="mGENDER",font=(TEXTFONT,FONTSIZE))],
                [
                    sg.Text("SYMPTOMS LIST:",font=(TEXTFONT,FONTSIZE)),
                    sg.Input(key="mSYMPTOMS",font=(TEXTFONT,FONTSIZE),size=(30,1)),
                    sg.Text("TIME LIST:",font=(TEXTFONT,FONTSIZE)),
                    sg.Input(key="mTIMES",font=(TEXTFONT,FONTSIZE),size=(30,1))
                    ],
                [sg.Text("TEMPERATURE IN C:",font=(TEXTFONT,FONTSIZE)),sg.Input(key="mTEMPERATURE",font=(TEXTFONT,FONTSIZE))],
                [
                    sg.Text("MEDICATION GIVEN:",font=(TEXTFONT,FONTSIZE)),sg.Input(key="mMEDICATION",font=(TEXTFONT,FONTSIZE)),
                    ],
                [sg.Text("SURVIVAL RATE:",font=(TEXTFONT,FONTSIZE)),sg.Text("                    ",key="mMORTALITY",font=(TEXTFONT,FONTSIZE)),
                sg.Text(" %",font=(TEXTFONT,FONTSIZE))],
                [sg.Button("ESTIMATE")]
                ]),
            ]
        ]

    def df_to_dataset(self,dataframe, shuffle=True, batch_size=55):
        dataframe = dataframe.copy()
        labels = dataframe.pop('MORTALITY')
        ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
        if shuffle:
            ds = ds.shuffle(buffer_size=len(dataframe))
        ds = ds.batch(batch_size)
        return ds

    def __init__(self):
        csvmanager=CSVManager(CSVFILE=path.abspath(__file__ + "/../../data.csv"))
        expanded_dataset=csvmanager.expanded_dataset()

        dataframe=pd.DataFrame(expanded_dataset)
        dataframe.columns = dataframe.columns.str.strip().str.replace(' ', '-').str.replace('(', '').str.replace(')', '')
        train, test = train_test_split(dataframe, test_size=0.2)
        train, val = train_test_split(train, test_size=0.2)

        batch_size = len(csvmanager.records_from_csv())
        train_ds = self.df_to_dataset(train, batch_size=batch_size)
        val_ds = self.df_to_dataset(val, shuffle=False, batch_size=batch_size)
        test_ds = self.df_to_dataset(test, shuffle=False, batch_size=batch_size)
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

        self.model = tf.keras.Sequential([
            feature_layer,
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(1)
        ])

        self.model.compile(optimizer='adam',
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy'])

        self.model.fit(train_ds,
                validation_data=val_ds,
                epochs=55)

        loss, accuracy = self.model.evaluate(test_ds)

    def predict(self, lod):
        dataframe=pd.DataFrame(lod)
        dataframe.columns = dataframe.columns.str.strip().str.replace(' ', '-').str.replace('(', '').str.replace(')', '')
        input_dataset = self.df_to_dataset(dataframe, batch_size=len(lod))
        predictions = self.model.predict(input_dataset)
        for prediction in predictions:
            prediction = tf.sigmoid(prediction).numpy()
            return prediction

if __name__=="__main__":
    predictor=Predictor()
    csvmanager=CSVManager(CSVFILE=path.abspath(__file__ + "/../../data.csv"))
    print("Survival Rate: ",predictor.predict(csvmanager.expanded_dataset()[:1]))