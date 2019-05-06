from re import sub
import os
import csv

#define headers

person_headers = {'node_id':'INT', 
               'name':'VARCHAR(100)', 
               'job':'VARCHAR(100)', 
               'birthday':'VARCHAR(10)'}
               
knows_headers = {'source_node_id':'INT',
               'target_node_id':'INT'}                          

def makeSQLFile(file_name, headers, dbname, primarykey, extradata):
    cwd = os.getcwd() # current working directory
    inputfile = open(f"{cwd}/{file_name}.csv","r")
    outputfile = open(f"{cwd}/{file_name}.sql", "w+")
    table = createTable(dbname, headers, primarykey)
    inserts = makeInsertStatements(file_name, headers, inputfile, outputfile, dbname)
    outputfile.write(table)
    outputfile.write(inserts)
    outputfile.write(extradata)
    outputfile.close()
    
def createTable(name, headers, primarykey):
    sql = f"CREATE DATABASE IF NOT EXISTS `socialnetwork`;\nUSE `socialnetwork`;\n\n"
    sql += f"drop table if exists {name};\n"
    sql += f"create table {name} (\n"
    sql += ", \n".join([f"\t{header} {sql_type}" for header,sql_type in headers.items()])
    if(primarykey):
        sql += f",\n\tprimary key({list(headers.keys())[0]})"
    sql += f"\n);\n"
    print(f'created table {name}')
    return sql
 
def valueOf(v, sql_type):
    if sql_type == "INT":
        return v
    return f'"{v}"' 
 
def makeInsertStatements(name, headers, infile, outfile, dbname):
    print("Writing inserts ",end='')
    headerline = infile.readline()
    csv_headers = headerline.rstrip().split(",")
    headerIndex = { h : csv_headers.index(h) for h in headers.keys()}
    sql = ""
    csv_in = csv.reader(infile, delimiter=',', quotechar='"')
    columns = ','.join(headers.keys())
    count = 0
    for row in csv_in:
        if row[-1] != "": # some positions are missing
            if(count == 0):
                sql += f"INSERT INTO {dbname} ( {columns} ) VALUES "
            sql_values = [valueOf(row[headerIndex[k]], headers[k]) for k in headers.keys()]
            values_combined = ','.join(sql_values)
            sql += f"({values_combined})"
            count +=1
            if(count >= 100000):
                count = 0
                sql += ";\n"
            else:
                sql += ",\n"
    return sql[:-2]
	
extraIndices = '''
;ALTER TABLE Knows
ADD INDEX indexSourceNodeID (source_node_id ASC),
ADD INDEX indexDestinatiionNodeID (target_node_id ASC);
'''
 
makeSQLFile("archive_graph/social_network_nodes", person_headers, "Person", True, "")
makeSQLFile("archive_graph/social_network_edges", knows_headers, "Knows", False, extraIndices)