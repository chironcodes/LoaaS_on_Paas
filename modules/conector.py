from google.cloud import datastore
import time
import uuid
import os

# Only required if you're outside GCP environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'


class interface_datastore:



    def __init__(self):
        self.client = datastore.Client()



    def insertEntity(self, from_who, to_you):
        try:
            unique_id = uuid.uuid4()
            key = self.client.key('Page', str(unique_id))
            entity = datastore.Entity(key=key)
            entity.update({
            'from_who': from_who,
            'to_you': to_you,
            'when': time.time(),
            'pics': 'abla',
            })
            self.client.put(entity)

            if self.getEntity(key):
                return unique_id
            else:
                return False
        except Exception as e:
            print(str(e))
            return False


    def getEntity(self, key: str):
        try:
            return self.client.get(key)
        except Exception as e:
            print(str(e))
            return False    