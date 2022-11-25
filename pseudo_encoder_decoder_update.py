def decimal_to_binary(n, byt):
    byt *= 6
    bi_num = bin(abs(n)).replace("0b", "")
    bi_len = len(bi_num)
    bi_app = "0" * byt
    bi_app = bi_app[0:byt - bi_len]
    return bi_app + bi_num


def pseudo_encoder(int_val, byt, pos=True):
    """
    Pseudobinary encoder function converts positive decimal number
    to pseudobinary. Length is determined by user.
    :param int_val: Decimal number
    :param byt: Number of bytes
    :param pos: Signed or unsigned
    :return: Pseudobinary b format
    """
    int_val = int(str(int_val).replace(".", ""))
    if int_val >= 0:
        if pos:
            int_val = min(int_val, 2 ** (6 * byt) - 1)
        if not pos:
            int_val = min(int_val, 2 ** (6 * byt) // 2 - 1)
    else:
        if pos:
            int_val = 0
        int_val = max(int_val, -2 ** (6 * byt) // 2)
        byt_six = byt * 6
        bi_num = bin(abs(int_val)).replace("0b", "")
        bi_len = len(bi_num)
        bi_app = "0" * byt_six
        bi_num = bi_app[0:byt_six - bi_len] + bi_num
        bi_str = ""
        for bit in bi_num:
            if bit == "1":
                bi_str += "0"
            else:
                bi_str += "1"
        int_val = int(bi_str, 2) + 1
    raw_msg = ""
    for i in range((byt - 1) * 6, -6, -6):
        temp = (int_val >> i) & 63
        if temp != 63:
            temp += 64
        raw_msg += chr(temp)
    return raw_msg


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
            temp = decimal_to_binary(num_val[num], 3)
            bi_val += temp[12:]
        bi_val = int(bi_val, 2)
        if pse_len == 1 and bi_val > 31 and pos == False:
            bi_val = bi_val - 64
        if pse_len == 2 and bi_val > 2047 and pos == False:
            bi_val = bi_val - 4096
        if pse_len == 3 and bi_val > 131071:
            bi_val = bi_val - 262144
        return bi_val * 10 ** -rn


for j in range(0, 50000000, 1):
    enc = pseudo_encoder(j, 7, True)
    dec = pseudo_decoder(enc, 0, True)
    print(j, enc, dec)
