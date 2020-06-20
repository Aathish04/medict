'''This file defines the function that are required for convert CSV to python object,
as well as write it to a MySql Database'''

#necessary imports
import json
import mysql.connector as ms
from os import path

if __name__=="__main__":
    from csvmanager import CSVManager
else:
    from .csvmanager import CSVManager

mySqlHost='localhost'
mySqlUsername='root'
mySqlDatabase = 'hospital'
mySqlPassword = 'password21'
SQLTableName='patients'


def is_num(var):
    '''Some checking of value of data written in SQL database and converting it'''
    if var == "null": #Check whether it is null
        return True
    try:
        var=int(var)
        return True
    except ValueError:
        return False

def intialise_dataBase():
    '''Initialises all the variable required for qurying MySql'''
    global con,cursor
    con=ms.connect(
        host=mySqlHost,
        user=mySqlUsername,
        passwd=mySqlPassword,
        database=mySqlDatabase
    )
    cursor=con.cursor()

def checkTableExists(tablename='patients'):
    '''Check whether the table `tablenames` already exits'''
    intialise_dataBase()
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        return True
    return False

def sql_to_list():
    '''Converts things in sql database to lists which contain rows as tuples
    Eg.
    [
        (1, 51, 'MALE', '["FEVER, CHEST TIGHTNESS, DYSPNEA"]', '["8, 8, 8"]', Decimal('38.90'), 'ANTI-INFLAMMATORY', None)
        (2, 20, 'FEMALE', '["DYSPNEA, DRY COUGH, FEVER"]', '["5, 5, 5"]', Decimal('38.50'), 'SELF:PARACETAMOL, AMOXILLIN', None)
        (3, 90, 'FEMALE', '["DYSPNEA, DRY COUGH, DEVER"]', '["7+"]', Decimal('38.00'), 'MULTI-DRUG THERAPY, O2-THERAPY', None)
        (4, 70, 'MALE', '["FEVER, DRY COUGH, DYSPNEA, CHEST PAIN"]', '["4, 4, 4, 4"]', Decimal('39.00'), 'MULTI-DRUG THERAPY, O2 THERAPY, INTUBATION, CPAP THERAPY', None)
        (5, 57, 'MALE', '["DYSPNEA, DRY COUGH, FEVER"]', '["7, 7, 7"]', Decimal('38.50'), 'MULTI-DRUG THERAPY, O2-THERAPY', None)
        (6, 51, 'MALE', '["FEVER, CHEST TIGHTNESS, DYSPNEA"]', '["8, 8, 8"]', Decimal('38.90'), 'ANTI-INFLAMMATORY', None)
        (7, 20, 'FEMALE', '["DYSPNEA, DRY COUGH, FEVER"]', '["5, 5, 5"]', Decimal('38.50'), 'SELF:PARACETAMOL, AMOXILLIN', None)
        (8, 90, 'FEMALE', '["DYSPNEA, DRY COUGH, DEVER"]', '["7+"]', Decimal('38.00'), 'MULTI-DRUG THERAPY, O2-THERAPY', None)
        (9, 70, 'MALE', '["FEVER, DRY COUGH, DYSPNEA, CHEST PAIN"]', '["4, 4, 4, 4"]', Decimal('39.00'), 'MULTI-DRUG THERAPY, O2 THERAPY, INTUBATION, CPAP THERAPY', None)
        (10, 57, 'MALE', '["DYSPNEA, DRY COUGH, FEVER"]', '["7, 7, 7"]', Decimal('38.50'), 'MULTI-DRUG THERAPY, O2-THERAPY', None)
    ]
    '''
    intialise_dataBase()
    cursor.execute("SELECT * from %s"%SQLTableName)
    items = cursor.fetchall()
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

def create_table():
    '''This create a table defined in `database.sql`'''
    intialise_dataBase()
    with open(path.join('..','database.sql'),'r') as f:
        SQLStatement=f.read()
    cursor.execute(SQLStatement)

def show_table_rows():
    '''This function would return the column names in SQL Tables.'''
    intialise_dataBase()
    cursor.execute("DESC %s"%SQLTableName)
    desc = cursor.fetchall()
    return [i[0] for i in desc]

def write_database(columnNames,rows):
    '''Write into MySql table name as specified.
    columnNames -> List
    rows ->List
    tablesName ->str
    '''
    intialise_dataBase()
    sympIndex=columnNames.index('SYMPTOMS')
    timesIndex=columnNames.index('TIMES')
    for row in rows:
        row[sympIndex]="null" if row[sympIndex]=="UNKNOWN" else json.dumps([row[sympIndex]])
        row[timesIndex]="null" if row[timesIndex]=="UNKNOWN" else json.dumps([row[timesIndex]])
        SQLStatement="INSERT INTO %s("%SQLTableName
        for i in range(len(columnNames)):
            if i!=len(columnNames)-1:
                SQLStatement+=columnNames[i]+','
            else:
                SQLStatement+=columnNames[i]+')'
        SQLStatement+=" VALUES("
        for i in range(len(row)):
            if row[i] == "UNKNOWN": #Make it to null in SQL instead of saving it as is as it cause errors.
                row[i]="null"
            if i!=(len(row)-1) and is_num(row[i]):
                SQLStatement+=row[i]+','
            elif i!=(len(row)-1) and (not is_num(row[i])):
                SQLStatement+="'%s'"%row[i]+','
            elif i==(len(row)-1) and is_num(row[i]):
                SQLStatement+=row[i]+');'
            elif i==(len(row)-1) and (not is_num(row[i])):
                SQLStatement+="'%s'"%row[i]+');'
        print(SQLStatement)
        if checkTableExists()==True:
            cursor.execute(SQLStatement)
        else:
            create_table()
            cursor.execute(SQLStatement)
        con.commit()

def update_row(patientid,fields_to_change,updated_data):
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
    intialise_dataBase()
    SQLStatement = "UPDATE "+SQLTableName+" SET "
    if len(fields_to_change)==len(updated_data):
        for field,data in zip(fields_to_change,updated_data):
            SQLStatement+=str(field)+"="+"'%s'"%data+', '
    else:
        raise ValueError("Looks like fields_to_change and updated_data doesn't have equal values.")
    SQLStatement=SQLStatement[:-2] #remove last comma and space
    SQLStatement+=' WHERE patientid=%s'%patientid+';'
    cursor.execute(SQLStatement)
    if cursor.rowcount == 0:
        print("There is no Rows affected Please Check Your Parameters")
    else:
        con.commit()

if __name__== '__main__':
    '''This is to test some functions'''
    csvmanager=CSVManager()
    a=csvmanager.records_from_csv()
    print(write_database(tuple(csvmanager.FIELDS),tuple(a)))
    print(sql_to_list())
    print(show_table_rows())
    update_row(20,['GENDER'],['FEMALE'])
