import json;

# File handling
f = open("secret.json")
#data = f.read()
secrets = json.load(f)

print(secrets["token"])