'''This file defines the function that are required for convert CSV to python object,
as well as write it to a MySql Database'''

#necessary imports
import csv
import json
import mysql.connector as ms
from os import path

from constants import mySqlDatabase,mySqlPassword,mySqlHost,mySqlUsername,SQLTableName


def parseCSV(fp):
    rowsList=[]
    with open(fp,'r',encoding='utf-8') as data:
        reader = csv.reader(data,dialect='excel')
        for rows in reader: #as first row in heading
            rowsList.append(rows)
    return rowsList

def is_num(var):
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
    return [[item for item in row]for row in items]

def create_table():
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
    for row in rows[1:]: #1st row in columnName
        row[sympIndex]=json.dumps([row[sympIndex]])
        row[timesIndex]=json.dumps([row[timesIndex]])
        SQLStatement="INSERT INTO %s("%SQLTableName
        for i in range(len(columnNames)):
            if i!=len(columnNames)-1:
                SQLStatement+=columnNames[i]+','
            else:
                SQLStatement+=columnNames[i]+')'
        SQLStatement+=" VALUES("
        for i in range(len(row)):
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

if __name__== '__main__':
    #a=parseCSV(path.join("..","data.csv"))
    #print(write_database(tuple(a[0]),tuple(a)))
    print(sql_to_list())
    #write_database(columnNames,rows)
    #print(show_table_rows())
