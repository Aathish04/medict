'''This file contain the elements of PySimpleGui which can be imported when creating final GUI.
'''

import PySimpleGUI as sg
import parsesql

sqlTableLayout = [
        sg.Table(
            values=parsesql.sql_to_list(),headings=FIELDS,key="table",
            display_row_numbers=True,header_font=("serif",12),alternating_row_color="black",
            auto_size_columns=False, def_col_width=20,size=[3*l for l in [16,9]],
            select_mode="extended",enable_events=True
            )
        ]