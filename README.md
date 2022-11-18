# workshop-python-astra-loader

## Steps

1. [Introduction](#1-introduction)

In this workshop you will learn about building small Python applications to load and query data, while using DataStax Astra DB as its data storage layer.

2. [Setup](#2-database-setup)

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

3. [GitPod - Dev Environment Setup](#3-gitpod-setup)

First, open this repo in Gitpod by right-clicking the following button (select "open in new tab"):

<a href="https://gitpod.io/#https://github.com/datastaxdevs/workshop-python-astra-loader"><img src="images/open_in_gitpod.svg?raw=true" /></a>

In a couple of minutes you will have your Gitpod IDE up and running, with this repo cloned, ready and waiting for you (you may have to authorize the Gitpod single-sign-on to continue).

_Note_: The next steps are to be executed _within the Gitpod IDE._

### Install and configure the Astra CLI

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

### Download the Secure Connect Bundle

The driver also need the "Secure Connect Bundle" zipfile to work (it contains proxy and routing information as well as the necessary certificates).

To download it:

```
astra db download-scb -f secure-connect-workshops.zip workshops
```

You can check it has been saved with `ls *.zip`.

### Configure the dot-env file

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

4. [Simple Demos](#4-simple-demos)

To verify that we've done everything correctly so far, let's run a couple simple scripts.  First, make sure you're in the `21_SimpleDemos` directory:

```
cd 21_SimpleDemos
```

Now, execute the getCassClusterInfo.py script:

```
python getCassClusterInfo.py
```

That should show you some simple properties about your Astra DB cluster:

```
```

Next, let's build a table and load a few rows of data.  If you like, have a look at the [01_cassdemo_emp_cassandraTable.cql](21_SimpleDemos/01_cassdemo_emp_cassandraTable.cql) file.  Once you're done, execute this command to run the CQL commands within:

```
astra db cqlsh workshops -f 01_cassdemo_emp_cassandraTable.cql
```

With the `emp` table created and a few rows of data INSERTed, let's run the `readWriteCassEmp.py` script.  That should show the following output:

```
```

5. [Sales Data Generator](#5-sales-data-generator)

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
token@cqlsh:sales> SELECT * FROM lookup_
lookup_email_servers      lookup_product_categories lookup_usa_states         lookup_user_platforms
token@cqlsh:sales> SELECT * FROM lookup_usa_states LIMIT 4;

 id | state_code | state_name
----+------------+----------------
 23 |         MI |       Michigan
 33 |         NM |     New Mexico
  5 |         CA |     California
 28 |         NC | North Carolina

(4 rows)
```
