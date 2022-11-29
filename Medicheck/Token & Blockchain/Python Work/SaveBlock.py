import json
import web3

from web3 import Web3, HTTPProvider
from os.path import dirname, join

def save(data):

    # truffle development blockchain address
    blockchain_address = 'http://192.168.0.19:7545'
    # Client instance to interact with the blockchain
    web3 = Web3(HTTPProvider(blockchain_address))
    # Set the default account (so we don't need to set the "from" for every transaction call)
    web3.eth.defaultAccount = "0x0ca25e9b99CeCA1bA67097F7299CB8007445e261"

    # Path to the compiled contract JSON file
    compiled_contract_path = join(dirname(__file__), "StoreUserData.json")
    # Deployed contract address (see `migrate` command output: `contract address`)
    deployed_contract_address = '0xF4F6Ce782B2748721DF1f1A83d519dc4A8598C99'

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    # Fetch deployed contract reference
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    # executes setPayload function
    tx_hash = contract.functions.setPayload(data).transact() #could be this?
    # waits for the specified transaction (tx_hash) to be confirmed
    # (included in a mined block)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    hashReturn = ('tx_hash: {}'.format(tx_hash.hex()))

    return hashReturn