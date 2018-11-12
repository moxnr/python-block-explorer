# Inlämning P1 Max Nerman

import requests
import json
rpc_user = 'alice'
rpc_pass = 'bob'
url = 'http://%s:%s@localhost:8332' % (rpc_user, rpc_pass)
headers = {'content-type': 'application/json'}

# Get general information about blockchain 
payload = {
    "method": "getblockchaininfo"
}
response = requests.post(url, data=json.dumps(payload), headers=headers).json()

# Find block by number
def findBlockByNum():
    print('Ange blocknummer:')
    num = int(input())
    firstPayload = {
        "method": "getblockhash",
        "params": [ num ],
    }
    response = requests.post(url, data=json.dumps(firstPayload), headers=headers).json()
    secondPayload = {
        "method": "getblock",
        "params": [ response['result']],
    }
    secondResponse = requests.post(url, data=json.dumps(secondPayload), headers=headers).json()
    blockInfo = secondResponse['result']
    print(response)
    print(blockInfo)
    # Printa resultat
    print('-------------------')
    print('Block hash: ' + response['result'])
    print('Prev. hash: ' + blockInfo['previousblockhash'])
    print('Merkle root: ' + blockInfo['merkleroot'])
    print('Height: ' + str(blockInfo['height']))
    print('Time: ' + str(blockInfo['time']))
    print('Difficulty: ' + str(blockInfo['difficulty']))
    print('Transactions ' + str(blockInfo['nTx']))
    for index in range(len(blockInfo['tx'])):
        print('Tx ' + str(index) + ' : ' + blockInfo['tx'][index])

# Find block by hash
def findBlockByHash():
    print('Ange hashnummer:')
    hash = str(input())
    secondPayload = {
        "method": "getblock",
        "params": [ hash ],
    }
    secondResponse = requests.post(url, data=json.dumps(secondPayload), headers=headers).json()
    blockInfo = secondResponse['result']
    print(blockInfo)
    # Print the result
    print('-------------------')
    print('Block hash: ' + hash)
    print('Prev. hash: ' + blockInfo['previousblockhash'])
    print('Merkle root: ' + blockInfo['merkleroot'])
    print('Height: ' + str(blockInfo['height']))
    print('Time: ' + str(blockInfo['time']))
    print('Difficulty: ' + str(blockInfo['difficulty']))
    print('Transactions ' + str(blockInfo['nTx']))
    for index in range(len(blockInfo['tx'])):
        print('Tx ' + str(index) + ' : ' + blockInfo['tx'][index])

# Find transaction through hash
def findTransaction():
    print('Ange transaktions-hash: ')
    id = str(input())
    payload = {
        "method": "getrawtransaction",
        "params": [ id, 1 ]
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    transaction = response['result']
    print(response)
    # Print the result
    print('-------------------')
    print('Txid:  ' + transaction['txid'])
    print('Blockhash: ' + transaction['blockhash'])
    print('Inputs: ' + str(len(transaction['vin'])))
    print('Outputs: ' + str(len(transaction['vout'])))
    for index in range(len(transaction['vout'])):
        output = ''
        # Check for coinbase transaction cases containing no addresses
        if transaction['vout'][index]['scriptPubKey']['type'] == 'nulldata':
            output = 'Ingen address'
        else:
            output = str(transaction['vout'][index]['value']) + ' BTE till: ' + str(transaction['vout'][index]['scriptPubKey']['addresses'][0])
        print('Output ' + str(index) + ': ' + output) 

# 

print('Bitcoin Edu utforskare')
print('==============================')
print('Antal block:', response['result']['blocks'], 'blocks')
print('==============================')

# Menu with different block explorer options
def menu():
    menuOption = int(input('\nMeny\n1.  Visa block (ange nr)\n2.  Visa block (ange hash)\n3.  Visa transaktion\n4.  Lista outputs för adress\n'))
    print('Du valde: ' + str(menuOption))
    if menuOption == 1:
        findBlockByNum()
    if menuOption == 2:
        findBlockByHash()
    if menuOption == 3:
        findTransaction()
    if menuOption == 4:
        listOutputs()
# A simple loop to keep the program going after each user action
while (1) :
    menu()
    

