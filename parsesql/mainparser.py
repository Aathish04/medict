'''This file defines the function that are required for convert CSV to python object,
as well as write it to a MySql Database'''

#necessary imports
import csv
import json
import mysql.connector as ms
from os import path

from .constants import mySqlDatabase,mySqlPassword,mySqlHost,mySqlUsername,SQLTableName


def parseCSV(fp):
    rowsList=[]
    with open(fp,'r',encoding='utf-8') as data:
        reader = csv.reader(data,dialect='excel')
        for rows in reader: #as first row in heading
            rowsList.append(rows)
    return rowsList

def isNum(var):
    try:
        var=int(var)
        return True
    except ValueError:
        return False

def intialiseDataBase():
    '''Initialises all the variable required for qurying MySql'''
    global con,cursor
    con=ms.connect(
        host=mySqlHost,
        user=mySqlUsername,
        passwd=mySqlPassword,
        database=mySqlDatabase
    )
    cursor=con.cursor()

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
    intialiseDataBase()
    cursor.execute("SELECT * from %s"%SQLTableName)
    return cursor.fetchall()
def writeDatabase(columnNames,rows,tableName):
    '''Write into MySql table name as specified.
    columnNames -> List
    rows ->List
    tablesName ->str
    '''
    intialiseDataBase()
    sympIndex=columnNames.index('SYMPTOMS')
    timesIndex=columnNames.index('TIMES')
    for row in rows[1:]: #1st row in columnName
        row[sympIndex]=json.dumps([row[sympIndex]])
        row[timesIndex]=json.dumps([row[timesIndex]])
        SQLStatement="INSERT INTO %s("%tableName
        for i in range(len(columnNames)):
            if i!=len(columnNames)-1:
                SQLStatement+=columnNames[i]+','
            else:
                SQLStatement+=columnNames[i]+')'
        SQLStatement+=" VALUES("
        for i in range(len(row)):
            if i!=(len(row)-1) and isNum(row[i]):
                SQLStatement+=row[i]+','
            elif i!=(len(row)-1) and (not isNum(row[i])):
                SQLStatement+="'%s'"%row[i]+','
            elif i==(len(row)-1) and isNum(row[i]):
                SQLStatement+=row[i]+');'
            elif i==(len(row)-1) and (not isNum(row[i])):
                SQLStatement+="'%s'"%row[i]+');'
        print(SQLStatement)
        cursor.execute(SQLStatement)
        con.commit()
if __name__== '__main__':
    #a=parseCSV(path.join(".","data.csv"))
    #print(writeDatabase(tuple(a[0]),tuple(a),SQLTableName))
    for i in sql_to_list(): print(i)
