#code is from geeks for geeks
import bcrypt
 
password = b'app_user'
 
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)

print("Salt :")
print(salt)
 
print("Hashed")
print(hashed)