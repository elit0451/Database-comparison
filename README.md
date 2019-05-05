# Database comparison - <img src="https://pngimg.com/uploads/mysql/mysql_PNG9.png" height="40" align="center"> vs <img src="https://go.neo4j.com/rs/710-RRC-335/images/neo4j_logo_globe.png" height="40" align="center"> (MySQL vs Neo4j)
</br>

In this repository <img src="https://cdn.iconscout.com/icon/premium/png-256-thumb/repository-15-834642.png" height="18"> we will bring into your attention a **MySQL** and a **Neo4j** database <img src="https://image.flaticon.com/icons/svg/148/148825.svg" height="18">. 
</br>We will initialize the databases with data of an artificial social network <img src="https://trello-attachments.s3.amazonaws.com/5a0c1bbf93b2d2556f9cc845/5a1d5bbf034dbe3bcf832cf0/2c8f6c9ea06bcd9f7aa83a0b59827140/socialNetwork.png" height="40" align="center">. That network consists of persons <img src="https://trello-attachments.s3.amazonaws.com/5a0c1bbf93b2d2556f9cc845/5a1d5bbf034dbe3bcf832cf0/9e587ab061dd7797aebfb1be424eb8ce/people-icon-in-various-color-vector-21092005.jpg" height="20" align="center"> (users of a platform such as LinkedIn) and endorsements <img src="https://trello-attachments.s3.amazonaws.com/5a0c1bbf93b2d2556f9cc845/5a1d5bbf034dbe3bcf832cf0/ba9a3fe0f8b72850b2618876b000bdc0/blue-handshake-icon-flat-style-vector-11304772.jpg" height="20" align="center">(the acknowledgment of another person).

</br>

With this exercise we will execute a small experiment in which we will _compare runtimes_ of various queries on the two databases and _report the measured results_<img src="https://i.ibb.co/DkGjv3L/law-scale-icon-justice-outline-icon-vector-17484259.jpg" height="20" align="center">, as well as possible _explanation_ and _conclusions_ for the observations will be provided. :nerd_face:

</br>

----
<a name="toc"></a>
## Table of Contents <img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46db978826878dba87e6ab03f60da1cd6416743e7853e37a25cbb77ef1132d43434d0eee1e020a17b8eb8339a3e46979820e5ae8d76b5d72943411adb0d41beb57bb72895d99a4fedb1294b7607caddecd5d340c041f83fe5830a29148cc5bf64be94b57b65e.png" align="center" height="45"> 
* [Exercise 1](#ex1)
* [Exercise 2](#ex2)
* [Exercise 3](#ex3)
* [Exercise 4](#ex4)
* [Exercise 5](#ex5)

<br/>

----
<a name="ex1"></a>
## Excercise 1 - Setup an SQL and a Neo4j database ![Generic badge](https://img.shields.io/badge/Setup-databases-informational.svg)
**Commands** for starting up Docker containers :whale::
> Neo4j:
```c#
docker run -d --rm --name neo4j --publish=7474:7474 --publish=7687:7687 -v $(pwd):/var/lib/neo4j/import --env NEO4J_AUTH=neo4j/fancy99Doorknob --env NEO4J_dbms_memory_heap_max__size=2G neo4j

```
> MySQL:
```c#
docker run --rm --name my_mysql -d -v $(pwd)/db_data:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

</br>

---
<a name="ex2"></a>
## Excercise 2 - Importing data into the databases ![Generic badge](https://img.shields.io/badge/Data-import-yellowgreen.svg)

_NB_ :bangbang: _The files mentioned in the following queries can be found in [archive_graph.tar.gz](./archive_graph.tar.gz)._

> Import into Ne04j <img src="https://cdn-ak.f.st-hatena.com/images/fotolife/V/Vastee/20180509/20180509140835.gif" height="40" align="center">
```javascript
USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///archive_graph/social_network_nodes.csv" AS row 
    FIELDTERMINATOR ","
WITH row
CREATE (p:Person {
    node_id:row["node_id"],
    name: row["name"],
    job: row["job"],
    birthday: row["birthday"]
    })


USING PERIODIC COMMIT 1000    
LOAD CSV WITH HEADERS FROM "file:///archive_graph/social_network_edges.csv" AS row 
    FIELDTERMINATOR ","
WITH row
MATCH (person:Person {node_id:row["source_node_id"]}), (anotherPerson:Person {node_id:row["target_node_id"]})
CREATE (person)-[:KNOWS]->(anotherPerson)
```
</br>

> Import into MySQL <img align="center" height="20" src="https://thumbs.gfycat.com/CelebratedComplexDipper-max-1mb.gif">

<br/>

----
<a name="ex3"></a>
## Excercise 3 - Construct queries in SQL and in Cypher ![Generic badge](https://img.shields.io/badge/Query-construction-yellow.svg)

#### I. All persons that a person endorses (endorsements of depth :one:)
> Cypher
```javascript
MATCH(:Person {node_id:'16'})-[:KNOWS*1..1]->(known:Person)
RETURN known.name
```
> SQL
```sql
SELECT Person.name 
FROM Knows
INNER JOIN Person ON target_node_id = Person.node_id
WHERE source_node_id = 16;
```
<br/>

#### II. All persons that are endorsed by endorsed persons of a person (endorsements of depth :two:)
> Cypher
```javascript
MATCH(:Person {node_id:'16'})-[:KNOWS*2..2]->(known:Person)
RETURN known.name
```
> SQL
```sql
WITH depthOne AS
	(SELECT Person.* 
	FROM Knows
	INNER JOIN Person ON target_node_id = Person.node_id
	WHERE source_node_id = 16)
SELECT Person.name 
FROM depthOne
INNER JOIN Knows ON Knows.source_node_id = depthOne.node_id
INNER JOIN Person ON Person.node_id = Knows.target_node_id;
```
<br/>

#### III. All persons that ... (endorsements of depth :three:)
> Cypher
```javascript
MATCH(:Person {node_id:'16'})-[:KNOWS*3..3]->(known:Person)
RETURN known.name
```
> SQL
```sql
WITH depthOne AS
	(SELECT Person.* 
	FROM Knows
	INNER JOIN Person ON target_node_id = Person.node_id
	WHERE source_node_id = 16),
depthTwo AS
	(SELECT Person.* 
	FROM depthOne
	INNER JOIN Knows ON Knows.source_node_id = depthOne.node_id
	INNER JOIN Person ON Person.node_id = Knows.target_node_id)
SELECT Person.name 
FROM depthTwo
INNER JOIN Knows ON Knows.source_node_id = depthTwo.node_id
INNER JOIN Person ON Person.node_id = Knows.target_node_id;
```
<br/>

#### IV. All persons that ... (endorsements of depth :four:)
> Cypher
```javascript
MATCH(:Person {node_id:'16'})-[:KNOWS*4..4]->(known:Person)
RETURN known.name
```
> SQL
```sql
WITH depthOne AS
	(SELECT Person.* 
	FROM Knows
	INNER JOIN Person ON target_node_id = Person.node_id
	WHERE source_node_id = 16),
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

```
<br/>

#### V. All persons that ... (endorsements of depth :five:)
> Cypher
```javascript
MATCH(:Person {node_id:'16'})-[:KNOWS*5..5]->(known:Person)
RETURN known.name
```
> SQL
```sql
WITH depthOne AS
	(SELECT Person.* 
	FROM Knows
	INNER JOIN Person ON target_node_id = Person.node_id
	WHERE source_node_id = 16),
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

```
<br/>

----
<a name="ex4"></a>
## Excercise 4 -

<br/>

----
<a name="ex5"></a>
## Excercise 5 -
