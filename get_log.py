from decimal import Decimal
from builtins import min as py_min
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()
min_block = 105565669
max_block = 108157636
node_endpoint = os.environ.get('mainnet_node')
contract_add = os.environ.get('contract_address')
contract_name = os.environ.get('contract_name')

result_dict_list = [{'start_block': min_block,
                    'end_block': max_block,
                     'contract': contract_add,
                     'contractname': contract_name}]
abi = os.environ.get('abi_value')


def get_signature_text(abi_value, type='text'):
    # abi_value = os.environ.get('abi_value')   #list type
    inputs = abi_value[0]['inputs']
    event_name = abi_value[0]['name']
    argument_types = [param["type"] for param in abi_value[0]['inputs']]
    argument_types_str = ",".join(argument_types)

    signature_text = f"{event_name}({argument_types_str})"
    signature_hex = web3.to_hex(web3.keccak(text=signature_text))

    if type == 'text':
        return signature_text
    elif type == 'hex':
        return signature_hex


def get_event_log(w3, abi: list, contract_address: str, token_contract: str, start_block: int, end_block: int):
    contract_address = w3.to_checksum_address(contract_address)
    contract = w3.eth.contract(address=contract_address, abi=abi)
    # event_signature = w3.keccak(
    #     text="EventName(type1,type2,type3)").hex()
    event_signature = get_signature_text(abi, 'hex')
    formatted_token_address = '0x' + token_contract[2:].rjust(64, '0')

    logs = w3.eth.get_logs({
        "fromBlock": start_block,
        "toBlock": end_block,
        "address": contract_address,
        "topics": [event_signature, None, None]
    })
    return logs


if __name__ == "__main__":
    chunk_size = 30000
    total = []
    for data in result_dict_list:
        start_block = data['start_block']
        end_block = data['end_block']
        # wallet = data['account']
        contract_add = data['contract']
        contract_name = data['contractname']

        web3 = Web3(Web3.HTTPProvider(node_endpoint,
                    request_kwargs={'timeout': None}))

        if isinstance(start_block, int):
            for block in range(start_block, end_block, chunk_size):
                current_end_block = py_min((block+chunk_size-1), end_block)
                print(block, current_end_block)

                logs = get_event_log(
                    web3, abi, contract_add, block, current_end_block)
                for log in logs:
                    contract = web3.eth.contract(
                        web3.to_checksum_address(contract_add), abi=abi)
                    temp = {}
                    doc = {}
                    doc['contract'] = contract_name
                    temp['logs'] = [log]
                    decoded_logs = contract.events['IncomeAdded'](
                    ).process_receipt(temp)
                    doc['amount'] = str(decoded_logs[0]['args']['amount'])
                    doc['contractaddress'] = decoded_logs[0]['address'].lower()
                    doc['token'] = decoded_logs[0]['args']['token'].lower()

                    total.append(doc)
