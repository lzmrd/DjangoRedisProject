from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/173d16289b9343a18d3bc53f0b95df73'))
    address = '0x56384F933CC79f6F316D09AaAf411C9CFF60b05A'
    privateKey = '0x93e10620c6346d8e8604b7af79a97c91a0561425721f64f13af98160572f3bc1'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice= w3.eth.gasPrice
    value= w3.toWei(0.9 ,'ether')
    signedTX = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice = gasPrice,
        gas = 100000,
        to ='0x687422eEA2cB73B5d3e242bA5456b782919AFc85',
        value=value,
        data=message.encode ('utf-8')
    ), privateKey)

    tx= w3.eth.sendRawTransaction(signedTX.rawTransaction)
    txId = w3.toHex(tx)
    return txId