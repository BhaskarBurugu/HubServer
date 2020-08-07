from bitstring import BitStream, BitArray
a = BitArray(bytes=b'\xf0\x01\x02\xff', length=28, offset=1)
print(a.bin[0])

mem = b'\xfe\x02\xff'
x = [[int(digit) for digit in "{0:08b}".format(byte)] for byte in mem]
print(x[0][-1])