import hashlib
import requests
import json
import sys


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """
    # return proof
    block_string = json.dumps(block, sort_keys=True).encode()

    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof


def valid_proof(block_string, proof):
        # return True or False
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    # TODO: change back to 6 zeros
    return guess_hash[:3] == "000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0

    # Run forever until interrupted
    while True:
        # : Get the last proof from the server and look for a new one
        req = requests.get(url=node + "/last_block")
        data = req.json()

        last_block = data.get('last_block')
        # : When found, POST it to the server {"proof": new_proof}
        print(f"Last Block: {last_block}")
        next_proof = proof_of_work(last_block)
        print(f"found a proof: {next_proof}")

        # : We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        post_data = {
            "proof": next_proof
        }

        req = requests.post(url=node + "/mine", data=post_data)
        data = req.json()

        # : If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data.get('message') == "New Block Forged":
            coins_mined += 1
            print(f"Mined Coins: {str(coins_mined)}")
        else:
            print(data.get('message'))
