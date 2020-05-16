# Routine to download and upload all data to server
# Richard Paul
# May 16 2020
#
#
#

import quandl
import pandas
import requests
import json
import pyodbc

#
#
#metadata function handling

def meta_url_builder(datatable):
    front = 'https://www.quandl.com/api/v3/datatables/'
    const = 'SHARADAR/'
    target = datatable
    end = '/metadata.json'
    apikey = 'xxx'
    url = front+const+target+end+apikey
    return url

def request_handler(url):
    pull = requests.get(url)
    pull.json()
    return pull

def meta_parser(file):
    temp = []
    primary_keys = []
    dump = json.dumps(file)
    parse = json.loads(dump)
    for topkey, subdict in parse.items():
        for subkey, value in subdict.items():
            if subkey == 'columns':
                for cols in value:
                    temp.append(cols)
            if subkey == 'primary_key':
                for keys in value:
                    primary_keys.append(keys)
    headers = []
    for i in temp:
        values = []
        for vals in i.values():
            values.append(vals)
        headers.append(values)
    
    for j in range(len(primary_keys)):
        temp = []
        temp.append(primary_keys[j])
        temp.append('Primary Key')
        headers.append(temp)

    return headers



#
#
#various data functions

def data_handler(datatable):
    quandl.ApiConfig.api_key = "xxx"
    const = 'SHARADAR/'
    data = quandl.get_table(const+datatable,paginate=True)
    return data

def data_headers(data):
    headers = data.columns.tolist()
    return headers

def rename_headers(meta,data):
    columns = []
    for i in range(len(meta)):
        columns.append(meta[i][0])

    currentcolumns = data_headers(data)
    data.columns = columns
    return data

def get_keys(headers):
    primarykeys = []
    for i in range(len(headers)-1,0,-1):
        if headers[i][1] == 'Primary Key':
            primarykeys.append(headers[i][0])
            del headers[i]
    return primarykeys

def count_items(data):
    return len(data)

def paramater_mapping(data):
    for r in data.columns.values:
        data[r] = data[r].map(str)
        data[r] = data[r].map(str.strip)   
    tuples = [tuple(x) for x in data.values]

    string_list = ['NaT', 'nan', 'NaN', 'None']

    def remove_wrong_nulls(x):
        for r in range(len(x)):
            for i,e in enumerate(tuples):
                for j,k in enumerate(e):
                    if k == x[r]:
                        temp=list(tuples[i])
                        temp[j]=None
                        tuples[i]=tuple(temp)

    remove_wrong_nulls(string_list)

    def chunks(l, n):
        n = max(1, n)
        return [l[i:i + n] for i in range(0, len(l), n)]

    paramaters = chunks(tuples, 1000)
    return paramaters



#
#
#string functions 

def create_tr(headers,datatables,keys):
    stringbuilder = ''
    callfunction = "CREATE TABLE "
    tablename = datatables

    stringbuilder = callfunction+tablename+" ("


    for i in range(0,len(headers),1):
        

        bool = False
        for k in range(0,len(keys),1):
            if headers[i][0] == keys[k]:
                bool = True
                stringbuilder += headers[i][0]+" "
                if headers[i][1] == 'String': 
                    stringbuilder += 'varchar(255) NOT NULL, '
                elif headers[i][1] == 'Integer': 
                    stringbuilder += 'int NOT NULL, '
                elif headers[i][1] == 'Date': 
                    stringbuilder += 'Date NOT NULL, '
            

        if not(bool):
            stringbuilder += headers[i][0]+" "
            if headers[i][1] == 'String': stringbuilder += 'varchar(255) NULL, '
            elif headers[i][1] == 'Integer': stringbuilder += 'int NULL, '
            elif headers[i][1] == 'Date': stringbuilder += 'Date NULL, '



    stringbuilder += 'Primary Key ('
    if len(keys) > 1:
        for c in range(-1,len(keys)-1,1):
            if c < len(keys)-2: stringbuilder += keys[c]+", "
            else: stringbuilder += keys[c]+"));"

    return stringbuilder

def build_reserved_list():
    a_file = open("Reserved.txt", "r")   
    list_of_lists = [(line.strip()).split() for line in a_file]
    a_file.close()
    reserved = []
    for i in range(0,len(list_of_lists)-1,1):
        reserved.append(list_of_lists[i][0])
    return reserved

def check_for_reserved(headers):
    check = build_reserved_list()
    for i in range(0,len(headers)-1,1):
        for x in range(0,len(check)-1,1):
            if headers[i][0].lower() == check[x].lower(): headers[i][0] = 'fin_'+headers[i][0]
    return headers                

def insert_string(headers,datatables):
    stringbuilder = ""
    tableid = datatables
    querytype = "INSERT INTO "+tableid+" ("
    vstring = 'VALUES '

    cols = count_items(headers) - 1

    columnsstring = ""
    valuesstring = "("+("?, "*(cols))+"?)"

    for i in range(len(headers)-1):
        if i < len(headers)-2:  columnsstring += headers[i][0]+", "
        else: columnsstring += headers[i][0]+") "

    stringbuilder += querytype+columnsstring+vstring+valuesstring
    return stringbuilder



#
#
#connection functions

def start_connection():
    server = 'xxx' 
    database = 'xxx' 
    username = 'xxx' 
    password = 'xxx' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password )
    cursor = cnxn.cursor()
    return cursor

def query(query,params):
    cursor = start_connection()
    for i in range(len(params)):
        cursor.executemany(query, params[i])
    cursor.commit()
    cursor.close()

def querysingle(query):
    cursor = start_connection()
    cursor.execute(query)
    cursor.commit()
    cursor.close()




def main():
    running = True
    datatables = [xxx]


    print("Preparing to File Download")
    print("How many datatables?")
    print("The max is:")
    print(len(datatables))
    total = int(input("Please input a value-------------------"))
    
    dt = ''
    for i in range(total):
        dt = datatables[i]
    
    print("Program Commencing")

    while(running):
        #phase 1: Get Initial Metadata & Create Table
        response = request_handler(meta_url_builder(dt))
        headers = check_for_reserved(meta_parser(response.json()))
        print(headers)
        keys = get_keys(headers)
        query1 = create_tr(headers,dt,keys)
        print(query1)
        querysingle(query1)
        print('Phase 1 is complete')


        #phase 2: 
        predata = data_handler(dt)
        data = rename_headers(headers,predata)
        query2 = insert_string(headers,dt)
        print(query2)
        params = paramater_mapping(data)
        query(query2,params)
        print('Phase 2 is complete')
        running = False

        #phase 3



main()






