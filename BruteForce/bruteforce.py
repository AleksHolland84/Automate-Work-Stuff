from hashlib import sha256
import sys

hash = input("Past in hash:")


with open("passwd.list", "r", encoding="utf-8") as f:
	passwd = f.readlines()

	try:
		for pw in passwd:
			pw_hash = (sha256(pw.strip().encode('utf-8')).hexdigest())
			if pw_hash != hash:
				continue
			else:
				print(f"password found for hash: {hash}")
				print(f'{pw_hash}:{pw}')
				sys.exit()
		print("Password not found")
	except SystemExit as exit:
		print("Program Exited")
	except:
		print("error")
