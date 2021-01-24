"""
    ./managers/predictmanager.py

    This File contains the object Predictor which handles all functions
    related to predicting survival rate of a patient that may arise during
    the usage of the main program.

    This file may be run on its own to test the features of Predictor separately.
"""

from os import path
from functools import reduce

import PySimpleGUI as sg

if __name__=="__main__":
    from csvmanager import CSVManager
    from _config import get_settings_config
else:
    from .csvmanager import CSVManager
    from ._config import get_settings_config

class Predictor(object):
    TEXTFONT="serif"
    FONTSIZE=get_settings_config()["fontsize"]
    FIELDS=[]
    FIELDS=["pAGE","pGENDER","pSYMPTOMS","pTIMES","pTEMPERATURE","pMEDICATION"]
    layout=[
        [
            sg.Frame(
                "Data",[
                [sg.Text("AGE:",font=(TEXTFONT,FONTSIZE)), sg.Input(key="pAGE",font=(TEXTFONT,FONTSIZE))],
                [sg.Text("GENDER:",font=(TEXTFONT,FONTSIZE)),sg.Input(key="pGENDER",font=(TEXTFONT,FONTSIZE))],
                [
                    sg.Text("SYMPTOMS LIST:",font=(TEXTFONT,FONTSIZE)),
                    sg.Input(key="pSYMPTOMS",font=(TEXTFONT,FONTSIZE),size=(30,1)),
                    sg.Text("TIME LIST:",font=(TEXTFONT,FONTSIZE)),
                    sg.Input(key="pTIMES",font=(TEXTFONT,FONTSIZE),size=(30,1))
                    ],
                [sg.Text("TEMPERATURE IN C:",font=(TEXTFONT,FONTSIZE)),sg.Input(key="pTEMPERATURE",font=(TEXTFONT,FONTSIZE))],
                [
                    sg.Text("MEDICATION GIVEN:",font=(TEXTFONT,FONTSIZE)),sg.Input(key="pMEDICATION",font=(TEXTFONT,FONTSIZE)),
                    ],
                [sg.Text("SURVIVAL RATE:",font=(TEXTFONT,FONTSIZE)),sg.Text("      ",key="pMORTALITY",font=(TEXTFONT,FONTSIZE)),
                sg.Text("   %",font=(TEXTFONT,FONTSIZE))],
                [
                    sg.Button("ESTIMATE"),
                    sg.Text(
                        "Acceptable Deviance:",
                        font=(TEXTFONT,FONTSIZE)),
                    sg.Slider(range=(0,50),
                        default_value=10,
                        key="DEVIANCE",
                        size=(20,15),
                        orientation='horizontal',
                        font=('Helvetica', 12)
                        )
                    ]
                ]),
            ]
        ]

    def __init__(self,csvfile=path.abspath(__file__ + "/../../data.csv")):
        self.csvmanager=CSVManager(CSVFILE=csvfile)
        expanded_dataset=self.csvmanager.expanded_dataset()

    def predict(self, datadict, allowed_deviation = 5):
        """
        Return a percentage survival rate pertaining to the given data.
        Works by calculating probability of each individiual property of the patient
        and multiplying them together.

        """
        ex_ds = self.csvmanager.expanded_dataset()
        prob_dict = {key:0 for key in datadict.keys()}
        count_dict = {key:0 for key in datadict.keys()}
        for key in datadict:
            for entry in ex_ds:
                if key not in ["GENDER","MORTALITY"] :
                    minim = datadict[key] - allowed_deviation
                    maxim = datadict[key] + allowed_deviation
                    if entry[key] != 0 and minim <= entry[key] <= maxim:
                        count_dict[key]+=1
                        prob_dict[key] +=1 if entry["MORTALITY"] == 1 else 0
                elif key == "MORTALITY":
                    pass
                else:
                    count_dict[key]+=1
                    if entry[key] == datadict[key]:
                        prob_dict[key] += 1
        for key in prob_dict:
            prob_dict[key] = prob_dict[key]/count_dict[key] if prob_dict[key] !=0 else 1
        return (reduce(lambda x, y: x * y, prob_dict.values() )*100)

if __name__=="__main__":
    predictor=Predictor()
    csvmanager=CSVManager(CSVFILE=path.abspath(__file__ + "/../../data.csv"))
    print(
        "Survival Rate: ",
        predictor.predict(
            (
                {
                    key:value for key,value in csvmanager.expanded_dataset()[1].items() if key != "MORTALITY"}
                )
            )
    )
