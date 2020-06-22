'''This file contain the elements of PySimpleGui which can be imported when creating final GUI.
'''

import PySimpleGUI as sg
import json
import mysql.connector as ms
from os import path,chdir

if __name__=="__main__":
    from csvmanager import CSVManager
else:
    from .csvmanager import CSVManager

class SQLManager(object):
    def __init__(self,TEXTFONT="serif",FONTSIZE=15,NUM_ROWS=20):
        """Initialises the SQL Manager.

        Args:
            TEXTFONT (str, optional): The font to use for all text. Defaults to 15.
            FONTSIZE (int, optional): The fontsize to use for all text. Defaults to "serif".
            NUM_ROWS (int, optional): The number of rows to display in the Table. Defaults to 20
        """
        #MySQL Configuration Starts
        self.mySqlHost="localhost"
        self.mySqlUsername='root'
        self.mySqlDatabase = 'hospital'
        self.mySqlPassword = 'password21'
        self.SQLTableName='patients'
        self.SQLTableCreationPath = path.join('..','database.sql')
        #MySQl Configuration ends
        self.TEXTFONT=TEXTFONT
        self.FONTSIZE=FONTSIZE
        self.NUM_ROWS=NUM_ROWS
        if self.checkTableExists(): #check table exists or not.
            self.FIELDS = self.show_table_rows()
        else:
            self.create_table()
            self.FIELDS = self.show_table_rows()
        self.spread_layout=[
            [
                sg.Table(
                    values=self.sql_to_list(),headings=self.FIELDS,key="sqltable",
                    display_row_numbers=False,header_font=(self.TEXTFONT,self.FONTSIZE),alternating_row_color="black",
                    auto_size_columns=False, def_col_width=20,size=(None,self.NUM_ROWS),
                    select_mode="extended",enable_events=True,font=(self.TEXTFONT,self.FONTSIZE)
                    )
                ],
            [
                sg.Column(
                    [
                        [sg.Button(button_text="COMPARE WITH CSV",button_color=("white","blue"),size=(18,1))],
                        [sg.Button(button_text="RELOAD",key="RELOADSQL",button_color=("black","WHITE"),size=(16,1))],
                        ],
                        justification="center",
                    element_justification="center"),
                    ]
                ]
        self.table=self.spread_layout[0][0]
        self.table.StartingRowNumber=1
        self.table.RowHeaderText="ID"
    def reload_table(self):
        """Reloads the table by reading the Database and updating as necessary.
        """
        self.table.update(values=self.sql_to_list())
    def is_num(self,var):
        '''Some checking of value of data written in SQL database and converting it'''
        if var == "null": #Check whether it is null
            return True
        try:
            var=int(var)
            return True
        except ValueError:
            return False
    def intialise_dataBase(self):
        '''Initialises all the variable required for qurying MySql'''
        #global con,cursor
        self.con=ms.connect(
            host=self.mySqlHost,
            user=self.mySqlUsername,
            passwd=self.mySqlPassword,
            database=self.mySqlDatabase
        )
        self.cursor=self.con.cursor()

    def checkTableExists(self,tablename='patients'):
        '''Check whether the table `tablenames` already exits'''
        self.intialise_dataBase()
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))
        if self.cursor.fetchone()[0] == 1:
            return True
        return False
    
    def sql_to_list(self):
        '''Converts things in sql database to lists which contain rows as tuples
        Eg.
        [
            (1, 51, 'MALE', '["FEVER, CHEST TIGHTNESS, DYSPNEA"]', '["8, 8, 8"]', Decimal('38.90'), 'ANTI-INFLAMMATORY', None)
            (2, 20, 'FEMALE', '["DYSPNEA, DRY COUGH, FEVER"]', '["5, 5, 5"]', Decimal('38.50'), 'SELF:PARACETAMOL, AMOXILLIN', None)
            (3, 90, 'FEMALE', '["DYSPNEA, DRY COUGH, DEVER"]', '["7+"]', Decimal('38.00'), 'MULTI-DRUG THERAPY, O2-THERAPY', None)
            (4, 70, 'MALE', '["FEVER, DRY COUGH, DYSPNEA, CHEST PAIN"]', '["4, 4, 4, 4"]', Decimal('39.00'), 'MULTI-DRUG THERAPY, O2 THERAPY, INTUBATION, CPAP THERAPY', None)
            (5, 57, 'MALE', '["DYSPNEA, DRY COUGH, FEVER"]', '["7, 7, 7"]', Decimal('38.50'), 'MULTI-DRUG THERAPY, O2-THERAPY', None)
        ]
        '''
        self.intialise_dataBase()
        self.cursor.execute("SELECT * from %s"%self.SQLTableName)
        items = self.cursor.fetchall()
        tempItems = []
        finalItems = []
        for item in items:
            for things in item:
                if type(things) == str:
                    if '[' in things:
                        things = json.loads(str(things))
                if type(things) == list:
                    tempItems.append(str(things)[2:-2])
                else:
                    tempItems.append(str(things))
            else:
                finalItems.append(tempItems)
                tempItems=[]
        return finalItems
    
    def create_table(self):
        '''This create a table defined in `database.sql`'''
        self.intialise_dataBase()
        with open(self.SQLTableCreationPath,'r') as f:
            SQLStatement=f.read()
        self.cursor.execute(SQLStatement)

    def show_table_rows(self):
        '''This function would return the column names in SQL Tables.'''
        self.intialise_dataBase()
        self.cursor.execute("DESC %s"%self.SQLTableName)
        desc = self.cursor.fetchall()
        return [i[0] for i in desc]

    def write_database(self,columnNames,rows):
        '''Write into MySql table name as specified.
        columnNames -> List
        rows ->List
        tablesName ->str
        '''
        self.intialise_dataBase()
        sympIndex=columnNames.index('SYMPTOMS')
        timesIndex=columnNames.index('TIMES')
        for row in rows:
            row[sympIndex]="null" if row[sympIndex]=="UNKNOWN" else json.dumps([row[sympIndex]])
            row[timesIndex]="null" if row[timesIndex]=="UNKNOWN" else json.dumps([row[timesIndex]])
            SQLStatement="INSERT INTO %s("%self.SQLTableName
            for i in range(len(columnNames)):
                if i!=len(columnNames)-1:
                    SQLStatement+=columnNames[i]+','
                else:
                    SQLStatement+=columnNames[i]+')'
            SQLStatement+=" VALUES("
            for i in range(len(row)):
                if row[i] == "UNKNOWN": #Make it to null in SQL instead of saving it as is as it cause errors.
                    row[i]="null"
                if i!=(len(row)-1) and self.is_num(row[i]):
                    SQLStatement+=row[i]+','
                elif i!=(len(row)-1) and (not self.is_num(row[i])):
                    SQLStatement+="'%s'"%row[i]+','
                elif i==(len(row)-1) and self.is_num(row[i]):
                    SQLStatement+=row[i]+');'
                elif i==(len(row)-1) and (not self.is_num(row[i])):
                    SQLStatement+="'%s'"%row[i]+');'
            print(SQLStatement)
            if self.checkTableExists()==True:
                self.cursor.execute(SQLStatement)
            else:
                self.create_table()
                self.cursor.execute(SQLStatement)
            self.con.commit()

    def update_row(self,patientid,fields_to_change,updated_data):
        '''This updates a specific row in a SQL table with specific patientid.
        Parameters
        ----------
        patientid -> int
        fields_to_change -> List or Tuple
        updated_data -> List or Tuple

        Raises
        ------
        ValueError -> When length of `fields_to_change` and `updated_data` doesn't match
        Norows affected

        Returns
        -------
        None
        '''
        self.intialise_dataBase()
        SQLStatement = "UPDATE "+self.SQLTableName+" SET "
        if len(fields_to_change)==len(updated_data):
            for field,data in zip(fields_to_change,updated_data):
                SQLStatement+=str(field)+"="+"'%s'"%data+', '
        else:
            raise ValueError("Looks like fields_to_change and updated_data doesn't have equal values.")
        SQLStatement=SQLStatement[:-2] #remove last comma and space
        SQLStatement+=' WHERE patientid=%s'%patientid+';'
        self.cursor.execute(SQLStatement)
        if self.cursor.rowcount == 0:
            print("There is no Rows affected Please Check Your Parameters")
        else:
            self.con.commit()


if __name__=="__main__": #For if you want to run this standalone to edit quickly.
    #Some check of whether function works is below
    '''This is to test some functions'''
    csvmanager=CSVManager(CSVFILE=path.abspath(__file__ + "/../../data.csv"))
    a=csvmanager.records_from_csv()
    sqlmanager=SQLManager(TEXTFONT="Roboto Regular")
    print(sqlmanager.write_database(tuple(csvmanager.FIELDS),tuple(a)))
    print(sqlmanager.sql_to_list())
    print(sqlmanager.show_table_rows())
    sqlmanager.update_row(20,['GENDER'],['FEMALE'])
    sg.theme('DarkTanBlue')
    chdir(path.abspath(path.dirname(__file__)))
    info_layout=[[sg.Text("Hi")]]
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
            print("Exiting")
            break

        elif event=="tab":
            sqlmanager.reload_table()
        elif event=="RELOADSQL":
            sqlmanager.reload_table()
            print("Reloaded")
        else:
            print(event)

    window.close()
