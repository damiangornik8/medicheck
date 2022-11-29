from web3 import Web3
import time

#Node connecting to kovan testnet on ethereum blockchain
infura_url = "https://kovan.infura.io/v3/59b6285b7b694124ba1243090d23ab89"

web3 = Web3(Web3.HTTPProvider(infura_url))

#Medi-Coin token address
token = "0xFE038741027d9939d25E8305fF606dC3729Fd354"
#Medi-Coin token ABI
abi = '[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_decimals","type":"uint256"},{"internalType":"uint256","name":"_totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'

#Python representation of Medi-Coin token
contract = web3.eth.contract(token, abi=abi)


def checkBalance(address):

    '''
    account2 = "0xc622909339262BD4Ab3699B93449e06E66a96e3E"
    privatekey2 = "e8adc8c0ef9a465c7896192148d3bcdbbf97053de40dc3bad4d61b8e7c2052e3"
    account3 = "0x8a120BeD88f3C79179E0f418AC949bb4230d7E5A"
    privatekey3 = "d0757eabd6d3cdca6fd5e35dc2d25189ac1cd9e815aaabf1b1f13fb7584d27dd"
    '''

    if len(address) == 42:

        #Checking balance of Medi-Coin token in MetaMask wallet
        token_balance = contract.functions.balanceOf(address).call()
        finalBalance = web3.fromWei(token_balance,'ether')
        finalBalance = str(finalBalance)
        length = len(finalBalance)
        if length > 15:
            finalBalance = finalBalance[:-10]

    else:
        finalBalance = "Enter valid address"

    return finalBalance


def checkBalances(address,key):

    if len(address) == 42 and len(key) == 64:

        #MetaMask wallet address
        account = "0xaF343844F24256fb2b882669C64087d6b377E821"
        privatekey = "c62c0f4cb9fd5d554e7f6d5436067db2e58f185d036cb29a9eb59eedc182cb06"

        #Test Wallet
        ethBalance = web3.eth.get_balance(address)
        finalEth = web3.fromWei(ethBalance, 'ether')

        #Main Wallet
        ethBalance2 = web3.eth.get_balance(account)

        token_balance = contract.functions.balanceOf(address).call()
        finalBalance = web3.fromWei(token_balance,'ether')

        finalBalance = str(finalBalance)
        length = len(finalBalance)
        if length > 15:
            finalBalance = finalBalance[:-10]

        finalEth = str(finalEth)
        length = len(finalEth)
        if length > 15:
            finalEth = finalEth[:-10]



        if web3.fromWei(ethBalance, 'ether') < .1:
            enough = "Insufficient Funds for ETH to Medi-Coin exchange"
        elif web3.fromWei(ethBalance, 'ether') >= .1:
            enough = "Sufficient funds available for ETH to Medi-Coin exchange"

    else:
        finalEth = "0"
        finalBalance = "0"



    return finalEth,finalBalance


def exchange(amount,address,key):

    #This code checks to see if the Test wallet has at least .1 ETH
    #If the Test wallet does have enough ETH, then show the ETH balance of two wallets, Main and Test
    #Then send .01 ETH from Test wallet to Main wallet
    #Show updated balances of both wallets upon successful transaction of ETH
    #Show the MC balance of two wallets, Main and Test
    #Then in return, Main wallet sends 6 MC to Test wallet (.01ETH == 6MC (€37))
    #Show updated balances of both wallets upon successful transaction of MC

    if len(address) == 42 and len(key) == 64:

        #MetaMask wallet address
        account = "0xaF343844F24256fb2b882669C64087d6b377E821"
        privatekey = "c62c0f4cb9fd5d554e7f6d5436067db2e58f185d036cb29a9eb59eedc182cb06"


        #Main Wallet
        ethBalance2 = web3.eth.get_balance(account)


        ethBalance = web3.eth.get_balance(address)
        finalEth = web3.fromWei(ethBalance, 'ether')

        token_balance = contract.functions.balanceOf(address).call()
        finalBalance = web3.fromWei(token_balance,'ether')


        if web3.fromWei(ethBalance, 'ether') < .1:
            enough = "Insufficient Funds for ETH to Medi-Coin exchange"
            finalTokenUserBalance = ""
            # get the nonce.  Prevents one from sending the transaction twice




        else:

            allAmounts = []

            if amount == ".01":
                amount2 = 6000000000000000000
                allAmounts.append(amount)
            elif amount == ".02":
                amount2 = 6000000000000000000 * 2
                allAmounts.append(amount)
            elif amount == ".03":
                amount2 = 6000000000000000000 * 3
                allAmounts.append(amount)
            elif amount == ".04":
                amount2 = 6000000000000000000 * 4
                allAmounts.append(amount)
            elif amount == ".05":
                amount2 = 6000000000000000000 * 5
                allAmounts.append(amount)


            if amount in allAmounts:

                nonce = web3.eth.getTransactionCount(address)


                # build a transaction in a dictionary
                tx = {
                    'nonce': nonce,
                    'to': account,
                    'value': web3.toWei(amount, 'ether'),
                    'gas': 210000,
                    'gasPrice': web3.toWei('50', 'gwei')
                }

                # sign the transaction
                signed_tx = web3.eth.account.sign_transaction(tx, key)

                # send transaction
                tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

                web3.toHex(tx_hash)



                time.sleep(10)
                ethBalanceAgain = web3.eth.get_balance(address)


                if web3.fromWei(ethBalanceAgain, 'ether') != web3.fromWei(ethBalance, 'ether'):
                    result = "Exchange of ETH successful"

                    #token_balance = contract.functions.balanceOf(account).call()

                    token_balanceBefore = contract.functions.balanceOf(account).call()


                    nonce = web3.eth.getTransactionCount(account)
                    transaction = contract.functions.transfer(address, amount2).buildTransaction(
                        {'nonce': nonce, 'chainId': 42, 'gas': 210000})
                    signed_txn = web3.eth.account.signTransaction(transaction, privatekey)
                    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                    web3.toHex(txn_hash)


                    time.sleep(10)
                    token_balanceAgain = contract.functions.balanceOf(account).call()
                    token_balanceAgainUser = contract.functions.balanceOf(address).call()
                    finalTokenUserBalance = web3.fromWei(token_balanceAgainUser,'ether')

                    finalTokenUserBalance = str(finalTokenUserBalance)
                    length = len(finalTokenUserBalance)
                    if length > 15:
                        finalTokenUserBalance = finalTokenUserBalance[:-10]
                        enough = "Exchange Successful!"

                    if web3.fromWei(token_balanceBefore,'ether') != web3.fromWei(token_balanceAgain,'ether'):
                        result2 = "Exchange of Medi-Coin successful"

                    else:
                        result2 = "Exchange of Medi-Coin unsuccessful"

                else:
                    result = "Exchange of ETH unsuccessful"

            else:
                enough = "MAX exchange allowed .05ETH"
                finalTokenUserBalance = ""

    else:

        enough = ""
        finalTokenUserBalance = ""







    return finalTokenUserBalance,enough



def payPremium(amount,address,key):

    if len(address) == 42 and len(key) == 64:

        token_balanceBefore = contract.functions.balanceOf(address).call()

        #MetaMask wallet address
        account = "0xaF343844F24256fb2b882669C64087d6b377E821"


        token_balance = contract.functions.balanceOf(address).call()


        if int(token_balance) < int(amount):
            enough = "Insufficient Funds"


        else:

            allAmounts = []

            if amount == "6":
                amount2 = 6000000000000000000
                allAmounts.append(amount)
            elif amount == "12":
                amount2 = 6000000000000000000 * 2
                allAmounts.append(amount)
            elif amount == "18":
                amount2 = 6000000000000000000 * 3
                allAmounts.append(amount)
            elif amount == "30":
                amount2 = 6000000000000000000 * 5
                allAmounts.append(amount)


            if amount in allAmounts:



                nonce = web3.eth.getTransactionCount(address)
                transaction = contract.functions.transfer(account, amount2).buildTransaction(
                    {'nonce': nonce, 'chainId': 42, 'gas': 210000})
                signed_txn = web3.eth.account.signTransaction(transaction, key)
                txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                web3.toHex(txn_hash)


                time.sleep(8)
                token_balanceAgainUser = contract.functions.balanceOf(address).call()


                if token_balanceBefore > token_balanceAgainUser:
                    enough = "Payment Successful!"

                else:

                    enough = "Payment Unsuccessful!"




            else:
                enough = "Choose from the coverage options above"


    else:

        enough = "Enter valid credentials"



    return enough