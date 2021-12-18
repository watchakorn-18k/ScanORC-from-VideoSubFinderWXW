# How to use
* Download [Scaner-ORC.exe](https://github.com/watchakorn-18k/ScanORC-from-VideoSubFinderWXW/blob/master/Scaner-ORC.exe)
* Bring the file to the source address of the program VideoSubFinder
![Exsample](https://cdn.discordapp.com/attachments/581018943041306641/921795938228506684/unknown.png)
* Create new project and download credentials.json file from [Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python)
* put credentials.json file beside Scaner-ORC.exe
* Install the Google Client Library using
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
* Create a folder named File_srt and raw_texts
* [You can watch the video here](https://youtu.be/JXbL-PEoT4I)


# How to develop 
* [Install python](https://www.python.org/)
* Create new project and download credentials.json file from [Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python)
* put credentials.json file beside main.py
* Install the Google Client Library using
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
* Export images using [VideoSubFinder](https://sourceforge.net/projects/videosubfinder/) and put them in images folder
* Run main.py and login with google account (only for first time)
* Wait until it complete processing evey image.