def load_credentials(file_path):
     creds={}
     with open(file_path, "r") as f:
          for line in f:
               key, value = line.strip().split("=",1)
               creds[key] = value
     return creds

print(load_credentials("reddit_credentials.txt"))