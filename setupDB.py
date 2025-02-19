import sqlite3 as sqlite
import requests

def createdb():
    createHeightTable = '''
        CREATE TABLE IF NOT EXISTS heights (
            id integer PRIMARY KEY,
            chain text NOT NULL,
            height integer
        );
    '''
    createTableExecuted = '''
        CREATE TABLE IF NOT EXISTS executed (
            id integer PRIMARY KEY,
            sourceAddress text NOT NULL,
            targetAddress text NOT NULL,
            tnTxId text NOT NULL,
            wavesTxId text NOT NULL,
            timestamp timestamp
            default current_timestamp,
            amount real,
            amountFee real
    );
    '''
    createTableErrors = '''
        CREATE TABLE IF NOT EXISTS errors (
            id integer PRIMARY KEY,
            sourceAddress text ,
            targetAddress text ,
            tnTxId text ,
            wavesTxId text ,
            timestamp timestamp
            default current_timestamp,
            amount real,
            error text,
            exception text
    );
    '''

    con = sqlite.connect('gateway.db')
    cursor = con.cursor()
    cursor.execute(createHeightTable)
    cursor.execute(createTableExecuted)
    cursor.execute(createTableErrors)
    con.commit()
    con.close()

def createVerify():
    createVerifyTable = '''
        CREATE TABLE IF NOT EXISTS verified (
            id integer PRIMARY KEY,
            chain text NOT NULL,
            tx text NOT NULL,
            block integer
        );
    '''
    con = sqlite.connect('gateway.db')
    cursor = con.cursor()
    cursor.execute(createVerifyTable)
    con.commit()
    con.close()

def initialisedb(config):
    #get current TN block:
    tnlatestBlock = requests.get(config['dcc']['node'] + '/blocks/height').json()['height'] - 1

    #get current Waves block:
    waveslatestBlock = requests.get(config['waves']['node'] + '/blocks/height').json()['height'] - 1

    con = sqlite.connect('gateway.db')
    cursor = con.cursor()
    cursor.execute('INSERT INTO heights ("chain", "height") VALUES ("Waves", ' + str(waveslatestBlock) + ')')
    cursor.execute('INSERT INTO heights ("chain", "height") VALUES ("DCC", ' + str(tnlatestBlock) + ')')
    con.commit()
    con.close()
