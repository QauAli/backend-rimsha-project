import hashlib

password = "Rimsha"

hashed_string = hashlib.sha256(password.encode('utf-8')).hexdigest()
print(hashed_string)
