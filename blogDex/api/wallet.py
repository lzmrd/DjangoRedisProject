from web3 import Web3

w3 = Web3(Web3.HTTPProvider ('https://goerli.infura.io/v3/173d16289b9343a18d3bc53f0b95df73'))
account = w3.eth.account.create()
privateKey= account.privateKey.hex()
address = account.address

print (f"Your address: {address}\nYour key : {privateKey}")