# Database comparison - <img src="https://pngimg.com/uploads/mysql/mysql_PNG9.png" height="40" align="center"> vs <img src="https://go.neo4j.com/rs/710-RRC-335/images/neo4j_logo_globe.png" height="40" align="center"> (MySQL vs Neo4j)
</br>

In this repository <img src="https://cdn.iconscout.com/icon/premium/png-256-thumb/repository-15-834642.png" height="18"> we will bring into your attention a **MySQL** and a **Neo4j** database <img src="https://image.flaticon.com/icons/svg/148/148825.svg" height="18">. 
</br>We will initialize the databases with data of an artificial social network <img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46db978826878dba87e6ab03f60da1cd6416723e7952e37a23cbb07ff1112243434d0eee1e020a17b8eb8339a3e46979820e5ae8d76b5d72943411adb0d41beb57bb72895d99a4fedb1294b7607caddecd5d340c041083fe5830a7984fcb5ef442e74457b65e.png" height="40" align="center">. That network consists of persons <img src="https://trello-attachments.s3.amazonaws.com/5a0c1bbf93b2d2556f9cc845/5a1d5bbf034dbe3bcf832cf0/9e587ab061dd7797aebfb1be424eb8ce/people-icon-in-various-color-vector-21092005.jpg" height="20" align="center"> (users of a platform such as LinkedIn) and endorsements <img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46db978826878dba87e6ab03f60da1cd6416723e7952e37a23cbb07ff1172d43434d0eee1e020a17b8eb8339a3e46979820e5ae8d76b5d72943411adb0d41beb57bb72895d99a4fedb1294b7607caddecd5d340c041083fe5830a7984fcb5ff74de74c53b65e.png" height="20" align="center">(the acknowledgment of another person).

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
To make following this README easier we would ask you to create a new folder in a location of your preference and then navigate to it within your shell/terminal.
</br>

To initialize the databases using Docker is quite **easy** by executing the following commands :whale::
> Neo4j:
```c#
docker run -d --rm --name neo4j --publish=7474:7474 --publish=7687:7687 -v ${PWD}:/var/lib/neo4j/import --env NEO4J_AUTH=neo4j/fancy99Doorknob --env=NEO4J_dbms_memory_pagecache_size=4G --env=NEO4J_dbms_memory_heap_initial__size=4G --env=NEO4J_dbms_memory_heap_max__size=4G neo4j
```

</br>

> MySQL:

_NB_ :bangbang: _Be sure to create a `db_data` folder inside your current location_
</br>

```c#
docker run --rm --name my_mysql -d -v ${PWD}/db_data:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql --max-allowed-packet=1073741824
```
</br>

It is important to notice that we have set the **heap max size** of Neo4j to **4GB** of memory to be sure we won’t have additional timings on our queries for RAM swapping. If you are a Windows user <img src="https://images.all-free-download.com/images/graphiclarge/windows_81_default_icon_pack_6830210.jpg" height="20" align="center">, execute the previous commands in PowerShell.
</br>

<p align="right">
<a href="#toc"><img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46e1999b248790ebc3abaf51ab57f5973d047d317c06a6722887e27de91429570d564ead490e5b10aaf8db29b4aa2e32db025fb28c341521842f1bbeb98b15be04bf22834b80bfbb8f49c0e92f68.png" width="30"></a>
</p>

---
<a name="ex2"></a>
## Excercise 2 - Importing data into the databases ![Generic badge](https://img.shields.io/badge/Data-import-yellowgreen.svg)

_NB_ :bangbang: _The files mentioned in the following queries can be found in [here](https://github.com/datsoftlyngby/soft2019spring-databases/raw/master/data/archive_graph.tar.gz). Extract the file into a folder named **archive_graph**._

We are starting to work with big files, and for this reason the importing had to be thought through. Due to the files being quite big, we have decided to provide the [script](./sqlDataScriptsGenerator.py) we used to build the SQL insertion queries instead of uploading them by themselves.

</br>

> Import into Ne04j <img src="https://cdn-ak.f.st-hatena.com/images/fotolife/V/Vastee/20180509/20180509140835.gif" height="40" align="center">

To import data to Neo4j the steps are a bit simpler, _“all”_ you have to do is load up your favourite browser on the page `http://localhost:7474` and within the query field insert the following statements:

```javascript
CREATE CONSTRAINT ON (p:Person) ASSERT p.node_id IS UNIQUE
```
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
```
```javascript
USING PERIODIC COMMIT 1000    
LOAD CSV WITH HEADERS FROM "file:///archive_graph/social_network_edges.csv" AS row 
    FIELDTERMINATOR ","
WITH row
MATCH (person:Person {node_id:row["source_node_id"]}), (anotherPerson:Person {node_id:row["target_node_id"]})
CREATE (person)-[:KNOWS]->(anotherPerson)
```

These two commands should create all the nodes you need from the data and create the appropriate relationships between.

</br>
</br>

> Import into MySQL <img align="center" height="20" src="https://thumbs.gfycat.com/CelebratedComplexDipper-max-1mb.gif">

To proceed with this step, you will need Python. If you don’t have Python you can use Docker by running this command:
`docker run -it --rm -v ${PWD}:/tmp -w /tmp python sh -c "python3 sqlDataScriptsGenerator.py"`

Do make sure you have the files to import in a folder named **archive_graph** in the current directory. </br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _Ex. PreviouslyCreatedNewFolder > archive_graph > social_network_edges.csv_


Running this command should leave you with two files on the same directory (**archive_graph**) with the extension **.sql**. You can then grab the SQL commands from there and import them with your favorite tool (MySQL workbench, mysqlimport, etc.)

</br>

The following figure demonstrates the ER diagram of the created `socialnetwork` database:

<p align="center">
<img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46db978826878dba87e6ab03f60da1cd6416723e7952e37b26cbb170f1112243434d0eee1e020a17b8eb8339a3e46979820e5ae8d76b5d72943411adb0d41beb57bb72895d99a4fedb1294b7607caddecd5d340c041f83fe5830a79849c15ef348e94d53b65e.png" width="55%">
</p>

<p align="right">
<a href="#toc"><img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46e1999b248790ebc3abaf51ab57f5973d047d317c06a6722887e27de91429570d564ead490e5b10aaf8db29b4aa2e32db025fb28c341521842f1bbeb98b15be04bf22834b80bfbb8f49c0e92f68.png" width="30"></a>
</p>

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

<p align="right">
<a href="#toc"><img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46e1999b248790ebc3abaf51ab57f5973d047d317c06a6722887e27de91429570d564ead490e5b10aaf8db29b4aa2e32db025fb28c341521842f1bbeb98b15be04bf22834b80bfbb8f49c0e92f68.png" width="30"></a>
</p>

----
<a name="ex4"></a>
## Excercise 4 - Writing an execution program ![Generic badge](https://img.shields.io/badge/Execution-program-green.svg)

A program in Python <img src="https://www.python.org/static/opengraph-icon-200x200.png" height="25" align="center"> was written where we can automatically execute the above queries for twenty random nodes against the two respective databases. It can be found in [databasePerformanceFinder.py](./databasePerformanceFinder.py)

</br>

To be able to run it you once again will need Python, and if you are running them within your computer (not through the following docker command) be sure to install the following packages for Python: **mysql-connector-python** and **neo4j**. 

These can normally be installed through the following commands:

`pip install mysql-connector-python`</br>
`pip install neo4j`

</br>

In case you don’t have python installed on your machine you can run the application through the following command: 

```c#
docker run -it --rm --net=host -v ${PWD}:/tmp -w /tmp python sh -c "pip install mysql-connector-python && pip install neo4j && python3 databasePerformanceFinder.py"
```
<br/>

<p align="right">
<a href="#toc"><img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46e1999b248790ebc3abaf51ab57f5973d047d317c06a6722887e27de91429570d564ead490e5b10aaf8db29b4aa2e32db025fb28c341521842f1bbeb98b15be04bf22834b80bfbb8f49c0e92f68.png" width="30"></a>
</p>

----
<a name="ex5"></a>
## Excercise 5 - Measure the average and median execution times of each query ![Generic badge](https://img.shields.io/badge/Average-median-inactive.svg?labelColor=9cf)

> Times of each query for each id

Within this table you can find all the single execution results (in seconds) that were gathered to calculate the _average_ and the _median_ in the next section.

<table>
    <tr>
        <th>
            Person ID
        </th>
        <th>
        </th>
        <th>
            Depth 1
        </th>
        <th>
            Depth 2
        </th>
        <th>
            Depth 3
        </th>
        <th>
            Depth 4
        </th>
        <th>
            Depth 5
        </th>
    </tr>
    <tr>
        <td align="center">
             <b>97452</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.03653</td>
                </tr>
                <tr>
                    <td align="center">1.22664</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.37388</td>
                </tr>
                <tr>
                    <td align="center">0.39445</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">3.51995</td>
                </tr>
                <tr>
                    <td align="center">3.01810</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">24.1196</td>
                </tr>
                <tr>
                    <td align="center">17.8080</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">184.538</td>
                </tr>
                <tr>
                    <td align="center">86.7519</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>255867</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00437</td>
                </tr>
                <tr>
                    <td align="center">0.06993</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.01433</td>
                </tr>
                <tr>
                    <td align="center">0.08220</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.27315</td>
                </tr>
                <tr>
                    <td align="center">0.09300</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">8.06737</td>
                </tr>
                <tr>
                    <td align="center">1.06203</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">101.861</td>
                </tr>
                <tr>
                    <td align="center">26.3120</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>130040</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00266</td>
                </tr>
                <tr>
                    <td align="center">0.04821</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00825</td>
                </tr>
                <tr>
                    <td align="center">0.03834</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.07310</td>
                </tr>
                <tr>
                    <td align="center">0.04315</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.95411</td>
                </tr>
                <tr>
                    <td align="center">0.31826</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">21.8818</td>
                </tr>
                <tr>
                    <td align="center">6.25341</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>469490</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00269</td>
                </tr>
                <tr>
                    <td align="center">0.04378</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.02635</td>
                </tr>
                <tr>
                    <td align="center">0.04336</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.40049</td>
                </tr>
                <tr>
                    <td align="center">0.14956</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">10.1751</td>
                </tr>
                <tr>
                    <td align="center">2.96481</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">229.032</td>
                </tr>
                <tr>
                    <td align="center">92.4653</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>103304</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.11603</td>
                </tr>
                <tr>
                    <td align="center">0.40534</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.06791</td>
                </tr>
                <tr>
                    <td align="center">0.08176</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.35004</td>
                </tr>
                <tr>
                    <td align="center">0.15943</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">6.67067</td>
                </tr>
                <tr>
                    <td align="center">1.84992</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">81.9830</td>
                </tr>
                <tr>
                    <td align="center">21.8072</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>397769</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00961</td>
                </tr>
                <tr>
                    <td align="center">0.04519</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.02219</td>
                </tr>
                <tr>
                    <td align="center">0.04532</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.27431</td>
                </tr>
                <tr>
                    <td align="center">0.10072</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">5.27164</td>
                </tr>
                <tr>
                    <td align="center">1.27270</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">112.094</td>
                </tr>
                <tr>
                    <td align="center">32.5137</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>51294</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00722</td>
                </tr>
                <tr>
                    <td align="center">0.04765</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00785</td>
                </tr>
                <tr>
                    <td align="center">0.04883</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.15692</td>
                </tr>
                <tr>
                    <td align="center">0.07154</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">3.59671</td>
                </tr>
                <tr>
                    <td align="center">0.90464</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">79.0004</td>
                </tr>
                <tr>
                    <td align="center">22.2726</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>68412</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00243</td>
                </tr>
                <tr>
                    <td align="center">0.04269</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00270</td>
                </tr>
                <tr>
                    <td align="center">0.04347</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.04087</td>
                </tr>
                <tr>
                    <td align="center">0.03597</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.28967</td>
                </tr>
                <tr>
                    <td align="center">0.10296</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">6.11298</td>
                </tr>
                <tr>
                    <td align="center">1.50000</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>198449</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00262</td>
                </tr>
                <tr>
                    <td align="center">0.04068</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.03228</td>
                </tr>
                <tr>
                    <td align="center">0.04822</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.78400</td>
                </tr>
                <tr>
                    <td align="center">0.23565</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">18.0964</td>
                </tr>
                <tr>
                    <td align="center">5.24085</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">469.017</td>
                </tr>
                <tr>
                    <td align="center">324.510</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>91907</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.27356</td>
                </tr>
                <tr>
                    <td align="center">1.56897</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">1.50708</td>
                </tr>
                <tr>
                    <td align="center">0.48353</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">2.81950</td>
                </tr>
                <tr>
                    <td align="center">3.30760</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">15.6674</td>
                </tr>
                <tr>
                    <td align="center">23.6031</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">143.167</td>
                </tr>
                <tr>
                    <td align="center">56.0398</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>258194</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00712</td>
                </tr>
                <tr>
                    <td align="center">0.05558</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.01978</td>
                </tr>
                <tr>
                    <td align="center">0.06205</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.29573</td>
                </tr>
                <tr>
                    <td align="center">0.09378</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">6.21519</td>
                </tr>
                <tr>
                    <td align="center">1.10606</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">102.922</td>
                </tr>
                <tr>
                    <td align="center">29.1510</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>133300</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00487</td>
                </tr>
                <tr>
                    <td align="center">0.05212</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00237</td>
                </tr>
                <tr>
                    <td align="center">0.05019</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.03531</td>
                </tr>
                <tr>
                    <td align="center">0.04259</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.47808</td>
                </tr>
                <tr>
                    <td align="center">0.18823</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">11.6657</td>
                </tr>
                <tr>
                    <td align="center">3.34666</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>241762</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00226</td>
                </tr>
                <tr>
                    <td align="center">0.04657</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00804</td>
                </tr>
                <tr>
                    <td align="center">0.04332</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.07160</td>
                </tr>
                <tr>
                    <td align="center">0.05190</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">1.10339</td>
                </tr>
                <tr>
                    <td align="center">0.33738</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">25.6912</td>
                </tr>
                <tr>
                    <td align="center">7.30859</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>165339</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00311</td>
                </tr>
                <tr>
                    <td align="center">0.04126</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.01533</td>
                </tr>
                <tr>
                    <td align="center">0.04044</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.18578</td>
                </tr>
                <tr>
                    <td align="center">0.07253</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">3.33041</td>
                </tr>
                <tr>
                    <td align="center">0.90306</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">71.1918</td>
                </tr>
                <tr>
                    <td align="center">20.6824</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>179387</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00264</td>
                </tr>
                <tr>
                    <td align="center">0.04644</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.02387</td>
                </tr>
                <tr>
                    <td align="center">0.04269</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.38614</td>
                </tr>
                <tr>
                    <td align="center">0.12717</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">7.92666</td>
                </tr>
                <tr>
                    <td align="center">2.15771</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">177.503</td>
                </tr>
                <tr>
                    <td align="center">52.2270</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>201061</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.01267</td>
                </tr>
                <tr>
                    <td align="center">0.07671</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.04688</td>
                </tr>
                <tr>
                    <td align="center">0.04499</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.57512</td>
                </tr>
                <tr>
                    <td align="center">0.12013</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">13.3445</td>
                </tr>
                <tr>
                    <td align="center">2.06087</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">169.269</td>
                </tr>
                <tr>
                    <td align="center">45.8724</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>345988</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00345</td>
                </tr>
                <tr>
                    <td align="center">0.06435</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.01577</td>
                </tr>
                <tr>
                    <td align="center">0.10779</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.24862</td>
                </tr>
                <tr>
                    <td align="center">0.07026</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">5.69475</td>
                </tr>
                <tr>
                    <td align="center">0.86054</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">76.7484</td>
                </tr>
                <tr>
                    <td align="center">19.9341</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>161060</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.01534</td>
                </tr>
                <tr>
                    <td align="center">0.03560</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.01241</td>
                </tr>
                <tr>
                    <td align="center">0.03631</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.09598</td>
                </tr>
                <tr>
                    <td align="center">0.05508</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">1.96803</td>
                </tr>
                <tr>
                    <td align="center">0.54601</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">45.3058</td>
                </tr>
                <tr>
                    <td align="center">12.7325</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>406091</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00239</td>
                </tr>
                <tr>
                    <td align="center">0.04499</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00984</td>
                </tr>
                <tr>
                    <td align="center">0.04055</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.07678</td>
                </tr>
                <tr>
                    <td align="center">0.05426</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">1.07535</td>
                </tr>
                <tr>
                    <td align="center">0.31957</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">25.7734</td>
                </tr>
                <tr>
                    <td align="center">7.33849</td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td align="center">
            <b>406740</b>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td>MySQL</td>
                </tr>
                <tr>
                    <td>Neo4j</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00319</td>
                </tr>
                <tr>
                    <td align="center">0.04593</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.00294</td>
                </tr>
                <tr>
                    <td align="center">0.04055</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">0.06243</td>
                </tr>
                <tr>
                    <td align="center">0.05141</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">1.68152</td>
                </tr>
                <tr>
                    <td align="center">0.43146</td>
                </tr>
            </table>
        </td>
        <td>
            <table align="center">
                <tr>
                    <td align="center">39.5864</td>
                </tr>
                <tr>
                    <td align="center">10.1191</td>
                </tr>
            </table>
        </td>
    </tr>
</table>

</br>

> Average & Median

The following graphs represent the Average and the Median values (in seconds) for both databases. Since the time difference are significant from depth 3+, we decided to split the graph into 2, therefore, getting a closer look.

<img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46ed9893379182ba9bfcb945e611b2843b492d762a10e17132d0e12de61a79005a5948ae470a5644fdf1df2ff2e03d22884e17ff933c0120996048e6edc00db513bb29814e80b3bb8b48c0ec3827ee82875d73.png" height="70%">

</br>

<img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46ed9893379182ba9bfcb945f61fbcd6395428792c07b7692ac7b62aba1b23030e5a48aa435e0d4dfcf8817da2e26a71d85e19f1c32f0e2a92624cf5f2d75dad0ba8218c4584b3b98d4dc4e8392ce3888c4b2c53.png" height="70%">

| <p align="left">:tangerine: - The <b>orange</b> line represents the Neo4j median</br>:eggplant: - The <b>dark blue</b> line represents the MySQL median </p> | <p align="left">:apple: - The <b>red</b> bar represents the Neo4j average</br>:green_apple:- The <b>green</b> bar represents the MySQL average</p> |
|:-:|:-:|

</br>

### Time differences explanation

We have reached the conclusion that the time differences that occur are due to the fact that **Neo4j** has the relations associated with each node, and therefore it doesn’t need to go through more objects than it should to find the next depth level of persons. This leads **Neo4j** to be able to run on pretty much O(NlogN) complexity. 

**MySQL** on the other hand has to go and find the correct _IDs_, and even with indexes, for bigger depths its run time starts incrementing exponentially.

</br>

### Conclusion
It can be concluded that if you need to go to **shallow depths** (1 or 2 levels deep), **MySQL** might be a better choice regarding execution time. But the moment you want to start knowing the relations at **deeper depths**, **Neo4j** takes the win and should definitely be the correct choice (at least between the two systems analysed in this assignment).
<br/>

<p align="right">
<a href="#toc"><img src="https://waffleio-direct-uploads-production.s3.amazonaws.com/uploads/5b631124103d580013dcf6a4/125516c66e82c728ace21e0d46e1999b248790ebc3abaf51ab57f5973d047d317c06a6722887e27de91429570d564ead490e5b10aaf8db29b4aa2e32db025fb28c341521842f1bbeb98b15be04bf22834b80bfbb8f49c0e92f68.png" width="30"></a>
</p>

----
> #### Assignment made by:   
`David Alves 👨🏻‍💻 ` :octocat: [Github](https://github.com/davi7725) <br />
`Elitsa Marinovska 👩🏻‍💻 ` :octocat: [Github](https://github.com/elit0451) <br />
> Attending "Databses for Developers" course of Software Development bachelor's degree

