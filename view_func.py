from web3 import Web3
from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()
node_endpoint = os.environ.get('mainnet_node')
abi_value = os.environ.get('abi_value')

web3 = Web3(Web3.HTTPProvider(node_endpoint, request_kwargs={'timeout': 60}))


contract = ''
contract_addr = web3.to_checksum_address(contract)
contract_addr = web3.eth.contract(address=contract_addr, abi=abi_value)
print(contract_addr.all_functions())

contract_addr.functions.base().call()