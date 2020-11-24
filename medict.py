import os
import csv
try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    raise ModuleNotFoundError("The PySimpleGUI module needs to be installed.")

from managers import CSVManager,Predictor,SQLManager

if __name__=="__main__":
    sg.theme('DarkTanBlue')
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    csvmanager=CSVManager()
    predictor=Predictor()
    sqlmanager = SQLManager()
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
            csvmanager.clear_data(values,window)
            csvmanager.reload_table()
            sqlmanager.reload_table()

        elif event=="csvtable": #Table is clicked etc.
            row=csvmanager.table.SelectedRows[-1]
            for i in range(len(values.keys())):
                key = list(values.keys())[i]
                if key in list(csvmanager.FIELDS):
                    window[key](csvmanager.table.get()[row][i-1])

        elif event=="SUBMIT":
            csvmanager.submit_filled(values)

        elif event=="RELOAD":
            csvmanager.table.update(values=csvmanager.records_from_csv())

        elif event == "RELOADSQL":
            sqlmanager.reload_table()

        elif event=="CLEAR FILLED":
            csvmanager.clear_data(values,window)

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
                data["AGE"]=int(data.pop("pAGE"))
                data["GENDER"]=data.pop("pGENDER")
                data["SYMPTOMS"] = ["UNKNOWN"] if data["pSYMPTOMS"] == "UNKNOWN" else data["pSYMPTOMS"].split(",")
                data["TIMES"]=["UNKNOWN"] if data["pTIMES"] == "UNKNOWN" else [int(time) for time in data["pTIMES"].split(",")]
                data["TEMPERATURE"]=["UNKNOWN"] if data["pTEMPERATURE"] == "UNKNOWN" else float(data["pTEMPERATURE"])
                data["MEDICATION"]=["UNKNOWN"] if data["pMEDICATION"] == "UNKNOWN" else data["pMEDICATION"].split(",")

                del data["pSYMPTOMS"]
                del data["pTIMES"]
                del data["pTEMPERATURE"]
                del data["pMEDICATION"]

                data=csvmanager.expanded_dataset([data])[0] #expanded_dataset returns a list. In this case, only one element is in the list.
                prediction=predictor.predict(data,allowed_deviation=values["DEVIANCE"])
                window['pMORTALITY'].update(str(prediction))
        else:
            print(event)

    window.close()
