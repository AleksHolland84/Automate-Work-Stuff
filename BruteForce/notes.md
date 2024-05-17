# Teach How to Brute Force a Password

##To encrypt
`openssl enc -aes-256-ctr -pbkdf2 -e -a -in plain.txt -out encrypted.txt`


##To decrypt
`openssl enc -aes-256-ctr -pbkdf2 -d -a -in encrypted.txt -out decrypted.txt`


##Get hash for password entered when encrypted:
`echo -n "<the entered password>" | sha256sum`

Or use the script to encrypt the text file and save the hash of the entered password 
