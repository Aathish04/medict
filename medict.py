import os
import csv
try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    raise ModuleNotFoundError("The PySimpleGUI module needs to be installed.")

from csvmanager import CSVManager

if __name__=="__main__":
    sg.theme('DarkTanBlue')
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    csvmanager=CSVManager()

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
                            )
                        ]
                    ],
                enable_events=True,key="tab"
                )
            ]
        ]

    window = sg.Window("Medict", layout).Finalize()
    window.Maximize()

    while True: #Main event loop.
        event, values = window.read()

        if event in (None, 'Exit'):
            break

        elif event=="tab":
            csvmanager.clear_data(locals())
            csvmanager.reload_table()

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

        elif event=="CLEAR FILLED":
            csvmanager.clear_data(locals())

        elif event=="DELETE ROWS":
            csvmanager.delete_selected_rows()

        elif event == "DELETE ALL ROWS":
            csvmanager.delete_all_rows()

        else:
            print(event)

    window.close()
