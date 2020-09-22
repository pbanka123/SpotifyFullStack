import pylast, time
import requests, json, datetime, requests_cache

# define headers and URL
url = 'http://ws.audioscrobbler.com/2.0/'
USER_AGENT = 'Dataquest'
headers = {'user-agent': USER_AGENT}
counterCache = 0 #keep track of number of times cache was utilized
outData = [] 

requests_cache.install_cache('requests_cache') #creates a local cache in directory

def getUserCreds(user,inFile):
    inData = json.load(open(inFile))
    for ind,d in enumerate(inData):
        if d['credsName'].lower() == user.lower():
            return inData[ind]

def getNumberPages(payload, API_KEY, username):
    payload['api_key'] = API_KEY
    payload['user'] = username
    payload['format'] = 'json'
    response = requests.get(url, headers=headers, params=payload)
    return response.json()['recenttracks']['@attr']['totalPages']

def getRecentlyPlayed(payload, API_KEY, username,inFile,pgNum):
    # Add API key and format to the payload - need to add other pages
    payload['api_key'] = API_KEY
    payload['user'] = username
    payload['format'] = 'json'
    payload['page'] = str(pgNum)
    
    response = requests.get(url, headers=headers, params=payload)
    with open(inFile,'w') as outfile:
        json.dump(response.json(),outfile,indent=4)
    

def getTopGenreTags(payload,API_KEY):
    global counterCache
    payload['method'] = 'artist.getTopTags'
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    response = requests.get(url, headers=headers, params=payload)
    if response.from_cache: #implementing caching
        counterCache += 1
    else:
        time.sleep(0.15) #To ensure rate limiting
    tags = [t['name'] for t in response.json()['toptags']['tag'][:3]]
    if payload['artist'].lower() in tags: #remove occuernces of artist name if exist
        tags.remove(payload['artist'].lower()) 
    # print(tags)
    return ', '.join(tags)

def lastfm_get_track_duration(payload,API_KEY):
    payload['method'] = 'track.getinfo'
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    response = requests.get(url, headers=headers, params=payload)
    obj = response.json()['track']['duration']
    fin = int(int(obj) * 0.001) #to convert to seconds
    return fin 

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def dateStrip(dt):
    your_dt = datetime.datetime.fromtimestamp(int(dt))
    return your_dt.strftime("%Y-%m-%d"), your_dt.strftime("%H:%M:%S")   

def dateDiff(dt,dt1):
    your_dt = datetime.datetime.fromtimestamp(int(dt))
    your_dt1 = datetime.datetime.fromtimestamp(int(dt1))
    fin_dt = your_dt - your_dt1
    return int(fin_dt.total_seconds())

def getTimeOfDay(dt):
    # Morning (0-12), Afternoon (12-5), Evening (5-9), Night (9-12)
    your_dt = datetime.datetime.fromtimestamp(int(dt))
    hour = int(your_dt.strftime("%H"))
    if hour >= 0 and hour < 12:
        return("Morning")
    elif hour >= 12 and hour < 17:
        return("Afternoon")
    elif hour >= 17 and hour < 21:
        return("Evening")
    else:
        return("Night")

def cleanseAndWrite(inFile, outputFile,API_KEY):
    inData = json.load(open(inFile))
    global outData
    trName = inData['recenttracks']['track'][1]['name']
    arName = inData['recenttracks']['track'][1]['artist']['#text']
    dur = lastfm_get_track_duration({
        'artist': arName,
        'track': trName
    },user['API_KEY'])
    # Ignore, first record as it could have currently playing, which doesn't have time
    prevDt = 0
    for ind, d in enumerate(inData['recenttracks']['track'][1:]):       
        each = {}
        each['SongName'] = (d['name']).strip() #get Track Name
        each['Artist'] = (d['artist']['#text']) #get Artist name
        each['Album'] = (d['album']['#text']) #get Album Name
        dt,time = dateStrip(d['date']['uts'])
        each['ArtistTopTags'] = getTopGenreTags({'artist': d['artist']['#text']},user['API_KEY'])
        each['Date'] = dt # get date
        each['Time'] = time #get time
        each['TimeOfDay'] = getTimeOfDay(d['date']['uts'])
        # 1st Song - duration from api, get duration from diff in time, if greater than 500
        # (signifies song was paused) assign duration to 300, & some songs don't have that info 
        if(ind == 0):
            if dur == 0:   dur = 300
            each['durationSec'] = dur
            prevDt = d['date']['uts']
        else:
            duration = dateDiff(prevDt,d['date']['uts'])
            if(duration > 500):
                duration = lastfm_get_track_duration({
                    'artist': d['artist']['#text'],
                    'track': d['name']},user['API_KEY'])
            if duration == 0:   duration = 300
            prevDt = d['date']['uts']
            each['durationSec'] = duration
        outData.append(each)

if __name__ == "__main__":
    # Which user credentials to use
    print("Fetching User API Credentials")
    user = getUserCreds('TeJas','loginCreds.json')

    numPages = getNumberPages({'method': 'user.getrecenttracks'},user['API_KEY'],user['username'])
    for x in range(1,int(numPages)+1):
        print("Processing page number: "+str(x))
        getRecentlyPlayed({'method': 'user.getrecenttracks'},user['API_KEY'],user['username'],user['inFile'],x)
        cleanseAndWrite(user['inFile'],user['outFile'],user['API_KEY'])

    # Dump list into file
    with open(user['outFile'],'w') as outfile:
        json.dump(outData,outfile,indent=4)
    # print("Getting Recent Tracks... ")
    # getRecentlyPlayed({'method': 'user.getrecenttracks'},user['API_KEY'],user['username'],user['inFile'])
    # print("Cleansing Output & Writing to Json file" )
    # cleanseAndWrite(user['inFile'],user['outFile'],user['API_KEY'])
    print("No.of calls to artist tags cache: " + str(counterCache))



    



    