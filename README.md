# Reddit-TTS-Video-Py

Automatically Create Reddit TTS videos and upload

# Usage

Fill the settings.py in scripts.py
Install dependencies
Download client_secret.json from Google Cloud
Run run.py

## Praw:

https://www.reddit.com/prefs/apps


1. Create another app 
2. prawUserAgent is what you put in name field 
3. select script, put anything in desc, leave about url empty if you want
4. In redirect uri put http://localhost
5. Create app
6. prawClientSecret is under secret
7. prawClientId is the string of characters underneath "personal use script"


## Google Cloud

Follow this video: https://youtu.be/6bzzpda63H0 , save the json file as client_secret.json in the root folder (same as run.py)


## Google CSE

1. From the Google Custom Search homepage ( http://www.google.com/cse/ ), click Create a Custom Search Engine.
2. Type a name and description for your search engine.
3. Under Define your search engine, in the Sites to Search box, enter at least one valid URL (For now, just put www.anyurl.com to get past this screen. More on this later ).
4. Select the CSE edition you want and accept the Terms of Service, then click Next. Select the layout option you want, and then click Next.
5. Click any of the links under the Next steps section to navigate to your Control panel.
6. In the left-hand menu, under Control Panel, click Basics.
7. In the Search Preferences section, select Search the entire web but emphasize included sites.
8. Click Save Changes.
9. In the left-hand menu, under Control Panel, click Sites.
10. Delete the site you entered during the initial setup process.
11. googleCseId is under Search Engine ID
12. Go to https://developers.google.com/custom-search/v1/introduction , click Get a key, select the project... that is the googleApiKey


