from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()
node_endpoint = os.environ.get('mainnet_node')
abi_token = os.environ.get('abi_token')

w3 = Web3(Web3.HTTPProvider(node_endpoint, request_kwargs={'timeout': 60}))


def check_balance(addr: str, contract=None, block_number=None) -> dict:  # single ver
    tmp_d = {}
    tmp_d['address'] = addr
    tmp_d['contract'] = contract

    if contract:
        contract_type = 'token'
        contract = Web3.to_checksum_address(contract)
        contract_abi = os.environ.get('abi_token')
    else:
        contract_type = 'coin'

    addr = Web3.to_checksum_address(addr)

    if contract_type == 'token':
        token_contract = w3.eth.contract(address=contract, abi=contract_abi)
        if block_number:
            balance = token_contract.functions.get_balance(addr).call(block_identifier=block_number)
        else:
            balance = token_contract.functions.get_balance(addr).call()
        balance_eth = balance / float(10**18)
    else:
        if block_number:
            balance = w3.eth.get_balance(addr, block_identifier=block_number)
        else:
            balance = w3.eth.get_balance(addr)
        balance_eth = balance / float(10**18)

    tmp_d['balance'] = balance
    tmp_d['balance_eth'] = balance_eth

    return tmp_d


# need netid, contractaddress, blocknumber, account info
def check_balance_v2(info_list: list) -> dict:
    for num, i in enumerate(info_list):
        if i['netid'] == '3.0':
            node_endpoint = os.environ.get('mainnet_node')
        elif i['netid'] == 'Play':
            node_endpoint = os.environ.get('play_node')
        elif i['netid'] == 'Tornado':
            node_endpoint = os.environ.get('tornado_node')
        elif i['netid'] == 'Klaytn':
            node_endpoint = os.environ.get('klaytn_node')

        w3 = Web3(Web3.HTTPProvider(node_endpoint,
                  request_kwargs={'timeout': 60}))

        try:
            account = Web3.to_checksum_address(i['account'])
            if i['contractaddress'] == '0x0000000000000000000000000000000000000000':
                temp = {}
                balance = w3.eth.get_balance(account, block_identifier=i['blocknumber'])
                balance_eth = float(balance / 1.e018)
                print('coin balance is', balance_eth)
            else:
                token_final = w3.eth.contract(address=Web3.to_checksum_address(
                    i['contractaddress']), abi=abi_token)
                balance = token_final.functions.balanceOf(account).call(block_identifier=i['blocknumber'])
                balance_eth = float(balance / 1.e018)

                print('token balance is', balance_eth)

            i['balance'] = f'{balance}'
            i['balance_eth'] = balance_eth
        except:
            info_list.remove(i)
