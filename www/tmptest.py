x=int(3989)
y=int(5145)

# 输出x和y的高8位和低8位,16进制,byte格式

print(f"x的高8位:{x>>8},低8位:{x&0xff},16进制:{hex(x)},byte格式:{x.to_bytes(2, 'big')}")
print(f"y的高8位:{y>>8},低8位:{y&0xff},16进制:{hex(y)},byte格式:{y.to_bytes(2, 'big')}")