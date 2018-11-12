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

# Find all outputs of address
def listOutputs():
    print('Ange adress: ')
    address = str(input())
    print('-------------------')
    print('Söker efter adress: ' + address)
    # Get the search-span of blocks 
    totalBlocks = response['result']['blocks']
    searchBlock = totalBlocks - 2000
    startBlock = searchBlock
    searchedBlocks = 0
    # Iterate through blocks and their transactions to find matching addresses
    while searchBlock <= totalBlocks:
        # Print number of searched blocks
        if searchBlock == startBlock + 500:
            searchedBlocks += 500
            startBlock += 500
            print(searchedBlocks)
        # Check block for transactions
        firstPayload = {
            "method": "getblockhash",
            "params": [ searchBlock ],
        }
        secondResponse = requests.post(url, data=json.dumps(firstPayload), headers=headers).json()
        secondPayload = {
            "method": "getblock",
            "params": [ secondResponse['result']],
        }
        thirdResponse = requests.post(url, data=json.dumps(secondPayload), headers=headers).json()
        transactions = thirdResponse['result']
        # Iterate transactions to find address
        for index in range(len(transactions['tx'])):
            payload = {
                "method": "getrawtransaction",
                "params": [ transactions['tx'][index], 1 ]
            }
            fourthResponse = requests.post(url, data=json.dumps(payload), headers=headers).json()
            rawTransaction = fourthResponse['result']
            for secondIndex in range(len(rawTransaction['vout'])):
                if rawTransaction['vout'][secondIndex]['scriptPubKey']['type'] == 'nulldata':
                    break
                elif rawTransaction['vout'][secondIndex]['scriptPubKey']['addresses'][0] == address: 
                    output = str(rawTransaction['vout'][secondIndex]['value']) + ' BTE'
                    print('Block ' + str(searchBlock) + ', Tx: ' + transactions['tx'][index])
                    print('output: ' + transactions['tx'][secondIndex])
        # Test adress 1eduGsrvBJcfyTMij2rYXk9viiVV78PNq
        # Increase to search next block
        searchBlock += 1 

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
    

