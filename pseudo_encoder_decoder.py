def decimal_to_binary(n):
    bi_num = bin(abs(n)).replace("0b", "")
    bi_len = len(bi_num)
    bi_app = "0" * 18
    bi_app = bi_app[0:18 - bi_len]
    return bi_app + bi_num


def pseudo_decoder(pse_val, rn, pos=False):
    if pse_val == '///':
        return 'NaN'
    else:
        bi_val = ''
        num_val = [0, 0, 0]
        pse_len = len(pse_val)
        if pse_len == 1:
            pse_val = "@@" + pse_val
        elif pse_len == 2:
            pse_val = "@" + pse_val
        for num in range(3):
            num_val[num] = ord(pse_val[num])
            if num_val[num] != 63:
                num_val[num] = num_val[num] - 64
            temp = decimal_to_binary(num_val[num])
            bi_val += temp[12:]
        bi_val = int(bi_val, 2)
        if pse_len == 1 and bi_val > 31 and pos == False:
            bi_val = bi_val - 64
        if pse_len == 2 and bi_val > 2047 and pos == False:
            bi_val = bi_val - 4096
        if pse_len == 3 and bi_val > 131071:
            bi_val = bi_val - 262144
        return bi_val * 10 ** -rn


def pseudo_encoder(int_val, byt):
    """
    Pseudobinary encoder function converts binary number from -131072 to 131071
    :param int_val: Decimal number
    :param byt: Number of bytes (1,2 or 3)
    :return: Pseudobinary b format
    """
    int_val = int(str(int_val).replace(".", ""))
    iv = 0
    if int_val < 0:
        if byt == 1 and int_val < -31:
            return "`"
        if byt == 2 and int_val < -2047:
            return "`@"
        if byt == 3 and int_val < -131071:
            return "`@@"
        # Call decimal_to_binary Function
        bi_num = decimal_to_binary(int_val)
        bi_str = ""
        for bit in bi_num:
            if bit == "1":
                bi_str += "0"
            else:
                bi_str += "1"
        iv = int(bi_str, 2) + 1
    if int_val >= 0:
        if byt == 1 and int_val > 30:
            return "_"
        if byt == 2 and int_val > 2046:
            return "_?"
        if byt == 3 and int_val > 131070:
            return "_??"
        iv = int_val
    bi_array = [iv >> 12, (iv >> 6) & 63, iv & 63]
    for i in range(3):
        if bi_array[i] != int(63):
            bi_array[i] += 64
    if byt == 1:
        return chr(bi_array[2])
    elif byt == 2:
        return chr(bi_array[1]) + chr(bi_array[2])
    elif byt == 3:
        return chr(bi_array[0]) + chr(bi_array[1]) + chr(bi_array[2])

b = "P99999991B\P@@@@^0VeJ8AJv@gC#@yF1@}AA^BCEC@>???8@?f@|I#???3@SCb@a4Bz5C`5CJ6mO-7@g[<BW TJbLCaIKFU]GEiVp"
a=[]
c=[]
a.append(b[1:9])
c.append("station name")
b= b[9:]
a.append(b[:3])
c.append("sns")
b= b[3:]
a.append(b[:2])
c.append("dat")
b= b[2:]
a.append(b[:2])
c.append("sys num")
b= b[2:]
a.append(b[:1])
c.append("xtime off")
b= b[1:]
while True:
    check = b.find("0")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 3])
        a.append(b[check + 3: check + 4])
        c.append("sutron")
        c.append("hour")
        b = b.replace("0", "", 1)



while True:
    check = b.find("8")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 4])
        a.append(b[check + 4: check + 6])
        a.append(b[check + 6: check + 7])
        c.append("mwwl")
        c.append("mwwlstd")
        c.append("mwwlout")
        b = b.replace("8", "", 1)
        
while True:
    check = b.find("2")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 4])
        a.append(b[check + 4: check + 6])
        a.append(b[check + 6: check + 7])
        c.append("bwl")
        c.append("bwlstd")
        c.append("bwlout")
        b = b.replace("2", "", 1)

while True:
    check = b.find("#")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 4])
        c.append("red mwwl")
        b = b.replace("#", "", 1)

while True:
    check = b.find(">")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 4])
        c.append("red aqt")
        b = b.replace(">", "", 1)

while True:
    check = b.find("1")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 4])
        a.append(b[check + 4: check + 6])
        a.append(b[check + 6: check + 7])
        a.append(b[check + 7: check + 9])
        a.append(b[check + 9: check + 11])
        c.append("aqt")
        c.append("aqtstd")
        c.append("aqtout")
        c.append("aqt1")
        c.append("aqt2")
        b = b.replace("1", "", 1)
     
        
while True:
    check = b.find("3")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 3])
        a.append(b[check + 3: check + 5])
        a.append(b[check + 5: check + 7])
        c.append("ws")
        c.append("wd")
        c.append("wg")
        b = b.replace("3", "", 1)
while True:
    check = b.find("4")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 3])
        c.append("air temp")
        b = b.replace("4", "", 1)
        
while True:
    check = b.find("5")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 3])
        c.append("water temp")
        b = b.replace("5", "", 1)


while True:
    check = b.find("6")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 3])
        c.append("baro temp")
        b = b.replace("6", "", 1)


while True:
    check = b.find("-7")
    if check == -1:
        break
    else:
        a.append(b[check + 2: check + 5])
        c.append("conductivity")
        b = b.replace("-7", "", 1)

while True:
    check = b.find("<")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 3])
        c.append("battery")
        b = b.replace("<", "", 1)

while True:
    check = b.find("T")
    if check == -1:
        break
    else:
        a.append(b[check + 1: check + 2])
        a.append(b[check + 2: check + 3])
        a.append(b[check + 3: check + 4])
        a.append(b[check + 4: check + 6])
        a.append(b[check + 6: check + 8])
        a.append(b[check + 8: check + 10])
        a.append(b[check + 10: check + 12])
        a.append(b[check + 12: check + 14])
        a.append(b[check + 14: check + 16])
        c.append("tsunami hour")
        c.append("tsunami minute")
        c.append("offset")
        c.append("U1")
        c.append("U1")
        c.append("U1")
        c.append("U1")
        c.append("U1")
        c.append("U1")
        
        b = b.replace("T", "", 1)
for i in range(len(a)):
    print(c[i], pseudo_decoder(a[i], 0, True))
