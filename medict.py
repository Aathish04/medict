"""
    ./medict.py

    This is the main Python file which must be run to activate the application.
    It makes the necessary imports and in a modular manner builds the user interface
    for easy use.
"""

import os
import csv

try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    raise ModuleNotFoundError("The PySimpleGUI module needs to be installed.")

from managers import (
    CSVManager,
    ThemeManager,
    Predictor,
    BarGraphManager,
    SQLManager,
    get_settings_config,
    FontManager,
)

if __name__ == "__main__":
    sg.theme(get_settings_config()["theme"])
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    csvmanager = CSVManager()
    predictor = Predictor()
    sqlmanager = SQLManager()
    bargraphman = BarGraphManager()
    thememanager = ThemeManager()
    fontmanager = FontManager()
    info_layout = [[sg.Text(csvmanager.INSTRUCTIONS, font=(csvmanager.TEXTFONT, 12))]]
    layout = [  # Main Window layout
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Info", info_layout),
                        sg.Tab(
                            "CSV Spreadsheet",
                            csvmanager.spread_layout,
                            element_justification="center",
                        ),
                        sg.Tab(
                            "SQL Layout",
                            sqlmanager.spread_layout,
                            element_justification="center",
                        ),
                        sg.Tab(
                            "Predictor",
                            predictor.layout,
                            element_justification="center",
                        ),
                        sg.Tab(
                            "Graphs",
                            bargraphman.layout,
                            element_justification="center",
                        ),
                        sg.Tab(
                            "Settings",
                            [*thememanager.layout, *fontmanager.layout],
                            element_justification="center",
                        ),
                    ]
                ],
                enable_events=True,
                key="tab",
            )
        ]
    ]

    window = sg.Window("Medict", layout, resizable=True, finalize=True)
    window.maximize()
    window["tab"].expand(True, True, True)

    while True:  # Main event loop.
        event, values = window.read()

        if event in (None, "Exit"):
            break

        elif event == "tab":
            csvmanager.clear_data(values, window)
            csvmanager.reload_table()
            sqlmanager.reload_table()

        elif event == "bargraph_tab":
            window["-CANVAS-"].TKCanvas.delete("all")
            window["-GENDER_CANVAS-"].TKCanvas.delete("all")
            window["-MVF_CANVAS-"].TKCanvas.delete("all")

            if values["bargraph_tab"] == "age-vs-case":
                fig_photo = bargraphman.draw_figure(
                    window["-CANVAS-"].TKCanvas, bargraphman.fig
                )
            if values["bargraph_tab"] == "case-vs-gender":

                GENDER_CANVAS = bargraphman.draw_figure(
                    window["-GENDER_CANVAS-"].TKCanvas, bargraphman.fig1
                )  # assign to variable or else the graph is killed.
            if values["bargraph_tab"] == "male-vs-female":
                mvf_graph = bargraphman.draw_figure(
                    window["-MVF_CANVAS-"].TKCanvas, bargraphman.mvf_fig
                )
        elif event == "csvtable":  # Table is clicked etc.
            if len(csvmanager.table.SelectedRows) > 0:
                row = csvmanager.table.SelectedRows[-1]
                for i in range(len(values.keys())):
                    key = list(values.keys())[i]
                    if key in list(csvmanager.FIELDS):
                        window[key](csvmanager.table.get()[row][i - 1])

        elif event == "SUBMIT":
            csvmanager.submit_filled(values)

        elif event == "RELOAD":
            csvmanager.table.update(values=csvmanager.records_from_csv())

        elif event == "THEMEBTN":
            if len(values['THEMELIST']) > 0:
                sg.theme(values['THEMELIST'][0]) 
                thememanager.set_theme(values["THEMELIST"][0])
            if values["FONTSPIN"] != fontmanager.fontSize:
                fontmanager.set_fontsize(values["FONTSPIN"])
            sg.popup_ok("Restart program to see changes.",keep_on_top=True)
        elif event == "THEMELIST":
            sg.theme(values["THEMELIST"][0])
            sg.popup_ok("This is {}".format(values["THEMELIST"][0]),keep_on_top=True)
        elif event == "FONTSPIN":
            window["FONTSPIN"].update(values["FONTSPIN"])
            window["FontPreview"].update(font = "Helvetica "+str(values['FONTSPIN']))
        elif event == "RELOADSQL":
            sqlmanager.reload_table()

        elif event == "CLEAR FILLED":
            csvmanager.clear_data(values, window)
        elif event == "DELETE ROWS":
            csvmanager.delete_selected_rows()

        elif event == "DELETE ALL ROWS":
            csvmanager.delete_all_rows()
        elif event == "WRITEDB":
            if sqlmanager.sql_to_list() == []:
                sqlmanager.write_database(
                    tuple(csvmanager.FIELDS), tuple(csvmanager.records_from_csv())
                )

        elif event == "ESTIMATE":
            data = {
                field: values[field] for field in values if field in predictor.FIELDS
            }
            if not all(data.values()):
                sg.popup(csvmanager.UNFILLED_DATA_ERROR)
            else:
                data["AGE"] = int(data.pop("pAGE"))
                data["GENDER"] = data.pop("pGENDER")
                data["SYMPTOMS"] = (
                    ["UNKNOWN"]
                    if data["pSYMPTOMS"] == "UNKNOWN"
                    else data["pSYMPTOMS"].split(",")
                )
                data["TIMES"] = (
                    ["UNKNOWN"]
                    if data["pTIMES"] == "UNKNOWN"
                    else [int(time) for time in data["pTIMES"].split(",")]
                )
                data["TEMPERATURE"] = (
                    ["UNKNOWN"]
                    if data["pTEMPERATURE"] == "UNKNOWN"
                    else float(data["pTEMPERATURE"])
                )
                data["MEDICATION"] = (
                    ["UNKNOWN"]
                    if data["pMEDICATION"] == "UNKNOWN"
                    else data["pMEDICATION"].split(",")
                )

                del data["pSYMPTOMS"]
                del data["pTIMES"]
                del data["pTEMPERATURE"]
                del data["pMEDICATION"]

                data = csvmanager.expanded_dataset([data])[
                    0
                ]  # expanded_dataset returns a list. In this case, only one element is in the list.
                prediction = predictor.predict(
                    data, allowed_deviation=values["DEVIANCE"]
                )
                window["pMORTALITY"].update(str(prediction))
        else:
            print(event)

    window.close()
