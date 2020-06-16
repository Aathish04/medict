# AATHISH SIVASUBRAHMANIAN

import os
import csv
import PySimpleGUI as sg

class CSVManager(object):
    CSVFILE="data.csv"

    INSTRUCTIONS="""The SYMPTOMS LIST and TIME LIST entries must be \
    comma separated values that correspond with each other.
    If the patient has severe cough for the past 2 days,\
    the first symptom entry must be "SEVERE COUGH" and the first
    TIME LIST entry must be "2", without quotes for both."""

    ROW_WARN="Are you ABSOLUTELY SURE you want to DELETE the selected row(s)?"

    UNFILLED_DATA_ERROR="Some (or all) fields were left empty. \
    Please use UNKNOWN as the entry if you don't know the data!"

    TEXTFONT="serif"

    FIELDS=["AGE","GENDER","SYMPTOMS","TIMES","TEMPERATURE","MEDICATION","MORTALITY"]

    def __init__(self):
        self.spread_layout=[
            [
                sg.Table(
                    values=self.records_from_csv(),headings=self.FIELDS,key="csvtable",
                    display_row_numbers=True,header_font=(self.TEXTFONT,12),alternating_row_color="black",
                    auto_size_columns=False, def_col_width=20,size=[3*l for l in [16,9]],
                    select_mode="extended",enable_events=True
                    )
                ],
            [
                sg.Frame(
                    "Form",[
                    [sg.Text("AGE:",font=(self.TEXTFONT,12)), sg.Input(key="AGE",font=(self.TEXTFONT,12))],
                    [sg.Text("GENDER:",font=(self.TEXTFONT,12)),sg.Input(key="GENDER",font=(self.TEXTFONT,12))],
                    [
                        sg.Text("SYMPTOMS LIST:",font=(self.TEXTFONT,12)),
                        sg.Input(key="SYMPTOMS",font=(self.TEXTFONT,12)),
                        sg.Text("TIME LIST:",font=(self.TEXTFONT,12)),
                        sg.Input(key="TIMES",font=(self.TEXTFONT,12))
                        ],
                    [sg.Text("TEMPERATURE IN C:",font=(self.TEXTFONT,12)),sg.Input(key="TEMPERATURE",font=(self.TEXTFONT,12))],
                    [
                        sg.Text("MEDICATION GIVEN:",font=(self.TEXTFONT,12)),sg.Input(key="MEDICATION",font=(self.TEXTFONT,12)),
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
        self.table=self.spread_layout[0][0]
        self.table.StartingRowNumber=1

    def clear_data(self, local_variables=None):
        """Clears all the unpushed data filled in the form.

        Args:
            local_variables (dict, optional): Pass locals() here iff you are
            importing CSVManager from another file. This is so it can access
            the local namespace of that file. Defaults to None.
        """
        if __name__!="__main__":
            values=local_variables["values"]
            window=local_variables["window"]
        else:
            values=globals()["values"]
            window=globals()["window"]
        for key in values.keys():
            if key in self.FIELDS:
                window[key]('')

    def records_from_csv(self):
        """Returns a list of (list of entries for each field)
        for each row of the CSV file.

        Returns:
            list of lists: The outer list holds each row, the inner list holds
                            each value in that row for each field.
        """
        with open(self.CSVFILE,'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            return [
                [
                    row[fieldname] for fieldname in csv_reader.fieldnames
                    ] for row in csv_reader
                ]

    def list_od_from_csv(self):
        """Returns a list of ordered dictionaries that map each field to its value
        for each row in the CSV file.

        Returns:
            list[OrderedDictionary]: List containing the ordered dictionaries that
                                    map the field to their values, for each row.
        """
        with open(self.CSVFILE, "r") as csvfile:
            data=csv.DictReader(csvfile)
            datalist=[d for d in data]
        return datalist

    def write_list_od_to_csv(self,list_of_ordered_dicts):
        """Writes a list of ordered dictionaries that maps each field to its value
        for a single row, to the CSV file.

        Args:
            list_of_ordered_dicts (list[OrderedDict]): The list containing the
                            ordered dictionaries that map each field to its value.

        """
        with open(self.CSVFILE,"w") as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=self.FIELDS,extrasaction="ignore")
            writer.writeheader()
            writer.writerows(list_of_ordered_dicts)

    def submit_filled(self, local_variables=None):
        """Submits the data filled in the form by writing it to the CSV file.
        If the NEW ROW checkbox has been unchecked, it edits the currently
        selected row instead of adding a new row.

        Args:
            local_variables (dict, optional): Pass locals() here iff you are
            importing CSVManager from another file. This is so it can access
            the local namespace of that file. Defaults to None.
        """
        if __name__ !="__main__":
            values=local_variables["values"]
        else:
            values=globals()["values"]

        data={
            field:values[field] for field in values if field in self.FIELDS[:-1]
            }
        if not all(data.values()):
            sg.popup(self.UNFILLED_DATA_ERROR)
        else:
            if values["NEW ROW"]==True:
                with open(self.CSVFILE, 'a') as csvfile:
                    data["MORTALITY"]="ALIVE"
                    w = csv.DictWriter(csvfile, data.keys())
                    if csvfile.tell() == 0:
                        w.writeheader()
                    w.writerow(data)
            else:
                if self.table.SelectedRows!=[]:
                    new_rows=[]
                    datalist=self.list_od_from_csv()
                    for i in range(len(datalist)):
                        if i in self.table.SelectedRows:
                            for field in self.FIELDS:
                                if field is not "MORTALITY":
                                    datalist[i][field]=values[field]
                                else:
                                    datalist[i][field]="ALIVE"
                    self.write_list_od_to_csv(datalist)
                else:
                    sg.popup("No row(s) selected!")
        self.clear_data(local_variables)
        self.reload_table()

    def reload_table(self):
        """Reloads the table by reading the CSV file and updating as necessary.
        """
        self.table.update(values=self.records_from_csv())

    def delete_selected_rows(self):
        """Deletes only the rows selected in the User Interface.
        """
        if self.table.SelectedRows != [] and sg.popup_yes_no(self.ROW_WARN)=="Yes":
            rows_left=[]
            datalist=self.list_od_from_csv()
            for i in range(len(datalist)):
                if i not in self.table.SelectedRows:
                    rows_left.append(datalist[i])
            self.write_list_od_to_csv(rows_left)
        elif table.SelectedRows == []:
            sg.popup("No Rows have been selected!")
        self.reload_table()

    def delete_all_rows(self):
        """Deletes all rows in the CSV.
        """
        confirm=sg.popup_yes_no("Are you sure you want to DELETE ALL ROWS?")
        if confirm=="Yes":
            with open(self.CSVFILE, 'r') as csvfile:
                firstline=csvfile.readline()
            with open(self.CSVFILE,"w") as csvfile:
                csvfile.write(firstline)
        self.reload_table()

if __name__=="__main__": #For if you want to run this standalone to edit quickly.
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
                            "SpreadSheet",csvmanager.spread_layout,
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
            csvmanager.clear_data()
            csvmanager.reload_table()

        elif event=="csvtable": #Table is clicked etc.
            row=csvmanager.table.SelectedRows[-1]
            for i in range(len(values.keys())):
                key = list(values.keys())[i]
                if key in list(csvmanager.FIELDS):
                    window[key](csvmanager.table.get()[row][i-1])

        elif event=="SUBMIT":
            csvmanager.submit_filled()

        elif event=="RELOAD":
            csvmanager.table.update(values=csvmanager.records_from_csv())

        elif event=="CLEAR FILLED":
            csvmanager.clear_data()

        elif event=="DELETE ROWS":
            csvmanager.delete_selected_rows()

        elif event == "DELETE ALL ROWS":
            csvmanager.delete_all_rows()

        else:
            print(event)

    window.close()
