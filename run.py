from scripts import upload_video as run
from scripts import settings
import os

params=[settings.prawClientID, settings.prawClientSecret, settings.prawUserAgent, settings.googleApiKey, settings.googleCseId]
for param in params:
    if param=="":
        print("You haven't filled the settings.py file in the scripts folder")
        assert False
if not "client_secret.json" in os.listdir():
    print("You haven't downloaded the client_secret json from Google Cloud or didn't rename it correctly")
    assert False
run()