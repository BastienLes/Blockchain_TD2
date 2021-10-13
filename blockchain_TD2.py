import sys
import random
import hashlib
import hmac

from bip39 import bip39

seed = ""
pvmk = ""
chain_code = ""
pbmk = ""

def interpreter(l):
	data = l.split("\n")[0].split(" ")
	if (data[0] == "help" or data[0] == "0"):
		help()
	elif (data[0] == "create_seed" or data[0] == "1"):
		create_seed_128()
	elif (data[0] == "import_seed" or data[0] == "2"):
		import_seed(data[1:])
	elif (data[0] == "gen_pvmk_chain" or data[0] == "3"):
		generate_pvmk_chain()
	elif (data[0] == "gen_pbmk" or data[0] == "4"):
		generate_pbmk()
	else:
		print("Could not understant, try \"help\" to find what functions are available")


def help():
	print("What you can type : ")
	print(" - [0] : \"help\" display this message again")
	print(" - [1] : \"create_seed\" to create a 128bits seed")
	print(" - [2] : \"import_seed word1 word2 ...\" to find seed from your mnemonic phrase")
	print(" - [3] : \"gen_pvmk_chain\" to generate private master key and chain code")
	print(" - [4] : \"gen_pbmk\" to generate public master key")

def create_seed_128():
	global seed 

	entropy = random.getrandbits(128)
	hash_seed = hashlib.sha256(str(entropy).encode())
	checksum = hash_seed.digest()[0] >> 4

	seed = int(entropy << 4) + int(checksum)

	print("Your seed (hexa) : ", end="")
	print(hex(seed))

	seed = bin(seed)

	print("Your seed (binary) : ", end="")
	print(seed)

	seed = seed[2:].zfill(132) # on retire le 0b et on rajoute les 0 devant qui pourrait avoir été omis

	split_seed = [seed[i:i+11] for i in range(0, len(seed), 11)]
	print("Your seed (binary words) : ", end="")
	print(split_seed)

	split_seed_int = [int(split_seed[i], 2) for i in range(len(split_seed))]
	print("Your seed (binary words as integers) : ", end="")
	print(split_seed_int)


	split_seed_word = [bip39.INDEX_TO_WORD_TABLE[split_seed_int[i]] for i in range(len(split_seed_int))]
	print("Your seed (as mnemonic phrase) : ", end="")
	print(*split_seed_word, sep=" ")

	# save seed as bytes
	seed = ((int(entropy)).to_bytes(16, sys.byteorder))


def import_seed(phrase):
	global seed 

	print("Your mnemonic phrase : ", end="")
	print(*phrase, sep=" ")


	split_seed_int = [bip39.INDEX_TO_WORD_TABLE.index(phrase[i]) for i in range(len(phrase))]
	print("Your seed (mnemonic hprase as integers) : ", end="")
	print(split_seed_int)

	split_seed = [str(bin(split_seed_int[i])[2:]).zfill(11) for i in range(len(split_seed_int))]
	print("Your seed (binary words) : ", end="")
	print(split_seed)

	seed = "".join(split_seed)

	entropy = seed[:128]
	hash_seed = hashlib.sha256(str(int(entropy, 2)).encode())
	calculated_checksum = hash_seed.digest()[0] >> 4
	given_checksum = int(seed[128:], 2)

	if(given_checksum == calculated_checksum):
		print("Seed successfully imported (checksum valid)")
	else:
		print("Error, seed could not be imported (checksum not valid)")
		return

	seed = int(seed, 2)
	print("Your seed (binary) : ", end="")
	print(bin(seed))

	print("Your seed (hexa) : ", end="")
	print(hex(seed))

	# save seed as bytes
	seed = ((int(entropy, 2)).to_bytes(16, sys.byteorder))

def generate_pvmk_chain():
	global seed, pvmk, chain_code

	print("Generating private master key and chain code from seed : \n", seed)
	h = hmac.new(seed, None, hashlib.sha512)

	# split result into private master key and chain code
	pvmk = int(h.hexdigest()[:64], 16)
	chain_code = int(h.hexdigest()[64:], 16)
	print("Your private key (hexa) : ", hex(pvmk))
	print("Your chain code (hexa) : ", hex(chain_code))

	# converting into bytes
	pvmk = (pvmk).to_bytes(32, sys.byteorder)
	chain_code = (chain_code).to_bytes(32, sys.byteorder)

def generate_pbmk():
	return


help()
for l in sys.stdin:
	if 'Exit' == l.rstrip():
		break
	#print(f'\nreceived : {l}')
	interpreter(l)

Int128
print("Done")