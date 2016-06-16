import boto.dynamodb
conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id='',
        aws_secret_access_key='')

print conn.list_tables()



import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

# Uses your ``aws_access_key_id`` & ``aws_secret_access_key`` from either a
# config file or environment variable & the default region.
users = Table.create('items', schema=[
HashKey('rfid'), # defaults to STRING data_type
RangeKey('pname'),
], throughput={    
        'read': 1,
       'write': 1,
  }, global_indexes=[
     GlobalAllIndex('EverythingIndex', parts=[
          HashKey('tray_status'),
      ],
      throughput={
            'read': 1,
            'write': 1,
     })
],
 # If you need to specify custom parameters, such as credentials or region,
 # use the following:
 # connection=boto.dynamodb2.connect_to_region('us-east-1')
print("Table status:", table.table_status)
)
