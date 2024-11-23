import hashlib
from datetime import datetime
from typing import List, Optional
import json

class Block:
    """A class representing a single block in the blockchain."""
    
    def __init__(self, index: int, previous_hash: str, timestamp: str, data: str, hash: str):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    @staticmethod
    def calculate_hash(index: int, previous_hash: str, timestamp: str, data: str) -> str:
        """Calculate the SHA-256 hash of a block."""
        value = f"{index}{previous_hash}{timestamp}{data}"
        return hashlib.sha256(value.encode()).hexdigest()

    def __repr__(self) -> str:
        return (f"Block(Index: {self.index}, Previous Hash: {self.previous_hash}, "
                f"Timestamp: {self.timestamp}, Data: {self.data}, Hash: {self.hash})")

class Blockchain:
    """A class representing the blockchain."""
    
    GENESIS_DATA = "Genesis Block"

    def __init__(self):
        """Initialize the blockchain with the genesis block."""
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        """Create the genesis block and return it."""
        timestamp = datetime.utcnow().isoformat()
        hash = Block.calculate_hash(0, "0", timestamp, self.GENESIS_DATA)
        return Block(0, "0", timestamp, self.GENESIS_DATA, hash)

    def create_new_block(self, data: str) -> Block:
        """Create a new block with the given data and add it to the chain."""
        previous_block = self.get_latest_block()
        index = previous_block.index + 1
        timestamp = datetime.utcnow().isoformat()
        previous_hash = previous_block.hash
        hash = Block.calculate_hash(index, previous_hash, timestamp, data)
        new_block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(new_block)
        return new_block

    def get_latest_block(self) -> Block:
        """Return the latest block in the blockchain."""
        return self.chain[-1]

    def validate_chain(self) -> bool:
        """Validate the entire blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Validate the hash of the current block
            if current_block.hash != Block.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                print(f"Invalid hash at block {current_block.index}")
                return False
            
            # Validate the previous hash of the current block
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {current_block.index}")
                return False
        
        return True

    def get_chain(self) -> List[Block]:
        """Return the entire blockchain."""
        return self.chain

    def get_chain_length(self) -> int:
        """Return the length of the blockchain."""
        return len(self.chain)

    def get_block_by_index(self, index: int) -> Optional[Block]:
        """Retrieve a block by its index."""
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def to_json(self) -> str:
        """Serialize the blockchain to JSON format."""
        return json.dumps([block.__dict__ for block in self.chain], indent=4)

# Using the Blockchain class
if __name__ == "__main__":
    blockchain = Blockchain()

    # Adding new blocks
    blockchain.create_new_block("Block 1 Data")
    blockchain.create_new_block("Block 2 Data")

    # Displaying the blockchain
    for block in blockchain.get_chain():
        print(block)

    # Validating the blockchain
    is_valid = blockchain.validate_chain()
    print("Is the blockchain valid?", is_valid)

    # Serialize blockchain to JSON
    blockchain_json = blockchain.to_json()
    print("Blockchain JSON:")
    print(blockchain_json)