# AATHISH SIVASUBRAHMANIAN

import os
import csv
import PySimpleGUI as sg

os.chdir(os.path.abspath(os.path.dirname(__file__)))

INSTRUCTIONS="""The SYMPTOMS LIST and TIME LIST entries must be \
comma separated values that correspond with each other.
If the patient has severe cough for the past 2 days,\
the first symptom entry must be "SEVERE COUGH" and the first
TIME LIST entry must be "2", without quotes for both."""

UNFILLED_DATA_ERROR="Some (or all) fields were left empty. \
Please use UNKNOWN as the entry if you don't know the data!"

FIELDS=["AGE","GENDER","SYMPTOMS","TIMES","TEMPERATURE","MEDICATION"]

def clear_data():
    for key in values.keys():
        if key in FIELDS:
            window[key]('')

sg.theme('DarkTanBlue')

form_layout=[
    [sg.Text(
        "AGE:",font=("serif",12)), sg.Input(key="AGE",font=("serif",12)
        )],

    [sg.Text(
        "GENDER:",font=("serif",12)), sg.Input(key="GENDER",font=("serif",12)
        )],

    [
        sg.Text(
            "SYMPTOMS LIST:",font=("serif",12)),
            sg.Input(key="SYMPTOMS",font=("serif",12)
            ),
        sg.Text(
            "TIME LIST",font=("serif",12)),
            sg.Input(key="TIMES",font=("serif",12)
            )
        ],

    [
        sg.Text("TEMPERATURE IN C:",font=("serif",12)),
        sg.Input(key="TEMPERATURE",font=("serif",12))
        ],

    [
        sg.Text("MEDICATION GIVEN:",font=("serif",12)),
        sg.Input(key="MEDICATION",font=("serif",12))
        ],

    [sg.Text("_"*180)],
    [sg.Text(INSTRUCTIONS,font=("serif",12))]
    ]

# NOTE: Might need to subclass the Dictreader to add some custom methods.
csv_reader = csv.DictReader(open('data.csv', mode='r+'))

# NOTE: This is one of those methods.
def records_from_csv():
    csv_reader = csv.DictReader(open('data.csv', mode='r+'))
    return [
        [
            row[fieldname] for fieldname in csv_reader.fieldnames
            ] for row in csv_reader
        ]

spread_layout=[
    [
        sg.Table(
            values=records_from_csv(),headings=FIELDS,key="table",
            display_row_numbers=True,header_font=("serif",12),alternating_row_color="black",
            auto_size_columns=False, def_col_width=20,size=[5*l for l in [16,9]],
            select_mode="extended",enable_events=True
            )
        ],
        [
            sg.Input(key="Change Entry",font=("serif",12)),sg.Button("Change Entry",key="change_entry")
        ]
]

layout=[ # Main Window layout
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Form",form_layout),

                    sg.Tab(
                        "SpreadSheet",spread_layout,
                        element_justification='center'
                        )
                    ]
                ],
            enable_events=True,key="tab"
            )
        ],
    [
        sg.Button(button_text="SUBMIT",button_color=("black","green")),
        sg.Button(button_text="CLEAR ALL",button_color=("black","RED"))
        ]
    ]

table=spread_layout[0][0] # Just so the table can easily be referred to.

window = sg.Window("Data Enterer", layout)

while True: #Main application loop.
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    elif event=="tab":
        clear_data()
        table.update(values=records_from_csv())

    elif event=="SUBMIT":
        if values["tab"]=="SpreadSheet":
            sg.popup("The SpreadSheet is read-only for now. Editing is coming!")
        else:
            with open("data.csv", 'a') as csvfile:
                    data={
                        e:values[e] for e in values if e in [
                            "AGE","GENDER","SYMPTOMS",
                            "TIMES","TEMPERATURE","MEDICATION"
                            ]}
                    data["MORTALITY"]="ALIVE"
                    if not all(data.values()):
                        sg.popup(UNFILLED_DATA_ERROR)
                    else:
                        w = csv.DictWriter(csvfile, data.keys())
                        if csvfile.tell() == 0:
                            w.writeheader()

                        w.writerow(data)
                        sg.popup("Data Submitted!")
            clear_data()

    elif event=="CLEAR ALL":
        if values["tab"]=="SpreadSheet":
            sg.popup("The SpreadSheet is read-only for now. Editing is coming!")
        else:
            clear_data()

    elif event=="table": #Table is clicked etc.
        table.update(values=records_from_csv())
        print(table.SelectedRows)

    else:
        print(event)

window.close()
