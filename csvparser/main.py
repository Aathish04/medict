'''This file defines the function that are required for convert CSV to python object,
as well as write it to a MySql Database'''

#necessary imports
import csv
import constants
import mysql.connector as ms
from os import path

def parseCSV(fp):
    rowsList=[]
    with open(fp,'r',encoding='utf-8') as data:
        reader = csv.DictReader(data)
        for rows in reader: #as first row in heading
            rowsList.append(rows)
    return rowsList

print(parseCSV(path.join(".","data.csv")))