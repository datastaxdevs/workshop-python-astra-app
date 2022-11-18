## python cassandra-driver
![CassPy.jpg](https://github.com/sarma1807/python-cassandra-driver/blob/master/CassPy.jpg) <br><br>

#### python cassandra-driver is built by DataStax and distributed via : https://pypi.org/project/cassandra-driver/

---

### Latest Verification

```
# 22-October-2022
# this is working properly with following software versions :

Linux OS : CentOS Linux release 7.9.2009 (Core) & CentOS Stream release 9 (5.14.0-171.el9.x86_64)
Python version 3.6.8+
python cassandra-driver 3.25.0
Apache Cassandra 3.11.x / 4.x / including 4.1-beta1
DataStax Enterprise 6.8.x
AstraDB
```

### This code is NO LONGER compatible with Python version 2.x

---

#### https://www.youtube.com/watch?v=c34JLr5UNKE

## Database pre-requisites

For this workshop you will need an Astra DB instance.  You will be able to create one and use it for free.  If you already have an Astra DB instance, you can certainly use that.

_In case you haven't created your Astra DB cluster yet, go ahead and create it now (for free) by clicking here:_

<a href="https://astra.dev/yt-8-10"><img src="images/create_astra_db_button.png?raw=true" /></a>

> _Tip_: call the database `workshops` and the keyspace `sales`.

**Note**: the Token that is created with the database does not have all permissions we need, so you _need_ to manually [create a Token](https://awesome-astra.github.io/docs/pages/astra/create-token/) with the higher "DB Administrator" permission and use it in what comes next.


_If you have a database named `workshops` but no `sales` keyspace,
simply add it using the "Add Keyspace" button on the bottom right hand corner of your DB dashboard._

## Steps

## 1. Setup

#### Astra DB "Administrator" token

If you don't have a "DB Administrator" token yet, log in to your Astra DB
and create a token with this role.
To create the token, click on the "..." menu next to your database in the main
Astra dashboard and choose "Generate token". Then make sure you select the "DB Administrator" role.
_Download or note down all components of the token before navigating away:
these will not be shown again._
[See here](https://awesome-astra.github.io/docs/pages/astra/create-token/)
for more on token creation.

> **⚠️ Important**
> ```
> The instructor will show the token creation on screen,
> but will then destroy it immediately for security reasons.
> ```

Mind that, as mentioned already, _the default Token auto-created for you when
creating the database is not powerful enough for us today._
### Gitpod

First, open this repo in Gitpod by right-clicking the following button ("open in new tab"):

<a href="https://github.com/datastaxdevs/workshop-python-astra-loader"><img src="images/open_in_gitpod.svg?raw=true" /></a>

In a couple of minutes you will have your Gitpod IDE up and running, with this repo cloned, ready and waiting for you (you may have to authorize the Gitpod single-sign-on to continue).

_Note_: The next steps are to be executed _within the Gitpod IDE._

#### Install and configure the Astra CLI

In a console within Gitpod, provide the "token proper" part of the Token (the string starting with `AstraCS:...`) by running:

```
. ~/.bashrc ; astra setup
```

You will be prompted to paste your Astra token.  Remember, that token needs "Database Administrator" permissions.  The default, auto-generated token will not work.

(_Optional)_ Get some information on your Astra DB with:

```
astra db list
astra db list-keyspaces workshops
astra db get workshops
```

#### Download the Secure Connect Bundle

Besides the "Client ID" and the "Client Secret" from the Token, the drivers also need the "Secure Connect Bundle" zipfile to work (it contains proxy and routing information as well as the necessary certificates).

To download it:

```
astra db download-scb -f secure-connect-workshops.zip workshops
```

You can check it has been saved with `ls *.zip`.

#### Configure the dot-env file

Copy the template dot-env and edit it with:

```
cp .env.sample .env ; gp open .env
```

Replace the Client ID and Client Secret strings from the database Token.

Finally, `source` the .env file:

```bash
source .env
```
