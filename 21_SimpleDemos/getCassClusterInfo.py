#!/usr/bin/env python

### import cassConnectionManager.py and other required libraries
#from cassConnectionManager import cassConnect
#replacing with Stefano Lottini's dbConnection
from dbConnection import get_session
import sys

### sys.version_info.major : to identify python version (major release identifier)

try:
	session = get_session()

	### execute queries
	cass_output_1 = session.execute("SELECT cluster_name, release_version FROM system.local")
	for cass_row in cass_output_1:
		output_message = "Connected to " + str(cass_row.cluster_name) + " and it is running " + str(cass_row.release_version) + " version."
		print(output_message)

except Exception as e:
	### something went wrong
	print("something went wrong.")
	print("")
	print(e)
else:
	### all went well
	print("Done.")


### close connection to cassandra cluster
#cc.disconnect_from_cassandra()
# now happens in shutdown_driver() in dbConnection
