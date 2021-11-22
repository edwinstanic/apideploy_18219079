from fastapi import FastAPI, HTTPException, Depends
from Auth.Auth_handler import signJWT, get_password_hash, verify_password
from Auth.Auth_bearer import JWTBearer
import json

with open("accdb.json", "r") as readUser:
    daftaruser = json.load(readUser)

app = FastAPI()

@app.post("/register")
async def register(username: str, email: str, password: str):
    for listuser in daftaruser['user database']:
        if listuser['username'] == username:
            return ({'Message' : "Username tidak bisa digunakan"})
        else :
            hashedpw = get_password_hash(password)
            new_user = {'username': username, 'email': email, 'password': hashedpw}
            daftaruser['user database'].append(new_user)
            
            with open("accdb.json", "w") as writeUser:
                json.dump(daftaruser, writeUser, indent = 4)
            
            writeUser.close()
            return ({'Message' : "Pendaftaran berhasil"})
 
@app.post("/login")
async def login(email: str, password: str):
    for listuser in daftaruser['user database']:
        if listuser['email'] == email:
            if verify_password(password, listuser['password']):
                return signJWT(email)
            else:
                return ({'Message' : "Password salah"})
    return ({'Message' : "Email tidak ada"})