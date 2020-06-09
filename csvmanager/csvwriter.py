# AATHISH SIVASUBRAHMANIAN

import os
import csv
import PySimpleGUI as sg

def clear_data():
    for key in values.keys():
        if key not in ("MORTALITY",0):
            window[key]('')

os.chdir(os.path.abspath(os.path.dirname(__file__)))

sg.theme('DarkTanBlue')

form_layout=[
    [sg.Text("AGE:"), sg.Input(key="AGE")],
    [sg.Text("GENDER:"), sg.Input(key="GENDER")],
    [
        sg.Text("SYMPTOMS LIST:"),sg.Input(key="SYMPTOMS"),
        sg.Text("TIME LIST"), sg.Input(key="TIMES")
        ],
    [sg.Text("TEMPERATURE IN C:"), sg.Input(key="TEMPERATURE")],
    [sg.Text("MEDICATION GIVEN:"), sg.Input(key="MEDICATION")],
]

spread_layout=[
    [sg.Text("The SpreadSheet Viewer and editor will go here.")]
]

layout=[
    [
        sg.TabGroup(
            [[sg.Tab("Form",form_layout),sg.Tab("SpreadSheet",spread_layout)]],
            enable_events=True,metadata="AAA"
            )
        ],[sg.Button(button_text="SUBMIT")]
    ]

sg.popup("""The SYMPTOMS LIST and TIME LIST entries must be
comma separated values that correspond with each other.
If the patient has severe cough for the past 2 days, the
first symptom entry must be "SEVERE COUGH" and the first
TIME LIST entry must be "2", without quotes for both.""")

window = sg.Window("Data Enterer", layout)

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break
    elif event==0: #TODO: File an Issue to let PySimpleGUI allow named events for TabGroup
        clear_data()
        pass
    elif event =="SUBMIT":
        with open("data.csv", 'a') as csvfile:

                data=values.copy()
                data["MORTALITY"]="ALIVE"
                del data[0]

                w = csv.DictWriter(csvfile, data.keys())
                if csvfile.tell() == 0:
                    w.writeheader()

                w.writerow(data)
        clear_data()

window.close()