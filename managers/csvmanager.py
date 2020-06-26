# AATHISH SIVASUBRAHMANIAN

import os
import csv
import PySimpleGUI as sg

class CSVManager(object):

    INSTRUCTIONS="""The SYMPTOMS LIST and TIME LIST entries must be \
    comma separated values that correspond with each other.
    If the patient has severe cough for the past 2 days,\
    the first symptom entry must be "SEVERE COUGH" and the first
    TIME LIST entry must be "2", without quotes for both."""

    ROW_WARN="Are you ABSOLUTELY SURE you want to DELETE the selected row(s)?"

    UNFILLED_DATA_ERROR="Some (or all) fields were left empty. \
    Please use UNKNOWN as the entry if you don't know the data!"

    FIELDS=["AGE","GENDER","SYMPTOMS","TIMES","TEMPERATURE","MEDICATION","MORTALITY"]

    def __init__(self,TEXTFONT="serif",FONTSIZE=14,NUM_ROWS=20,CSVFILE="data.csv"):
        """Initialises the CSV Manager.
            Good fontsizes are [12,21]
        Args:
            TEXTFONT (str, optional): The font to use for all text. Defaults to 12.
            FONTSIZE (int, optional): The fontsize to use for all text. Defaults to "serif".
            NUM_ROWS (int, optional): The number of rows to display in the Table. Defaults to 20
            CSVFILE (str, optional): The path (relative or full) to the csv file to read from.
            Defaults to "data.csv" in the same directory as the importing script.
        """
        self.TEXTFONT=TEXTFONT
        self.FONTSIZE=FONTSIZE
        self.NUM_ROWS=NUM_ROWS
        self.CSVFILE=CSVFILE
        self.spread_layout=[
            [
                sg.Table(
                    values=self.records_from_csv(),headings=self.FIELDS,key="csvtable",
                    display_row_numbers=True,header_font=(self.TEXTFONT,self.FONTSIZE),
                    alternating_row_color="black", auto_size_columns=False,
                    def_col_width=20,size=(None,self.NUM_ROWS), select_mode="extended",
                    enable_events=True,font=(self.TEXTFONT,self.FONTSIZE),justification="center"
                    )
                ],
            [
                sg.Frame("Form",
                    [[
                        sg.Column(
                            [
                                [sg.Button(button_text="UPLOAD TO CLOUD",button_color=("white","blue"),size=(18,1))],
                                [sg.Button(button_text="USE CLOUD BACKUP",button_color=("blue","white"),size=(18,1))],
                                [sg.Button(button_text="VIEW SCANS",button_color=("white","purple"),size=(18,1))],
                                [sg.Button(button_text="ADD SCANS",button_color=("purple","white"),size=(18,1))]
                                ],justification="left",

                            element_justification="center"),

                        sg.Frame(
                            "Data",[
                            [sg.Text("AGE:",font=(self.TEXTFONT,self.FONTSIZE)), sg.Input(key="AGE",font=(self.TEXTFONT,self.FONTSIZE))],
                            [sg.Text("GENDER:",font=(self.TEXTFONT,self.FONTSIZE)),sg.Input(key="GENDER",font=(self.TEXTFONT,self.FONTSIZE))],
                            [
                                sg.Text("SYMPTOMS LIST:",font=(self.TEXTFONT,self.FONTSIZE)),
                                sg.Input(key="SYMPTOMS",font=(self.TEXTFONT,self.FONTSIZE),size=(30,1)),
                                sg.Text("TIME LIST:",font=(self.TEXTFONT,self.FONTSIZE)),
                                sg.Input(key="TIMES",font=(self.TEXTFONT,self.FONTSIZE),size=(30,1))
                                ],
                            [sg.Text("TEMPERATURE IN C:",font=(self.TEXTFONT,self.FONTSIZE)),sg.Input(key="TEMPERATURE",font=(self.TEXTFONT,self.FONTSIZE))],
                            [
                                sg.Text("MEDICATION GIVEN:",font=(self.TEXTFONT,self.FONTSIZE)),sg.Input(key="MEDICATION",font=(self.TEXTFONT,self.FONTSIZE)),
                                sg.Checkbox('ALIVE',key="ALIVE",default=True,size=(16,2),background_color=("#1b1b1b")),
                                ],
                            ]),

                        sg.Column(
                            [
                                [sg.Checkbox('NEW ROW',key="NEW ROW",default=True,size=(16,2),background_color=("#0366fc"))],
                                [sg.Button(button_text="SUBMIT",button_color=("black","green"),size=(16,1))],
                                [sg.Button(button_text="RELOAD",button_color=("black","WHITE"),size=(16,1))],
                                [sg.Button(button_text="CLEAR FILLED",button_color=("RED","WHITE"),size=(16,1))],
                                [sg.Button(button_text="DELETE ROWS",button_color=("BLACK","RED"),size=(16,1))],
                                [sg.Button(button_text="DELETE ALL ROWS",button_color=("red","black"),size=(16,1))],
                                ],justification="right",
                            element_justification="center")
                        ]]
                    )
                ]
            ]

        self.table=self.spread_layout[0][0]
        self.table.StartingRowNumber=1
        self.table.RowHeaderText="ID"

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

    def records_from_csv(self,datafile=None):
        """Returns a list of (list of entries for each field)
        for each row of the CSV file.

        Args:
            datafile (str,optional): The path to the csv file. Defaults to None but
            is self.CSVFILE if None.
        Returns:
            list of lists: The outer list holds each row, the inner list holds
                            each value in that row for each field.
        """
        if datafile is None:
            datafile=self.CSVFILE
        with open(datafile,'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            return [
                [
                    row[fieldname] for fieldname in csv_reader.fieldnames
                    ] for row in csv_reader
                ]

    def list_od_from_csv(self,datafile=None):
        """Returns a list of ordered dictionaries that map each field to its value
        for each row in the CSV file.

        Args:
            datafile (str,optional): The path to the csv file. Defaults to None but
            is self.CSVFILE if None.
        Returns:
            list[OrderedDictionary]: List containing the ordered dictionaries that
                                    map the field to their values, for each row.
        """
        if datafile is None:
            datafile=self.CSVFILE
        with open(datafile, "r") as csvfile:
            data=csv.DictReader(csvfile)
            datalist=[d for d in data]
        return datalist

    def typed_list_od_from_csv(self):
        """Converts the String data of the CSV to list, int, float, whatevs.

        Returns:
            list: List of ordered dictionaries.
        """
        data=self.list_od_from_csv()
        for i in range(len(data)):
            data[i]["AGE"]=int(data[i]["AGE"])
            data[i]["SYMPTOMS"]= ["UNKNOWN"] if data[i]["SYMPTOMS"] == "UNKNOWN" else data[i]["SYMPTOMS"].split(",")
            data[i]["TIMES"]=["UNKNOWN"] if data[i]["TIMES"] == "UNKNOWN" else [int(time) for time in data[i]["TIMES"].split(",")]
            data[i]["TEMPERATURE"]=["UNKNOWN"] if data[i]["TEMPERATURE"] == "UNKNOWN" else float(data[i]["TEMPERATURE"])
            data[i]["MEDICATION"]=["UNKNOWN"] if data[i]["MEDICATION"] == "UNKNOWN" else data[i]["MEDICATION"].split(",")
        return data

    def unique_symptoms(self):
        """Returns all the unique symptoms experienced by all the patients.

        Returns:
            list: List of strings of the names of the symptoms
        """
        unique_symptoms=[]
        for entry in self.typed_list_od_from_csv():
            symptoms=entry["SYMPTOMS"]
            for symptom in symptoms:
                if symptom not in unique_symptoms and symptom!="UNKNOWN":
                    unique_symptoms.append(symptom)
        return unique_symptoms

    def unique_medications(self):
        """Returns all the unique medicines used by all the patients.

        Returns:
            list: List of strings of the names of the medicines
        """
        unique_medications=[]
        for entry in self.typed_list_od_from_csv():
            medications=entry["MEDICATION"]
            for medication in medications:
                if medication not in unique_medications and medication!="UNKNOWN":
                    unique_medications.append(medication)
        return unique_medications

    def expanded_dataset(self,lod=None):
        """Returns a list of ordered dictionaries of the details of the patient
        creating entries for all medications, symptoms etc. The value for each symptom
        is the number of days the patient had the symptom, and the for medication, it is
        1 if they used it, 0 if not.

        Returns:
            list: list of ordered dictionaries.
        """
        if lod==None:
            data=self.typed_list_od_from_csv()
        else:
            data=lod
        unique_symptoms=self.unique_symptoms()
        unique_medications=self.unique_medications()
        for record in data:
            if record["TEMPERATURE"]==["UNKNOWN"]:
                record["TEMPERATURE"]=37
            for i in range(len(unique_symptoms)):
                if unique_symptoms[i] in record["SYMPTOMS"]:
                    if len(record["TIMES"])==1:
                        if record["TIMES"][0]!="UNKNOWN":
                            record[unique_symptoms[i]]=record["TIMES"][0]
                        else:
                            record[unique_symptoms[i]]=0
                    else:
                        record[unique_symptoms[i]] = record["TIMES"][record["SYMPTOMS"].index(unique_symptoms[i])]
                else:
                    record[unique_symptoms[i]]=0
            for i in range(len(unique_medications)):
                if unique_medications[i] in record["MEDICATION"]:
                    record[unique_medications[i]]=1
                else:
                    record[unique_medications[i]]=0
            if lod==None:
                record["MORTALITY"] = 1 if record["MORTALITY"]=="ALIVE" else 0
            del record["SYMPTOMS"]
            del record["TIMES"]
            del record["MEDICATION"]
        return data

    def write_list_od_to_csv(self,list_of_ordered_dicts,datafile=None):
        """Writes a list of ordered dictionaries that maps each field to its value
        for a single row, to the CSV file.

        Args:
            list_of_ordered_dicts (list[OrderedDict]): The list containing the
                            ordered dictionaries that map each field to its value.

        """
        if datafile is None:
            datafile=self.CSVFILE
        with open(datafile,"w") as csvfile:
            fields=list(list_of_ordered_dicts[0].keys())
            writer=csv.DictWriter(csvfile,fieldnames=fields,extrasaction="ignore")
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
                    data["MORTALITY"]="ALIVE" if values["ALIVE"]==True else "DEAD"
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
                                    datalist[i][field]="ALIVE" if values["ALIVE"]==True else "DEAD"
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
        elif self.table.SelectedRows == []:
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

    csvmanager=CSVManager(CSVFILE="../data.csv")

    info_layout=[[sg.Text(csvmanager.INSTRUCTIONS,font=(csvmanager.TEXTFONT,csvmanager.FONTSIZE))]]
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
    window = sg.Window("Data Enterer", layout,resizable=True).finalize()
    window["tab"].expand(True,True,True)
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
