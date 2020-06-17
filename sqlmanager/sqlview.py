'''This file contain the elements of PySimpleGui which can be imported when creating final GUI.
'''

import os
import PySimpleGUI as sg
import mainparser as parsesql

class SQLManager(object):
    CSVFILE="data.csv"
    def __init__(self,TEXTFONT="serif",FONTSIZE=15,NUM_ROWS=20):
        """Initialises the SQL Manager.

        Args:
            TEXTFONT (str, optional): The font to use for all text. Defaults to 12.
            FONTSIZE (int, optional): The fontsize to use for all text. Defaults to "serif".
            NUM_ROWS (int, optional): The number of rows to display in the Table. Defaults to 20
        """
        self.TEXTFONT=TEXTFONT
        self.FONTSIZE=FONTSIZE
        self.NUM_ROWS=NUM_ROWS
        self.FIELDS = parsesql.show_table_rows()
        self.spread_layout=[
            [
                sg.Table(
                    values=parsesql.sql_to_list(),headings=self.FIELDS,key="sqltable",
                    display_row_numbers=False,header_font=(self.TEXTFONT,self.FONTSIZE),alternating_row_color="black",
                    auto_size_columns=False, def_col_width=20,size=(None,self.NUM_ROWS),
                    select_mode="extended",enable_events=True,font=(self.TEXTFONT,self.FONTSIZE)
                    )
                ],
            [
                sg.Column(
                    [
                        [sg.Button(button_text="COMPARE WITH CSV",button_color=("white","blue"),size=(18,1))],
                        ],justification="center",
                    element_justification="center"),

                ]
            ]
        self.table=self.spread_layout[0][0]
        self.table.StartingRowNumber=1
        self.table.RowHeaderText="ID"
    def reload_table(self):
        """Reloads the table by reading the CSV file and updating as necessary.
        """
        self.table.update(values=parsesql.sql_to_list())
if __name__=="__main__": #For if you want to run this standalone to edit quickly.
    sg.theme('DarkTanBlue')
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    info_layout=[[sg.Text("Hi")]]
    sqlmanager=SQLManager()
    layout=[ # Main Window layout
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Info",info_layout),

                        sg.Tab(
                            "SpreadSheet",sqlmanager.spread_layout,
                            element_justification='center'
                            )
                        ]
                    ],
                enable_events=True,key="tab"
                )
            ]
        ]

    window = sg.Window("Data Enterer", layout).Finalize()
    window.Maximize()

    while True: #Main event loop.
        event, values = window.read()

        if event in (None, 'Exit'):
            break

        elif event=="tab":
            sqlmanager.reload_table()

        elif event=="sqltable": #Table is clicked etc.
            row=sqlmanager.table.SelectedRows[-1]
            for i in range(len(values.keys())):
                key = list(values.keys())[i]
                if key in list(sqlmanager.FIELDS):
                    window[key](sqlmanager.table.get()[row][i-1])
        else:
            print(event)

    window.close()