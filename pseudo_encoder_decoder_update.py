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
        bi_num = "0" * (byt_six - len(bi_num)) + bi_num
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


def pseudo_decoder(pse_val, rn, pos=True):
    if pse_val == '///':
        return 'NaN'
    else:
        bi_val = ""
        pse_len = len(pse_val)
        for num in range(pse_len):
            temp = ord(pse_val[num])
            if temp != 63:
                temp -= 64
            bi_num = bin(abs(temp)).replace("0b", "")
            bi_val += "0" * (6 - len(bi_num)) + bi_num
        bi_val = int(bi_val, 2)
        if not pos and bi_val > 2 ** (6 * pse_len) // 2 - 1:
            bi_val -= 2 ** 6 * pse_len // 2 * 2
        return bi_val * 10 ** -rn


j = 123
enc = pseudo_encoder(j, 6, False)
dec = pseudo_decoder(enc, 0, False)
print(j, enc, dec)
