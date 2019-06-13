l=['List of devices attached\n', '06157df6e839ee14\tunauthorized\n', '2892d4ea\tunauthorized\n', '127.0.0.1:62001\tdevice\n', '\n']
print(l[1:])
infp=[]
for value in l[1:len(l)-1]:
    print(value.split('\t')[0])
    deviceid = infp.append(value.split('\t')[0])

print(infp)