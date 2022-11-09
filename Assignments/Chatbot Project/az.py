import bs4 as bs
import urllib.request
#Open the cat web data page
data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Cyberpunk').read()
print(data)