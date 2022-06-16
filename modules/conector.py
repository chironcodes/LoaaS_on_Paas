import time
import uuid
import os
from google.cloud import datastore

# Only required if you're outside GCP environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'


class interface_datastore:



    def __init__(self):
        self.client = datastore.Client()



    def insertEntity(self, from_who, to_you, pictures):
        try:
            unique_key = uuid.uuid4()
            key = self.client.key('Page', str(unique_key))
            entity = datastore.Entity(key=key, exclude_from_indexes=['pictures'])
            entity.update({
            'from_who': from_who,
            'to_you': to_you,
            'when': time.time(),
            'pictures': pictures,
            })
            self.client.put(entity)
            return unique_key
        
        except Exception as e:
            print(str(e))
            return False


    def getEntity(self, from_who:str, to_you:str, key: str):
        try:
            key = self.client.key('Page', str(key))
            content = self.client.get(key)
            if content['from_who']==from_who and content['to_you']==to_you:
                return self.client.get(key)
            else:
                return False
        except Exception as e:
            print(str(e))
            return False    