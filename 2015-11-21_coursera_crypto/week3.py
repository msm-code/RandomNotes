import hashlib

data = open('file.dat', 'rb').read()
blocks = [data[1024*i:1024*(i+1)] for i in range((len(data)+1023)/1024)]
hash = ''
for block in blocks[::-1]:
    hash = hashlib.sha256(block + hash).digest()
print hash.encode('hex')
