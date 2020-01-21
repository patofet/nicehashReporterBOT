import os
import json
import requests
import time
import os.path
from time import sleep
def location( argument ):
	switcher = {
		0: "EU",
		1: "USA",
	}
	return switcher.get(argument, "Invalid location")

def algorismVelocityUnits( argument ):
	switcher = {
		21: "GH/s",
		24: "Sol/s",
		30: "kH/s",
	}
	return switcher.get(argument, "MH/s")

def algorismText( argument ):
	switcher = {
		0: "Scrypt",
		1: "SHA256",
		2: "ScryptNf",
		3: "X11",
		4: "X13",
		5: "Keccak",
		6: "X15",
		7: "Nist5",
		8: "NeoScrypt",
		9: "Lyra2RE",
		10: "WhirlpoolX",
		11: "Qubit",
		12: "Quark",
		13: "Axiom",
		14: "Lyra2REv2",
		15: "ScryptJaneNf16",
		16: "Blake256r8",
		17: "Blake256r14",
		18: "Blake256r8vnl",
		19: "Hodl",
		20: "DaggerHashimoto",
		21: "Decred",
		22: "CryptoNight",
		23: "Lbry",
		24: "Equihash",
		25: "Pascal",
		26: "X11Gost",
		27: "Sia",
		28: "Blake2s",
		29: "Skunk",
		30: "CryptoNightV7",
		31: "CryptoNightHeavy",
		32: "Lyra2Z",
		33: "X16R",
		34: "CryptoNightV8",
	}
	return switcher.get(argument, argument)
	
bitcoinPrice="https://api.coindesk.com/v1/bpi/currentprice.json"

nicehashAK="id=347165&key=b095ffac-e6e1-331c-4c1d-e5a6625b9dfd"
bitcoinAdress="addr=36WwfnEKfBWHXddE3hQq9NpMuQCKF9CTpQ"
functionWorkers="stats.provider.workers"
functionPayments="stats.provider.payments"
functionWallet="balance"
functionUnpaid="stats.provider.ex"
urlAPInicehash = "https://api.nicehash.com/"

token="nJ9xTtsMQAJ0Ht984JAHrLF7eoDRayrIlUek-7btU5F"
eventTelegram="nicehashTelegram"
eventGoogle="nicehashGoogleSheets"

urlIFTTTtelegram="https://maker.ifttt.com/trigger/"+eventTelegram+"/with/key/"+token
urlIFTTTgoogle="https://maker.ifttt.com/trigger/"+eventGoogle+"/with/key/"+token

myResponseMiners = requests.get(urlAPInicehash+"api?method="+functionWorkers+"&"+bitcoinAdress)
myResponseWallet = requests.get(urlAPInicehash+"api?method="+functionWallet+"&"+nicehashAK)
myResponseUnpaid = requests.get(urlAPInicehash+"api?method="+functionUnpaid+"&"+bitcoinAdress)
myResponsePayment = requests.get(urlAPInicehash+"api?method="+functionPayments+"&"+bitcoinAdress)
myResponsePrice = requests.get(bitcoinPrice)
bitcoinPrice=0.0
eurSymbol=""
walletBalance=""
walletBalanceBtc=0.0
walletBalanceEur=0.0
stringWorkers=""
unpaidBalance=0.0
proyectedMonthIncome=0
segonsUnMes=2419200 #28d=2419200s 29d=2505600s 30d=2592000s 31d=2678400s
lastPaidEpoch=0
proyectedMonthPaidIncome=""
proyectedMonthPaidIncomeBTC=0.0
proyectedMonthPaidIncomeEUR=0.0
if(myResponseMiners.ok):
	jMiners = json.loads(myResponseMiners.content)
	miners={}
	for key in jMiners:
		if(key=="result"):
			for keyIn in jMiners[key]:
				if(keyIn=="workers"):
					for keyInIn in jMiners[key][keyIn]:
						name=keyInIn[0]
						algorism = str(algorismText(keyInIn[6]))
						speed=keyInIn[1].get('a','0.0')+algorismVelocityUnits(keyInIn[6])
						if(miners.get(name,'')==''):
							miners[name]="<b>"+name+":<b><br>&nbsp;&nbsp;"+algorism+"("+speed+")"
						else:
							miners[name]=miners[name]+"<br>&nbsp;&nbsp;"+algorism+"("+speed+")"
	keylist = miners.keys()
	keylist.sort()
	for key in keylist:
		stringWorkers+=miners[key]+"<br>"
if(myResponsePrice.ok):
	jPrice = json.loads(myResponsePrice.content)
	bitcoinPrice=float(jPrice['bpi']['EUR']['rate_float'])
	eurSymbol=jPrice['bpi']['EUR']['symbol']
if(myResponseWallet.ok):
	jWallet = json.loads(myResponseWallet.content)
	walletBalanceBtc=float(jWallet['result']['balance_confirmed'])
	walletBalanceEur=round(walletBalanceBtc*bitcoinPrice,2)
	walletBalance="<b>Wallet:</b>"+str(walletBalanceBtc)+"BTC("+str(walletBalanceEur)+eurSymbol+")<br><b>BTC price:</b>"+str(round(bitcoinPrice,2))+eurSymbol+"<br>"
if(myResponseUnpaid.ok):
	if(myResponsePayment.ok):
		jUnpaid = json.loads(myResponseUnpaid.content)
		jPaymen = json.loads(myResponsePayment.content)
		for (i, item) in enumerate(jUnpaid['result']['current']):
			unpaidBalance+=float(item['data'][1])
		currentEpoch=int(time.time())
		
		for (i, item) in enumerate(jPaymen['result']['payments']):
			if(item['time'] > lastPaidEpoch):
				lastPaidEpoch=item['time']
		proyectedMonthPaidIncomeBTC=round(((segonsUnMes*unpaidBalance)/(currentEpoch-lastPaidEpoch)),8)
		proyectedMonthPaidIncomeEUR=round(proyectedMonthPaidIncomeBTC*bitcoinPrice,2)
		proyectedMonthIncome="<b>Monthly income:</b>"+str(proyectedMonthPaidIncomeBTC)+"BTC("+str(proyectedMonthPaidIncomeEUR)+eurSymbol+")"

requests.post(urlIFTTTtelegram, data={'value1':stringWorkers,'value2':walletBalance,'value3':proyectedMonthIncome})
requests.post(urlIFTTTgoogle, data={'value1':str(round(bitcoinPrice,2)).replace('.',',')+"|||"+stringWorkers,'value2':str(walletBalanceBtc).replace('.',',')+"|||"+str(walletBalanceEur).replace('.',','),'value3':str(proyectedMonthPaidIncomeBTC).replace('.',',')+"|||"+str(proyectedMonthPaidIncomeEUR).replace('.',',')})
