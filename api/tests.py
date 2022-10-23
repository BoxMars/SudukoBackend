import jwt
import time

salt = "asgfdgerher"
exp = time.time() + 1
payload = {
  "name": "dawsonenjoy",
  "exp": exp
}

token = jwt.encode(payload=payload, key=salt, algorithm='HS256')

print(token)
time.sleep(2)

info = jwt.decode(token, salt, algorithms=['HS256'])
print(info)
