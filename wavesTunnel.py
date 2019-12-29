import sqlite3 as sqlite
import requests
import datetime
import time
import base58
import pywaves as pw
import traceback

class WavesTunnel(object):

    def __init__(self, config):
        self.config = config
        self.dbCon = sqlite.connect('gateway.db')

        self.node = config['waves']['node']

        cursor = self.dbCon.cursor()
        self.lastScannedBlock = cursor.execute('SELECT height FROM heights WHERE chain = "Waves"').fetchall()[0][0]

    def getLatestBlockHeight(self):
        # height - 1 due to NG!
        latestBlock = requests.get(self.node + '/blocks/height').json()['height'] - 1

        return latestBlock

    def iterate(self):
        dbCon = sqlite.connect('gateway.db')

        while True:
            try:
                nextBlockToCheck = self.getLatestBlockHeight() - self.config['waves']['confirmations']

                if nextBlockToCheck > self.lastScannedBlock:
                    self.lastScannedBlock += 1
                    self.checkBlock(self.lastScannedBlock, dbCon)
                    cursor = dbCon.cursor()
                    cursor.execute('UPDATE heights SET "height" = ' + str(self.lastScannedBlock) + ' WHERE "chain" = "Waves"')
                    dbCon.commit()
            except Exception as e:
                self.lastScannedBlock -= 1
                print('Something went wrong during waves block iteration: ')
                print(traceback.TracebackException.from_exception(e))

            time.sleep(self.config['waves']['timeInBetweenChecks'])

    def checkBlock(self, heightToCheck, dbCon):
        print('checking waves block at: ' + str(heightToCheck))
        blockToCheck =  requests.get(self.node + '/blocks/at/' + str(heightToCheck)).json()
        for transaction in blockToCheck['transactions']:
            if transaction['type'] == 4 and transaction['recipient'] == self.config['waves']['gatewayAddress'] and transaction['assetId'] == self.config['waves']['assetId']:
                cursor = dbCon.cursor()
                targetAddress = base58.b58decode(transaction['attachment']).decode()
                if len(targetAddress) > 1 and self.txNotYetExecuted(transaction['id'], dbCon):
                    #amount = transaction['amount'] - (int(self.config['tn']['fee'] * 10 ** self.config['tn']['decimals']))
                    amount = transaction['amount'] / 10 ** self.config['waves']['decimals']
                    amount -= self.config['tn']['fee']
                    amount *= 10 ** self.config['tn']['decimals']
                    amount = int(amount)
                    
                    pw.setNode(node=self.config['tn']['node'], chain=self.config['tn']['network'], chain_id='L')
                    tnAddress = pw.Address(seed = self.config['tn']['gatewaySeed'])
                    try:
                        addr = pw.Address(targetAddress)
                        tx = tnAddress.sendAsset(pw.Address(targetAddress), pw.Asset(self.config['tn']['assetId']), amount, '', '', 2000000)
                        print("sended tx"+str(tx))
                    except Exception as e:
                        tx = {"id":"invalid attachment"}
                        print('invalid attachment')                    
                    
                    dateTimeObj = datetime.datetime.now()
                    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                    cursor.execute('INSERT INTO executed ("sourceAddress", "targetAddress", "wavesTxId", "tnTxId", "timestamp", "amount", "amountFee") VALUES ("' + transaction['sender'] + '", "' + targetAddress + '", "' + tx['id'] + '", "' + transaction['id'] + '", "' + timestampStr +  '", "' + str(amount) + '", "' + str(self.config['tn']['fee']) + '")')
                    dbCon.commit()
                    print('outgoing transfer completed')

    def txNotYetExecuted(self, transaction, dbCon):
        cursor = dbCon.cursor()
        result = cursor.execute('SELECT wavesTxId FROM executed WHERE wavesTxId = "' + transaction + '"').fetchall()

        return len(result) == 0
