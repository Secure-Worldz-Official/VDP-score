from bs4 import BeautifulSoup
from requests import get

req = get('https://example.com/')
main = BeautifulSoup(req.text,'html.parser')
for i in main.find_all('div'):
    print(i)