import sqlite3 as sqlite
import json
import threading
from tntunnel import TNTunnel
from wavesTunnel import WavesTunnel
from flask import Flask, render_template

app = Flask(__name__)

with open('config.json') as json_file:
    config = json.load(json_file)

@app.route('/')
def hello():
    heights = getHeights()

    return render_template('index.html', chainName = config['waves']['name'],
                           wavesHeight = heights['Waves'],
                           tnHeight = heights['TN'],
                           tnAddress = config['tn']['gatewayAddress'],
                           wavesAddress = config['waves']['gatewayAddress'])

@app.route('/heights')
def getHeights():
    dbCon = sqlite.connect('gateway.db')

    result = dbCon.cursor().execute('SELECT chain, height FROM heights WHERE chain = "Waves" or chain = "TN"').fetchall()

    return { result[0][0]: result[0][1], result[1][0]: result[1][1] }

def main():
    tnTunnel = TNTunnel(config)
    wavesTunnel = WavesTunnel(config)
    wavesThread = threading.Thread(target=wavesTunnel.iterate)
    ercThread = threading.Thread(target=tnTunnel.iterate)
    wavesThread.start()
    ercThread.start()
    app.run(port=8080, host='0.0.0.0')

main()
