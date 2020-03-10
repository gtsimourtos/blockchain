import hashlib
import time


class Block:

	def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
		self.index = index
		self.proof_no = proof_no
		self.prev_hash = prev_hash
		self.data = data
		self.timestamp = timestamp or time.time()

	@property
	def calculate_hash(self):
		block_of_string = "{}{}{}{}{}".format(self.index, self.proof_no,
		                                      self.prev_hash, self.data,
		                                      self.timestamp)

		return hashlib.sha256(block_of_string.encode()).hexdigest()

	def __repr__(self):
		return "{} - {} - {} - {} - {}".format(self.index, self.proof_no,
		                                       self.prev_hash, self.data,
		                                       self.timestamp)


class BlockChain:

	def __init__(self):
		self.chain = []
		self.current_data = []
		self.nodes = set()
		self.construct_genesis()

	def construct_genesis(self):
		self.construct_block(proof_no=0, prev_hash=0)

	def construct_block(self, proof_no, prev_hash):
		block = Block(
			index=len(self.chain),
			proof_no=proof_no,
			prev_hash=prev_hash,
			data=self.current_data)
		self.current_data = []

		self.chain.append(block)
		return block

	@staticmethod
	def check_validity(block, prev_block):
		if prev_block.index + 1 != block.index:
			return False

		elif prev_block.calculate_hash != block.prev_hash:
			return False

		elif not BlockChain.verifying_proof(block.proof_no,
		                                    prev_block.calculate_hash):
			return False

		elif block.timestamp <= prev_block.timestamp:
			return False
		guess = f'{block.proof_no}{prev_block.calculate_hash}'.encode()
		print('Transaction is valid.\nHash between block ( index ',prev_block.index,') and proof number of new block ( index ',block.index,') is: ',hashlib.sha256(guess).hexdigest())
		return True

	def new_data(self, sender, recipient, quantity):
		self.current_data.append({
			'sender': sender,
			'recipient': recipient,
			'quantity': quantity
		})
		return True

	@staticmethod
	def proof_of_work(last_proof):
		'''this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
		 f is the previous f'
		 f' is the new proof
		'''
		proof_no = 0
		while BlockChain.verifying_proof(proof_no, last_proof) is False:
			proof_no += 1

		return proof_no

	@staticmethod
	def verifying_proof(last_proof, proof):
		#verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?

		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	@property
	def latest_block(self):
		return self.chain[-1]

	def block_mining(self, details_miner):

		self.new_data(
			sender="0",  #it implies that this node has created a new block
			recipient=details_miner,
			quantity=
			1,  #creating a new block (or identifying the proof number) is awarded with 1
		)

		last_block = self.latest_block

		proof_no = self.proof_of_work(last_block.calculate_hash)

		last_hash = last_block.calculate_hash
		block = self.construct_block(proof_no, last_hash)

		return vars(block)

	def create_node(self, address):
		self.nodes.add(address)
		return True

	@staticmethod
	def obtain_block_object(block_data):
		#obtains block object from the block data

		return Block(
			block_data['index'],
			block_data['proof_no'],
			block_data['prev_hash'],
			block_data['data'],
			timestamp=block_data['timestamp'])


blockchain = BlockChain()
while(1):
	print('current chain is: ',blockchain.chain)

	last_block = blockchain.latest_block
	proof_no = blockchain.proof_of_work(last_block.calculate_hash)
	print('sender: ')
	str1 = str(input())
	print('recipient: ')
	str2 = str(input())
	print('quantity: ')
	qty = int(input())

	sum = 0
	for i in range(len(blockchain.chain),1,-1):
		if(str1 == '0'):
			continue
		temp = blockchain.chain[i-1]
		recip = str(temp.data).split()[3]
		recip = recip.replace("'", "")
		recip = recip.replace(",", "")
		amt = str(temp.data).split()[5]
		amt = amt.replace("}]","")
		if(str1 == recip):
			if(qty>sum):
				sum += int(amt)


	if qty>sum and str1 != '0':
		print('Transaction invalid!')
		continue

	blockchain.new_data(
		sender=str1,  #it implies that this node has created a new block
		recipient=str2,  #let's send Quincy some coins!
		quantity=qty,  #creating a new block (or identifying the proof number) is awarded with 1
	)

	last_hash = last_block.calculate_hash
	block = blockchain.construct_block(proof_no, last_hash)

	blockchain.check_validity(block,last_block)



	print('new block added')
