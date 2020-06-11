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

ROW_WARN="Are you ABSOLUTELY SURE you want to DELETE the selected row(s)?"

UNFILLED_DATA_ERROR="Some (or all) fields were left empty. \
Please use UNKNOWN as the entry if you don't know the data!"

FIELDS=["AGE","GENDER","SYMPTOMS","TIMES","TEMPERATURE","MEDICATION","MORTALITY"]

def clear_data():
    for key in values.keys():
        if key in FIELDS:
            window[key]('')

def records_from_csv():
    with open('data.csv', mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        return [
            [
                row[fieldname] for fieldname in csv_reader.fieldnames
                ] for row in csv_reader
            ]

sg.theme('DarkTanBlue')

info_layout=[[sg.Text(INSTRUCTIONS,font=("serif",12))]]

spread_layout=[
    [
        sg.Table(
            values=records_from_csv(),headings=FIELDS,key="table",
            display_row_numbers=True,header_font=("serif",12),alternating_row_color="black",
            auto_size_columns=False, def_col_width=20,size=[3*l for l in [16,9]],
            select_mode="extended",enable_events=True
            )
        ],
    [
        sg.Frame(
            "Form",[
            [sg.Text("AGE:",font=("serif",12)), sg.Input(key="AGE",font=("serif",12))],
            [sg.Text("GENDER:",font=("serif",12)),sg.Input(key="GENDER",font=("serif",12))],
            [
                sg.Text("SYMPTOMS LIST:",font=("serif",12)),
                sg.Input(key="SYMPTOMS",font=("serif",12)),
                sg.Text("TIME LIST:",font=("serif",12)),
                sg.Input(key="TIMES",font=("serif",12))
                ],
            [sg.Text("TEMPERATURE IN C:",font=("serif",12)),sg.Input(key="TEMPERATURE",font=("serif",12))],
            [
                sg.Text("MEDICATION GIVEN:",font=("serif",12)),sg.Input(key="MEDICATION",font=("serif",12)),
                ]
            ]),
        sg.Column(
            [
                [sg.Checkbox('NEW ROW',key="NEW ROW",default=True,size=(16,2),background_color=("#0366fc"))],
                [sg.Button(button_text="SUBMIT",button_color=("black","green"),size=(16,1))],
                [sg.Button(button_text="RELOAD",button_color=("black","WHITE"),size=(16,1))],
                [sg.Button(button_text="CLEAR FILLED",button_color=("RED","WHITE"),size=(16,1))],
                [sg.Button(button_text="DELETE ROWS",button_color=("BLACK","RED"),size=(16,1))],
                [sg.Button(button_text="DELETE ALL ROWS",button_color=("red","black"),size=(16,1))],
                ],
            element_justification="center")
        ]
    ]

layout=[ # Main Window layout
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Info",info_layout),

                    sg.Tab(
                        "SpreadSheet",spread_layout,
                        element_justification='center'
                        )
                    ]
                ],
            enable_events=True,key="tab"
            )
        ]
    ]

table=spread_layout[0][0] # Just so the table can easily be referred to.

window = sg.Window("Data Enterer", layout).Finalize()
window.Maximize()

while True: #Main application loop.
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    elif event=="tab":
        clear_data()
        table.update(values=records_from_csv())

    elif event=="table": #Table is clicked etc.
        row=table.SelectedRows[-1]
        for i in range(len(values.keys())):
            key = list(values.keys())[i]
            if key in list(FIELDS):
                window[key](table.get()[row][i-1])

    elif event=="SUBMIT":
        if values["NEW ROW"]==True:
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
        else:
            if table.SelectedRows!=[]:
                new_rows=[]
                with open("data.csv", "r") as csvfile:
                    data=csv.DictReader(csvfile)
                    datalist=[d for d in data]

                for i in range(len(datalist)):
                    if i in table.SelectedRows:
                        for field in FIELDS:
                            if field is not "MORTALITY":
                                datalist[i][field]=values[field]
                            else:
                                datalist[i][field]="ALIVE"
                with open("data.csv","w") as csvfile:
                    writer=csv.DictWriter(csvfile,FIELDS)
                    writer.writeheader()
                    writer.writerows(datalist)
            else:
                sg.popup("No row(s) selected!")
        clear_data()
        table.update(values=records_from_csv())

    elif event=="RELOAD":
        table.update(values=records_from_csv())

    elif event=="CLEAR FILLED":
        clear_data()

    elif event=="DELETE ROWS":
        if table.SelectedRows != [] and sg.popup_yes_no(ROW_WARN)=="Yes":
            rows_left=[]
            with open("data.csv", "r") as csvfile:
                data=csv.DictReader(csvfile)
                datalist=[d for d in data]
                for i in range(len(datalist)):
                    if i not in table.SelectedRows:
                        rows_left.append(datalist[i])
            with open("data.csv","w") as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows_left)
        elif table.SelectedRows == []:
            sg.popup("No Rows have been selected!")
        table.update(values=records_from_csv())

    elif event == "DELETE ALL ROWS":
        confirm=sg.popup_yes_no("Are you sure you want to DELETE ALL ROWS?")
        if confirm=="Yes":
            firstline=open("data.csv", 'r').readline()
            open("data.csv","w").write(firstline)
        table.update(values=records_from_csv())

    else:
        print(event)

window.close()
