import base64
#with open('path/sample.pdf', 'rb') as f:
#    blob = base64.b64encode(f.read())
#text_file = open('test_blob.txt', "rb")
#text_file.write("test")
#text_file.close()
with open('test_blob.txt', 'r') as f:
    print(f.read())
    blob=f.read()
blob = base64.b64decode(blob)
text_file = open('result.pdf','wb')
text_file.write(blob)
text_file.close()