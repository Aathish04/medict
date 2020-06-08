# AATHISH SIVASUBRAHMANIAN

import os
import csv
import PySimpleGUI as sg

os.chdir(os.path.abspath(os.path.dirname(__file__)))

sg.theme('DarkGrey')

elements=[
    [sg.Text("AGE:"), sg.Input(key="AGE")],
    [sg.Text("GENDER:"), sg.Input(key="GENDER")],
    [sg.Text("SYMPTOMS LIST:"), sg.Input(key="SYMPTOMS"), sg.Text("TIME LIST"), sg.Input(key="TIMES")],
    [sg.Text("TEMPERATURE IN C:"), sg.Input(key="TEMPERATURE")],
    [sg.Text("MEDICATION GIVEN:"), sg.Input(key="MEDICATION")],
    [sg.Button(button_text="SUBMIT")],
]
sg.popup("""The SYMPTOMS LIST and TIME LIST entries must be
comma separated values that correspond with each other.
If the patient has severe cough for the past 2 days, the
first symptom entry must be "SEVERE COUGH" and the first
TIME LIST entry must be "2", without quotes for both.""")

window = sg.Window("Data Enterer", elements)

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    elif event =="SUBMIT":
        with open("data.csv", 'a') as csvfile:
                values["MORTALITY"]="ALIVE"
                w = csv.DictWriter(csvfile, values.keys())
                if csvfile.tell() == 0:
                    w.writeheader()
                w.writerow(values)
        for key in values.keys():
            if key is not "MORTALITY":
                window[key]('')
        sg.popup("DATA SUBMITTED.")

window.close()