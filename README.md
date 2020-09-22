# SpotifyFullStack
Full Stack project sourcing data from Spotify

## Installations Required
*	Install Homebrew
*	Install Pyenv (Good way to manage diff python versions)
*	pip install requests-cache

## Setup Last.FM
* Create Last.Fm account https://secure.last.fm/login
* Go to: Settings -> Applications -> Connect for both Spotify scrobbling/playback
* Create API account https://www.last.fm/api/account/create. Just full in Application name, Application description, leave last 2 blank.
* Store Credentials

## Setup login creds file (required)
Create a json file "loginCreds.json" and enter in the following information
```
[
    {
        "credsName": "(any name you want)",
        "inFile" : "(input file name).json",
        "outFile" : "(output file name).json",
        "username" : "(lastfm username)",
        "API_KEY" : "(lastfm api key)"
    } (insert comma, followed by more users you would like to have)
]
```

### Notes
* Install/implement caching (for getting artist tags) https://pypi.org/project/requests-cache/

### Reference Websites
* https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
#### LastFM
* https://www.jayblanco.com/blog/2016/7/9/using-lastfm-and-r-to-understand-my-music-listening-habits
* https://github.com/encukou/lastscrape-gui/blob/master/lastexport.py
* https://www.last.fm/api/show/user.getPersonalTags
* https://www.dataquest.io/blog/last-fm-api-python/

