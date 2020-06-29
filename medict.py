import os
import sys
import csv
try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    raise ModuleNotFoundError("The PySimpleGUI module needs to be installed.")

from managers import CSVManager,SQLManager,Predictor

if __name__=="__main__":
    sg.theme('DarkTanBlue')
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    csvmanager=CSVManager()
    predictor=Predictor()
    if sys.platform=="darwin": # This "if" is just for MacOS testing.
        sqlmanager = SQLManager(mySqlHost="192.168.0.107")  #It will be removed
    else:   # as soon as everything else is finished.
        sqlmanager = SQLManager() # so don't remove it before that.
    info_layout=[[sg.Text(csvmanager.INSTRUCTIONS,font=(csvmanager.TEXTFONT,12))]]
    layout=[ # Main Window layout
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Info",info_layout),

                        sg.Tab(
                            "CSV Spreadsheet",csvmanager.spread_layout,
                            element_justification='center'
                            ),

                        sg.Tab(
                            "SQL Layout",sqlmanager.spread_layout,
                            element_justification='center'
                        ),
                        sg.Tab(
                            "Predictor",predictor.layout,
                            element_justification='center'
                        )
                        ]
                    ],
                enable_events=True,key="tab"
                )
            ]
        ]

    window = sg.Window("Medict", layout,resizable=True,finalize=True)
    window.maximize()
    window["tab"].expand(True,True,True)

    while True: #Main event loop.
        event, values = window.read()

        if event in (None, 'Exit'):
            break

        elif event=="tab":
            csvmanager.clear_data(locals())
            csvmanager.reload_table()
            sqlmanager.reload_table()

        elif event=="csvtable": #Table is clicked etc.
            row=csvmanager.table.SelectedRows[-1]
            for i in range(len(values.keys())):
                key = list(values.keys())[i]
                if key in list(csvmanager.FIELDS):
                    window[key](csvmanager.table.get()[row][i-1])

        elif event=="SUBMIT":
            csvmanager.submit_filled(locals())

        elif event=="RELOAD":
            csvmanager.table.update(values=csvmanager.records_from_csv())

        elif event == "RELOADSQL":
            sqlmanager.reload_table()

        elif event=="CLEAR FILLED":
            csvmanager.clear_data(locals())

        elif event=="DELETE ROWS":
            csvmanager.delete_selected_rows()

        elif event == "DELETE ALL ROWS":
            csvmanager.delete_all_rows()

        elif event == "ESTIMATE":
            data={
            field:values[field] for field in values if field in predictor.FIELDS
            }
            if not all(data.values()):
                sg.popup(csvmanager.UNFILLED_DATA_ERROR)
            else:
                data=[data]
                for i in range(len(data)):
                    data[i]["AGE"]=int(data[i].pop("mAGE"))
                    data[i]["GENDER"]=data[i].pop("mGENDER")
                    data[i]["SYMPTOMS"]= ["UNKNOWN"] if data[i]["mSYMPTOMS"] == "UNKNOWN" else data[i]["mSYMPTOMS"].split(",")
                    data[i]["TIMES"]=["UNKNOWN"] if data[i]["mTIMES"] == "UNKNOWN" else [int(time) for time in data[i]["mTIMES"].split(",")]
                    data[i]["TEMPERATURE"]=["UNKNOWN"] if data[i]["mTEMPERATURE"] == "UNKNOWN" else float(data[i]["mTEMPERATURE"])
                    data[i]["MEDICATION"]=["UNKNOWN"] if data[i]["mMEDICATION"] == "UNKNOWN" else data[i]["mMEDICATION"].split(",")
                    data[i]["MORTALITY"]=0 #This is just a value in order to keep the size of the data array the same.

                del data[i]["mSYMPTOMS"]
                del data[i]["mTIMES"]
                del data[i]["mTEMPERATURE"]
                del data[i]["mMEDICATION"]

                data=csvmanager.expanded_dataset(data)
                prediction=predictor.predict(data)
                window['mMORTALITY'].update(str(prediction[0]*100))
        else:
            print(event)

    window.close()
