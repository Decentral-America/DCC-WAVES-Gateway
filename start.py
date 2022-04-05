import sqlite3 as sqlite
import json
import threading
import uvicorn

import setupDB
from tnChecker import TNChecker
from wavesChecker import WavesChecker

with open('config.json') as json_file:
    config = json.load(json_file)

def main():
    #check db
    try:
        dbCon = sqlite.connect('gateway.db')
        result = dbCon.cursor().execute('SELECT chain, height FROM heights WHERE chain = "DCC" or chain = "Waves"').fetchall()
        #dbcon.close()
        if len(result) == 0:
            setupDB.initialisedb(config)
    except:
        setupDB.createdb()
        setupDB.initialisedb(config)

    setupDB.createVerify()

    #load and start threads
    tn = TNChecker(config)
    waves = WavesChecker(config)
    wavesThread = threading.Thread(target=waves.run)
    tnThread = threading.Thread(target=tn.run)
    wavesThread.start()
    tnThread.start()
    
    #start app
    uvicorn.run("gateway:app", host="0.0.0.0", port=config["main"]["port"], log_level="info")

main()
