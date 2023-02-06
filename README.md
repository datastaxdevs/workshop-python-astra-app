# Get Started on Python and NoSQL with Apache Cassandra

<img src="images/python_nosql_workshop.png?raw=true" />

## 📋 Table of contents

1. [Introduction](#1-introduction)
2. [Database Setup](#2-database-setup)
3. [GitPod - Dev Environment Setup](#3-gitpod-setup)
4. [Simple Demos](#4-simple-demos)
5. [Sales Data Generator](#5-sales-data-generator)
6. [What's NEXT ?](#6-whats-next)

## 1. Introduction

In this workshop you will learn about building small Python applications to load and query data, while using DataStax Astra DB as its data storage layer.

## 2. Database Setup

For this workshop you will need an Astra DB instance.  You will be able to create one and use it for free.  If you already have an Astra DB instance, you can certainly use that.

_In case you haven't created your Astra DB cluster yet, go ahead and create it now (for free) by clicking here:_

<a href="https://astra.dev/yt-8-10"><img src="images/create_astra_db_button.png?raw=true" /></a>

 - Database Name: `workshops`
 - Keyspace Name: `sales`

**Note**: the Token that is created with the database does not have all permissions we need, so you _need_ to manually [create a Token](https://awesome-astra.github.io/docs/pages/astra/create-token/) with the higher "DB Administrator" permission and use it in what comes next.

_If you have a database named `workshops` but not a `sales` keyspace,
simply add it using the "Add Keyspace" button on the bottom right hand corner of your DB dashboard._

#### Astra DB "Administrator" token

If you do not have a "DB Administrator" token yet, log in to your Astra DB
and create a token with the "Database Administrator" role.
To create the token, click on the "..." menu next to your database in the main
Astra dashboard and choose "Generate token". Then make sure you select the "Database Administrator" role.
_Download or note down all components of the token before navigating away:
these will not be shown again._
[See here](https://awesome-astra.github.io/docs/pages/astra/create-token/)
for more on token creation.

> **⚠️ Important**
> ```
> The instructor will show the token creation on screen,
> but will then destroy it immediately for security reasons.
> ```

Remember, as mentioned already, _the default Token auto-created for you when
creating the database is not powerful enough for us today._

## 3. GitPod Setup

First, open this repo in Gitpod by right-clicking the following button (select "open in new tab"):

<a href="https://gitpod.io/#https://github.com/datastaxdevs/workshop-python-astra-loader"><img src="images/open_in_gitpod.svg?raw=true" /></a>

In a couple of minutes you will have your Gitpod IDE up and running, with this repo cloned, ready and waiting for you (you may have to authorize the Gitpod single-sign-on to continue).

_Note_: The next steps are to be executed _within the Gitpod IDE._

### 3a. Install and configure the Astra CLI

In a console within Gitpod, provide the "token proper" part of the Token (the string starting with `AstraCS:...`) by running:

```
. ~/.bashrc ; astra setup
```

You will be prompted to paste your Astra token.  Remember, that token needs "Database Administrator" permissions.  The default, auto-generated token will not work.

_(Optional)_ If the above step was successful, try getting some information on your Astra DB by executing the following commands:

```
astra db list
```
```
astra db list-keyspaces workshops
```
```
astra db get workshops
```

### 3b. Download the Secure Connect Bundle

The driver also need the "Secure Connect Bundle" zipfile to work (it contains proxy and routing information as well as the necessary certificates).

To download it:

```
astra db download-scb -f secure-connect-workshops.zip workshops
```

You can check it has been saved with `ls *.zip`.

### 3c. Configure the dot-env file

Copy the template dot-env and edit it with:

```
cp .env.sample .env ; gp open .env
```

Replace the Client ID and Client Secret strings from the database Token.

Finally, `source` the .env file:

```bash
source .env
```

You can verify that your environment variables have been appropriately sourced by executing:

 ```bash
 env | grep ASTRA
 ```

### 3d. Cassandra Python driver

For these examples to work, the Cassandra Python driver will need to be installed.  The GitPod instance has automatically taken care of that, and you can verify it from a terminal with the following command:

```
pip show cassandra-driver
```

## 4. Simple Demos

To verify that we've done everything correctly so far, let's run a couple simple scripts.  First, make sure you're in the `21_SimpleDemos` directory:

### 4a. Python scripts

```
cd 21_SimpleDemos
```

Now, execute the getCassClusterInfo.py script:

```
python getCassClusterInfo.py
```

That should show you some simple properties about your Astra DB cluster:

```
% python getCassClusterInfo.py
Connected to cndb and it is running 4.0.0.6816 version.
Done.
```

Next, let's build a table and load a few rows of data.  If you like, have a look at the [01_cassdemo_emp_cassandraTable.cql](21_SimpleDemos/01_cassdemo_emp_cassandraTable.cql) file.  Once you're done, execute this command to run the CQL commands within:

```
astra db cqlsh workshops -f 01_cassdemo_emp_cassandraTable.cql
```

With the `emp` table created and a few rows of data INSERTed, let's run the `readWriteCassEmp.py` script.

```
python readWriteCassEmp.py
```

That should show the following output:

```
% python readWriteCassEmp.py
---- 1 row inserted -----------------------------------

---- select and print only 1 row ----------------------
-------------------------------------------------------
first_name | last_name | empid
-------------------------------------------------------
Scott | Tiger | 1001
-------------------------------------------------------

---- select and print 5 rows --------------------------
-------------------------------------------------------
first_name | last_name | empid
-------------------------------------------------------
0b1cdc3f78 | c3394c9d7b | 7206
f6b22d5a99 | e721642623 | 6762
Scott | Tiger | 1001
7807b62524 | a7390c4762 | 9278
Queen | John | 1003
-------------------------------------------------------

Done.
```
### 4b. FastAPI

Now let's pull the same data back with restful endpoints.  To begin, we first need to host our service layer with a small webserver.  Uvicorn is a simple webserver for Python, so we'll use that to invoke our simpleDemoApi.py service.

```
uvicorn simpleDemoApi:app
```

Once that's up and running, let's run a quick test on it.  Open another terminal and try the `/cluster_info` endpoint with curl.  Or, you can also open a web browser with the following URL: [http://127.0.0.1:8000/cluster_info](http://127.0.0.1:8000/cluster_info)

```
curl -s -XGET localhost:8000/cluster_info \
     -H 'Content-Type: application/json'
```

Whether you use a browser or the command line, the output should be the same:

```
[{"name":"cndb","version":"4.0.0.6816"}]
```

Now let's reproduce work similar to what we did with `readWriteCassEmp.py`.  First, let's add a new employee to our `emp` table.  We'll add an employee named "Wayne Gretzky" with the employee number of 99.

```
curl -s -XPOST localhost:8000/employee/create \
     -d'{"empid":98,"first_name":"Wayne","last_name":"Gretzky"}' \
     -H 'Content-Type: application/json'
```

The employee number of 99 should be the value returned.  Let's make sure by running a `GET` on the `/employee/{id}` endpoint URL: [http://127.0.0.1:8000/employee/99](http://127.0.0.1:8000/employee/99)

```
curl -s -XGET http://127.0.0.1:8000/employee/99 \
-H 'Content-Type: application/json'
```

This should return the output of:

```
[{"empid":99,"first_name":"Wayne","last_name":"Gretzky"}]
```

Likewise, we can also pull back the first 5 rows of the table, using the `/employees/{limit}` endpoint URL:

[http://127.0.0.1:8000/employees/5](http://127.0.0.1:8000/employees/5)

```
curl -s -XGET http://127.0.0.1:8000/employees/5 \
-H 'Content-Type: application/json'
```

This should return the output of:

```
[{"empid":99,"first_name":"Wayne","last_name":"Gretzky"},
 {"empid":7206,"first_name":"0b1cdc3f78","last_name":"c3394c9d7b"},
 {"empid":6762,"first_name":"f6b22d5a99","last_name":"e721642623"},
 {"empid":1001,"first_name":"Scott","last_name":"Tiger"},
 {"empid":9278,"first_name":"7807b62524","last_name":"a7390c4762"}]
```

## 5. Sales Data Generator

First of all, let's make sure we're in the right directory:

```
cd ../31_SalesApp_AutoSalesGenerator
```

Let's start by making sure that our keyspace has the necessary tables.  Have a look at the [02_sales_create_tables.cql](31_SalesApp_AutoSalesGenerator/02_sales_create_tables.cql) file.  Once you're donw, execute this command to run the CQL commands within:

```
astra db cqlsh workshops -f 02_sales_create_tables.cql
```

Once that script completes, we can verify that it created our new tables with the following command:

```
astra db cqlsh workshops -e "desc keyspace sales"
```

#### ✅ 5a. Lookup Tables

Next, let's load the lookup tables.  Feel free to look through the [03_load_data_in_lookup_tables.cql](31_SalesApp_AutoSalesGenerator/03_load_data_in_lookup_tables.cql) file:

```
astra db cqlsh workshops -f 03_load_data_in_lookup_tables.cql
```

You can verify the contents of the `lookup_product_categories`, `lookup_user_platforms`, `lookup_usa_states`, and `lookup_email_servers` tables with cqlsh:

```
astra db cqlsh workshops
```

You should be able to quickly sample the tables like this:

```
% astra db cqlsh workshops
[INFO]  Secure connect bundles have been downloaded.
[INFO]
Cqlsh is starting, please wait for connection establishment...
Connected to cndb at 127.0.0.1:9042.
[cqlsh 6.8.0 | Cassandra 4.0.0.6816 | CQL spec 3.4.5 | Native protocol v4]
Use HELP for help.
token@cqlsh> use sales;
token@cqlsh:sales> SELECT * FROM lookup_usa_states LIMIT 4;

 id | state_code | state_name
----+------------+----------------
 23 |         MI |       Michigan
 33 |         NM |     New Mexico
  5 |         CA |     California
 28 |         NC | North Carolina

(4 rows)
```

#### ✅ 5b. Generate User and Product Data

Let's have a look at the `globalSettings.py` file.

```python
### https://docs.datastax.com/en/developer/python-driver/3.25/api/cassandra/#cassandra.ConsistencyLevel
CASS_READ_CONSISTENCY  = ConsistencyLevel.LOCAL_QUORUM
CASS_WRITE_CONSISTENCY = ConsistencyLevel.LOCAL_QUORUM

### for small system
TOTAL_USERS    = 1000        # SalesApp_GenerateUsers.py    will generate this number of users
TOTAL_PRODUCTS = 5000        # SalesApp_GenerateProducts.py will generate this number of products
GEN_MAX_ORDERS = 120          # minimum 10. SalesApp_GenerateOrders.py will generate less than this number of orders randomly
GEN_MAX_PRODUCTS_ORDER = 6   # minimum 5. SalesApp_GenerateOrders.py will generate less than this number of products per order randomly
```

Next, let's generate data for users and products.  There are two Python scripts which will randomly generate users and products.  Feel free to take a look at them:
 - [SalesApp_GenerateUsers.py](31_SalesApp_AutoSalesGenerator/SalesApp_GenerateUsers.py)
 - [SalesApp_GenerateProducts.py](31_SalesApp_AutoSalesGenerator/SalesApp_GenerateProducts.py)

The behaviors of these scripts are controlled by the [globalSettings.py](31_SalesApp_AutoSalesGenerator/globalSettings.py) script, which is used as an import.  We've preset the variables with some good defaults.

Let's start by running the [SalesApp_GenerateUsers.py](31_SalesApp_AutoSalesGenerator/SalesApp_GenerateUsers.py) script:
```
% python SalesApp_GenerateUsers.py
100 users generated.
200 users generated.
300 users generated.
400 users generated.
500 users generated.
600 users generated.
700 users generated.
800 users generated.
900 users generated.
1000 users generated.
Done.
```

Next, we will run the [SalesApp_GenerateProducts.py](31_SalesApp_AutoSalesGenerator/SalesApp_GenerateProducts.py) script:
```
% python SalesApp_GenerateProducts.py
1000 products generated.
2000 products generated.
3000 products generated.
4000 products generated.
5000 products generated.
Done.
```

#### ✅ 5c. Generate Order Data

With the users and products generated, we can finally generate orders with the [SalesApp_GenerateOrders.py](31_SalesApp_AutoSalesGenerator/SalesApp_GenerateOrders.py) script:
```
% python SalesApp_GenerateOrders.py
2023-01-09 10:57:29.644454 | 50 orders generated.
93 total orders generated.
Done.
```

#### ✅ 5d. Check Generated Data

Now that everything has been generated, we can have a look at the tables with cqlsh.  We can use the Astra CLI to bring up a cqlsh session with our workshops database like this:

```
% astra db cqlsh workshops
[INFO]  Secure connect bundles have been downloaded.
[INFO]
Cqlsh is starting, please wait for connection establishment...
Connected to cndb at 127.0.0.1:9042.
[cqlsh 6.8.0 | Cassandra 4.0.0.6816 | CQL spec 3.4.5 | Native protocol v4]
Use HELP for help.
token@cqlsh>
```

Let's `use` our sales keyspace and `describe` the tables within:

```
token@cqlsh> use sales;
token@cqlsh:sales> desc tables;

emp                        lookup_usa_states      sales_order_products
lookup_email_servers       lookup_user_platforms  sales_orders
lookup_product_categories  products               users
```

You can sample the generated data using cqlsh:
```
token@cqlsh:sales> SELECT * FROm users LIMIT 10;

 user_id | user_email_id             | user_name    | user_phone_number | user_platform  | user_state_code
---------+---------------------------+--------------+-------------------+----------------+-----------------
     990 |   e7dd093a18f4@icloud.com | e7dd093a18f4 |      852-852-7693 |          Linux |              NV
     655 | c279111c20a4@fastmail.com | c279111c20a4 |      734-491-7328 | Android Tablet |              VA
     937 |    fc1cbfb4b754@lycos.com | fc1cbfb4b754 |      799-215-5954 |        Mozilla |              WA
     111 |     2491ff02c8f4@mail.com | 2491ff02c8f4 |      827-375-5187 | Android Tablet |              AL
     873 |    4f7642b67084@yahoo.com | 4f7642b67084 |      873-894-4802 | Android Tablet |              TN
     412 | 09614cf4eda4@fastmail.com | 09614cf4eda4 |      793-621-2836 |  Android Phone |              DC
     332 |    1b8339b37a04@email.net | 1b8339b37a04 |      812-738-3762 |         iPhone |              IL
     697 |      5ecc01fc8a14@aol.com | 5ecc01fc8a14 |      714-837-8714 |     ChromeBook |              NH
     383 |      1d645c6d44b4@aol.com | 1d645c6d44b4 |      763-129-7112 |        Mozilla |              NH
     314 |     8bcdbf085ee4@mail.com | 8bcdbf085ee4 |      774-335-8667 |        Firefox |              GA

(10 rows)

token@cqlsh:sales> SELECT * FROm products LIMIT 10;

 product_id | product_category | product_code | product_description          | product_name     | product_price | product_qoh
------------+------------------+--------------+------------------------------+------------------+---------------+-------------
       1535 |     Collectibles | b12f191b14c4 |       2f195 16a906 87 97390d |       bb9c9 ebfc |         23.97 |        2759
       1929 |            Games | 9b2795b36994 |     fe5a4 d8d57ac c2 e35e684 |    7a55 2a09c591 |         52.50 |         596
       4292 |  Beauty Products | a90d57817bf4 |        7055b 022bc 49 38899e |    d92e5d56 6a4d |         59.62 |        5161
       1235 |        Magazines | 5d33216893d4 | 3278a 868c13ee aeaa 85e99616 | 55b64e59 f38dcb8 |         42.37 |        3769
       1434 |     Garden Tools | 441c62e1a004 |      d9b6c f2e86 4f 41687b56 |       8bb9c 0b7e |         39.39 |        1354
       2482 |            Music | 6d1deeab3c74 |    8107 cc33f8db fc cbba2b57 |    a1f169a 2df86 |          13.6 |        2773
       3843 |            Games | 0d2e85f96084 |       cd53 756a9 aced 2aa92c |  200df11c a14cb2 |         38.28 |        3454
        990 |       Appliances | 1e91c433ab64 |       e60b 6ce4eb5 2d 9ab10f |   e3fab 02bc801d |         49.27 |         647
       3236 |      Electronics | bf0499ef8cd4 |        6e0f8 029cc cb 436aa8 |   6add32a7 9ef6f |         20.68 |         945
       1041 |            Games | 2a2de6dc1b14 |      5b99 059346 bd1 e70163d |       5d09 e42d7 |         36.55 |        5523

(10 rows)

token@cqlsh:sales> SELECT * FROM sales_orders LIMIT 10;

 order_date | order_date_hour | order_timestamp                 | order_code                           | order_actual_shipping_date | order_discount_percent | order_estimated_shipping_date   | order_grand_total | order_number_of_products | order_total | user_email_id             | user_id | user_name    | user_phone_number | user_platform | user_state_code
------------+-----------------+---------------------------------+--------------------------------------+----------------------------+------------------------+---------------------------------+-------------------+--------------------------+-------------+---------------------------+---------+--------------+-------------------+---------------+-----------------
 2023-01-20 |              15 | 2023-01-20 15:25:05.302000+0000 | 97867e70-b0bb-433c-982a-1bf9002c2e27 |                       null |                      3 | 2023-01-31 00:00:00.000000+0000 |         1365.9443 |                        5 |     1408.19 | 09bacfa1c734@hushmail.com |     239 | 09bacfa1c734 |      895-534-5551 |          iPad |              NC
 2023-01-20 |              15 | 2023-01-20 15:25:06.429000+0000 | 08629a2f-1e8d-439f-b335-5c49e390bab8 |                       null |                      5 | 2023-01-28 00:00:00.000000+0000 |         1521.2825 |                        5 |     1601.35 |    2748de4b7d74@yahoo.com |     826 | 2748de4b7d74 |      838-375-6071 |    BlackBerry |              VA
 2023-01-20 |              15 | 2023-01-20 15:25:07.583000+0000 | e081ff06-457c-4602-859e-fe198c4e056f |                       null |                      1 | 2023-02-03 00:00:00.000000+0000 |         1925.7579 |                        5 |     1945.21 | f686215b1434@hushmail.com |     536 | f686215b1434 |      727-586-9388 |         Linux |              SD
 2023-01-20 |              15 | 2023-01-20 15:25:08.648000+0000 | 956c916a-d5a9-452f-b5df-eecf990c9486 |                       null |                      0 | 2023-01-23 00:00:00.000000+0000 |            958.21 |                        3 |      958.21 | 8051919c0594@hushmail.com |     766 | 8051919c0594 |      818-755-8518 |        iPhone |              NC
 2023-01-20 |              15 | 2023-01-20 15:25:09.365000+0000 | f929daed-8867-4cb2-938b-7629796923a1 |                       null |                      2 | 2023-02-01 00:00:00.000000+0000 |          395.8612 |                        3 |      403.94 | 56fdd656e5d4@fastmail.com |      75 | 56fdd656e5d4 |      879-217-1128 |        Mac OS |              MN
 2023-01-20 |              15 | 2023-01-20 15:25:10.029000+0000 | be405566-6ff7-404d-b081-cc651056abdf |                       null |                      3 | 2023-01-28 00:00:00.000000+0000 |          963.2973 |                        3 |      993.09 |    539933567d94@gmail.com |      53 | 539933567d94 |      838-529-3149 | Android Phone |              MA
 2023-01-20 |              15 | 2023-01-20 15:25:10.727000+0000 | 19058b67-2146-4e5a-aeec-52743146a63e |                       null |                      2 | 2023-02-09 00:00:00.000000+0000 |         1447.8226 |                        5 |     1477.37 |    2395e5b0dba4@lycos.com |     994 | 2395e5b0dba4 |      880-164-2794 | Android Phone |              AL
 2023-01-20 |              15 | 2023-01-20 15:25:11.767000+0000 | b9479b1c-719c-413e-aa5b-0d19716ba775 |                       null |                      0 | 2023-02-09 00:00:00.000000+0000 |            692.45 |                        4 |      692.45 |    35fd9eb1cd24@email.net |     355 | 35fd9eb1cd24 |      851-397-8540 |        iPhone |              OH
 2023-01-09 |              10 | 2023-01-09 10:56:44.471000+0000 | ea372b07-63d1-40ca-ad12-3757fbf25dee |                       null |                      5 | 2023-01-21 00:00:00.000000+0000 |           888.136 |                        4 |      934.88 |   332b20a042f4@icloud.com |     543 | 332b20a042f4 |      840-351-4919 |        iPhone |              MI
 2023-01-09 |              10 | 2023-01-09 10:56:45.838000+0000 | 3b3f5511-13c2-4518-9471-91eb070d4314 |                       null |                      0 | 2023-01-21 00:00:00.000000+0000 |           1647.27 |                        4 |     1647.27 |    302903178444@inbox.com |     528 | 302903178444 |      735-452-2509 |       Mozilla |              HI

(10 rows)

token@cqlsh:sales> SELECT * FROM sales_order_products LIMIT 10;

 order_date | order_code                           | product_id | product_category | product_code | product_name  | product_price_each | product_price_total | product_sold_quantity
------------+--------------------------------------+------------+------------------+--------------+---------------+--------------------+---------------------+-----------------------
 2023-01-09 | 8a711501-f8f6-4ec7-b070-d77a9318db4b |       1074 |        Fine Arts | 3babfc747854 | 5713c3 952888 |              57.35 |              172.05 |                     3
 2023-01-09 | 8a711501-f8f6-4ec7-b070-d77a9318db4b |       4905 |     Pet Supplies | c0376db4ce84 |   1059f3 4829 |               44.0 |               440.0 |                    10
 2023-01-09 | 30386b08-d503-49b9-a478-319a0cb4fa96 |       1043 |         Software | cb7fc23cbc14 |   2e69 4eb50b |              32.82 |              459.48 |                    14
 2023-01-09 | 30386b08-d503-49b9-a478-319a0cb4fa96 |       4258 |       Gift Cards | a1e6d671d654 |  b0553 b48bcf |               43.8 |               481.8 |                    11
 2023-01-09 | 2e81ab4b-045f-4e0c-a9d2-38ac7d549811 |        913 |      Travel Gear | 63ffd5cebd94 |    8f1fd 1f68 |              59.21 |              177.63 |                     3
 2023-01-09 | 2e81ab4b-045f-4e0c-a9d2-38ac7d549811 |       2154 |       Gift Cards | 42ba43214b84 |  bdf64 321b0a |              53.33 |              426.64 |                     8
 2023-01-09 | 2e81ab4b-045f-4e0c-a9d2-38ac7d549811 |       2321 |     Garden Tools | 6b1acebdf0f4 | 22fc5c9 ad313 |              35.11 |              386.21 |                    11
 2023-01-09 | 2e81ab4b-045f-4e0c-a9d2-38ac7d549811 |       2999 |        Fine Arts | 1bdb689915b4 |   7853aa ae94 |              40.79 |              407.90 |                    10
 2023-01-09 | 2e81ab4b-045f-4e0c-a9d2-38ac7d549811 |       3113 |     Garden Tools | 7a96575c96e4 |  62ebd2 eb9c3 |              50.91 |              407.28 |                     8
 2023-01-09 | 736194ba-ad66-405a-b51a-baa97321732e |        959 |      Light Bulbs | 6f58f7706204 |   44b8a2 1e21 |              44.74 |              134.22 |                     3
 ```

 #### ✅ 5e. Sales Data via FastAPI

Before we go too much further, have a look at the [salesAppApi.py](31_SalesApp_AutoSalesGenerator/salesAppApi.py) code.  In it, you can see how we prepared our CQL statements, defined our object models, and exposed our restful endpoints.

Now let's stand-up our FastAPI `SalesAppApi` code with Uvicorn:

```
uvicorn salesAppApi:app
```

Now, let's pull back the top 5 users by hitting the `/users` endpoints with `curl`:

```
curl -s -XGET http://127.0.0.1:8000/users/5 \
-H 'Content-Type: application/json'
```

In the output, look for a specific user's ID.  We can use that ID to pull back specific data for that `user_id`:

```
curl -s -XGET http://127.0.0.1:8000/user/990 \
-H 'Content-Type: application/json'
```

Remember, as these are GET requests, you should be able to run these using a web browser, as well.  Now, let's do the same for products:

```
curl -s -XGET http://127.0.0.1:8000/products/5 \
-H 'Content-Type: application/json'
```

As we did with users above, let's look for a specific `product_id` in our output, and pull back specific data for it:

```
curl -s -XGET http://127.0.0.1:8000/product/1535 \
-H 'Content-Type: application/json'
```

Let's try this with our `orders` endpoint.  First, let's just bring back the first 5 orders:

```
curl -s -XGET http://127.0.0.1:8000/orders/5 \
-H 'Content-Type: application/json'
```

To bring back orders for a specific day, we need to make note of an order's date and hour.  Now, let's use that on our `/orders/date/hour` endpoint:

```
curl -s -XGET http://127.0.0.1:8000/orders/date/2023-01-20/hour/15 \
-H 'Content-Type: application/json'
```

If we wanted to see the specific products for one of those orders, we can take a specific `order_code` from one of the orders shown above.  Then we can use that with our original `order_date` and hit the `/orderproducts/date/code` endpoint:

```
curl -s -XGET http://127.0.0.1:8000/orderproducts/date/2023-01-20/code/b9479b1c-719c-413e-aa5b-0d19716ba775 \
-H 'Content-Type: application/json'
```
## 6. What's NEXT ?

We've just scratched the surface of what you can do using Python with Astra DB or Apache Cassandra.

Go take a look at [DataStax for Developers](https://www.datastax.com/dev) and our DataStax [Developers channel on YouTube](https://www.youtube.com/@DataStaxDevs/featured) to see what else is possible.  There's plenty to dig into!

Congratulations: You made it to the end of today's workshop!

> Sincerely yours, The DataStax Developers
