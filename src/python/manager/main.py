import requests

def get_data():
  url = 'http://g4bls_worker_1:80/api/start-worker'
  response = requests.get(url)
  return response.json()

if __name__ == '__main__':
  print(get_data())
