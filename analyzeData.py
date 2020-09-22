import time, json, datetime
from datetime import date

counter, morning, noon, evening, night = 0,0,0,0,0
morningDur, noonDur, eveningDur, nightDur = 0,0,0,0

def getUserCreds(user,inFile):
    inData = json.load(open(inFile))
    for ind,d in enumerate(inData):
        if d['credsName'].lower() == user.lower():
            return inData[ind]

def usageThroughDay(timeOfDay,duration):
    global morning, noon, evening, night
    global morningDur, noonDur, eveningDur, nightDur
    if timeOfDay == 'Morning': 
        morning += 1
        morningDur += duration
    elif timeOfDay == 'Afternoon': 
        noon += 1
        noonDur += duration
    elif timeOfDay == 'Evening': 
        evening += 1
        eveningDur += duration
    else: 
        night += 1
        nightDur += duration

def analyzeFile(inFile,currentDate):
    global counter
    inData = json.load(open(inFile))
    for ind, d in enumerate(inData):
        if d['Date'] == currentDate: #In order to only process current date's
            counter += 1
        else:
            break
        usageThroughDay(d['TimeOfDay'],d['durationSec'])
        
    # Convert to min
    print("Songs played today: "+str(counter))

if __name__ == "__main__":
    print("Running Data Analyzer")
    print("Fetching User API Credentials")
    user = getUserCreds('TeJas','loginCreds.json')

    print("Analyzing File..")
    curDate = date.today().strftime("%Y-%m-%d") #Passing in current date
    analyzeFile(user['outFile'],curDate)

    print(morning, noon, evening, night)
    morningDurMin, noonDurMin, eveningDurMin, nightDurMin = int(morningDur/60), int(noonDur/60), int(eveningDur/60), int(nightDur/60)
    print(morningDurMin, noonDurMin, eveningDurMin, nightDurMin)
    