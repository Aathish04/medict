'''This file defines the function that are required for convert CSV to python object,
as well as write it to a MySql Database'''

#necessary imports
import csv
import json
import mysql.connector as ms
from os import path

from constants import mySqlDatabase,mySqlPassword,CSVfileLocation,mySqlHost,mySqlUsername


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
    a=parseCSV(path.join(".","data.csv"))
    print(writeDatabase(tuple(a[0]),tuple(a),'patients'))