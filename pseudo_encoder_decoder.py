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
        print("1", bi_val)
        bi_val = int(bi_val, 2)
        print("2", bi_val)
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


print(pseudo_encoder(5, 2))
print(pseudo_decoder("@E", 0))