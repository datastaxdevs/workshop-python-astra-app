#!/usr/bin/env python
import os

### import cassandra driver libraries and other modules
from cassandra.cluster import Cluster
from cassandra.auth    import PlainTextAuthProvider
from cassandra.query   import SimpleStatement
from globalSettings    import *

### connection variables for on-prem Cassandra or DSE
CASS_CONTACT_POINTS    = ["192.168.1.151", "192.168.1.171"] ;
CASS_PORT              = 9042 ;
CASS_USERNAME          = "yourusername" ;
CASS_PASSWORD          = "yourpassword" ;

### connection variables for AstraDB
# AstraDB Portal -> Dashboard -> Serverless Databases -> Connect -> Drivers -> Legacy -> Python -> download Secure Connect Bundle
ASTRA_DB_SECURE_BUNDLE_PATH = os.environ["ASTRA_DB_SECURE_BUNDLE_PATH"]
ASTRADB_CLOUD_CONFIG   = { 'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH }
# AstraDB Portal -> Organization Settings -> Token Management -> Read/Write Service Account -> Generate a New Token -> Download Token Details
ASTRADB_CLIENT_ID      = os.environ["ASTRA_DB_CLIENT_ID"]
ASTRADB_CLIENT_SECRET  = os.environ["ASTRA_DB_CLIENT_SECRET"]

### common db settings
CASS_KEYSPACE          = os.environ["ASTRA_DB_KEYSPACE"] ;


### main class
class cassConnect:

	### init function
	def __init__(self):

		if not USE_ASTRA_DB:
			### prep for cassandra connection
			CASS_AUTH_PROVIDER = PlainTextAuthProvider(username = CASS_USERNAME, password = CASS_PASSWORD)
			self.cass_cluster = Cluster(contact_points = CASS_CONTACT_POINTS, port = CASS_PORT, auth_provider = CASS_AUTH_PROVIDER)
		else:
			### prep for AstraDB connection
			ASTRADB_AUTH_PROVIDER = PlainTextAuthProvider(ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
			self.cass_cluster = Cluster(cloud = ASTRADB_CLOUD_CONFIG, auth_provider = ASTRADB_AUTH_PROVIDER)


		### connect to cassandra cluster or AstraDB and set default keyspace
		self.cass_session = self.cass_cluster.connect(CASS_KEYSPACE)


	### close cassandra connection function
	def disconnect_from_cassandra(self):
		self.cass_cluster.shutdown()
		self.cass_session.shutdown()
		return (0)
