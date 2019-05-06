import sys
import mysql.connector
import random
import statistics

from neo4j import GraphDatabase
from time import time

# connecting to MySQL
def rootconnect():
    try:
        pw = '123456'
        conn = mysql.connector.connect( host='localhost', database='socialnetwork',user='root', password=pw)
        conn.autocommit = True
        return conn;
    except Exception as ex:
        print(str(ex), file=sys.stderr)
    

conn = rootconnect()

# function to execute queries in MySQL
def sqlQuery(sqlString):
    global conn
    try:
        if not conn.is_connected():
            conn = rootconnect()
        cursor = conn.cursor()
        cursor.execute(sqlString)
        res = cursor.fetchall()
        return res
    except Exception as ex:
        print(str(ex), file=sys.stderr)
    finally:    
        cursor.close()


# connecting to Neo4j
uri = "bolt://localhost:7687"
auth=("neo4j", "fancy99Doorknob")

# function to execute queries in Neo4j
def neo(command, driver):
    try:
        with driver.session() as session:
            result = session.run(command)
        return result # result is a resultset/cursor for neo4j
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        
def neov(command):
    try:
        driver = GraphDatabase.driver(uri, auth=auth)
        return neo(command, driver).values()
    except Exception as ex:
        return 'Something went wrong!'
    finally:
        driver.close()
        

## defining queries for getting the people on different endorsement depths

# contains the queries for depth 1, 2, 3, 4, 5
mySqlQueries = [
'''
SELECT Person.name 
FROM socialnetwork.Knows
INNER JOIN Person ON target_node_id = Person.node_id
WHERE source_node_id = $$id$$;
''',
'''
WITH depthOne AS
	(SELECT Person.* 
	FROM socialnetwork.Knows
	INNER JOIN Person ON target_node_id = Person.node_id
	WHERE source_node_id = $$id$$)
SELECT Person.name 
FROM depthOne
INNER JOIN Knows ON Knows.source_node_id = depthOne.node_id
INNER JOIN Person ON Person.node_id = Knows.target_node_id;
''',
'''
WITH depthOne AS
	(SELECT Person.* 
	FROM socialnetwork.Knows
	INNER JOIN Person ON target_node_id = Person.node_id
	WHERE source_node_id = $$id$$),
depthTwo AS
	(SELECT Person.* 
	FROM depthOne
	INNER JOIN Knows ON Knows.source_node_id = depthOne.node_id
	INNER JOIN Person ON Person.node_id = Knows.target_node_id)
SELECT Person.name 
FROM depthTwo
INNER JOIN Knows ON Knows.source_node_id = depthTwo.node_id
INNER JOIN Person ON Person.node_id = Knows.target_node_id;
''',
'''
WITH depthOne AS
	(SELECT Person.* 
	FROM socialnetwork.Knows
	INNER JOIN Person ON target_node_id = Person.node_id
	WHERE source_node_id = $$id$$),
depthTwo AS
	(SELECT Person.* 
	FROM depthOne
	INNER JOIN Knows ON Knows.source_node_id = depthOne.node_id
	INNER JOIN Person ON Person.node_id = Knows.target_node_id),
depthThree AS
	(SELECT Person.* 
	FROM depthTwo
	INNER JOIN Knows ON Knows.source_node_id = depthTwo.node_id
	INNER JOIN Person ON Person.node_id = Knows.target_node_id)
SELECT Person.name 
FROM depthThree
INNER JOIN Knows ON Knows.source_node_id = depthThree.node_id
INNER JOIN Person ON Person.node_id = Knows.target_node_id;
''',
'''
WITH depthOne AS
	(SELECT Person.* 
	FROM socialnetwork.Knows
	INNER JOIN Person ON target_node_id = Person.node_id
	WHERE source_node_id = $$id$$),
depthTwo AS
	(SELECT Person.* 
	FROM depthOne
	INNER JOIN Knows ON Knows.source_node_id = depthOne.node_id
	INNER JOIN Person ON Person.node_id = Knows.target_node_id),
depthThree AS
	(SELECT Person.* 
	FROM depthTwo
	INNER JOIN Knows ON Knows.source_node_id = depthTwo.node_id
	INNER JOIN Person ON Person.node_id = Knows.target_node_id),
depthFour AS
	(SELECT Person.* 
	FROM depthThree
	INNER JOIN Knows ON Knows.source_node_id = depthThree.node_id
	INNER JOIN Person ON Person.node_id = Knows.target_node_id)
SELECT Person.name 
FROM depthFour
INNER JOIN Knows ON Knows.source_node_id = depthFour.node_id
INNER JOIN Person ON Person.node_id = Knows.target_node_id;
'''
]

neo4jQuery = '''
MATCH(:Person {node_id:$$id$$})-[:KNOWS*$$depth$$..$$depth$$]->(known:Person)
RETURN known.name
'''


# choose and execute SQL query
def executeSql(depth, id):
	query = mySqlQueries[depth-1]
	query = query.replace('$$id$$', str(id))
	
	# calculate the execution time
	start = time()
	sqlQuery(query)
	end = time()
	
	return(end - start)
	
# choose and execute Neo4j query
def executeNeo4j(depth, id):
	query = neo4jQuery.replace('$$id$$', str(id)).replace('$$depth$$', str(depth))
	
	# calculate the execution time
	start = time()
	neov(query)
	end = time()
	
	return(end - start)



sqlTimes = [[], [], [], [], []]
neo4jTimes = [[], [], [], [], []]
	
# entry points and generation of random numbers to be executed in the databases
for i in range(0, 20):
	randomNr = random.randint(0, 500000)
	print('Id - ' + str(randomNr))
	
	for depth in range (1, 6):
		print('\tDepth - ' + str(depth))
		
		sqlTime = executeSql(depth, randomNr)
		sqlTimes[depth-1].append(sqlTime)
		
		neo4jTime = executeNeo4j(depth, randomNr)
		neo4jTimes[depth-1].append(neo4jTime)
		
		print('\t\tSQL time - ' + str(sqlTime)[:7])
		print('\t\tNeo4j time - ' + str(neo4jTime)[:7])
		
print("\n\n\tAverages")
# find averages for SQL and Neo4j	
for depth in range (1, 6):
	print('\nSQL average for depth ' + str(depth) + '\t-\t' + str(statistics.mean(sqlTimes[depth-1])))
	print('Neo4j average for depth ' + str(depth) + ' -\t' + str(statistics.mean(neo4jTimes[depth-1])))
	
	
# find median for SQL and Neo4j	
print("\n\n\tMedians")
for depth in range (1, 6):
	print('\nSQL median for depth ' + str(depth) + '\t-\t' + str(statistics.median(sqlTimes[depth-1])))
	print('Neo4j median for depth ' + str(depth) + ' -\t' + str(statistics.median(neo4jTimes[depth-1])))
		
	