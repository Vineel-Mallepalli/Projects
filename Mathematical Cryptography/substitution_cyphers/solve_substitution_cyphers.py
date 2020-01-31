letters = [chr(i) for i in range(65, 91)]
values = [i for i in range(26)]
get_val = dict(zip(letters, values))
get_char = dict(zip(values, letters))


def substitute_known_letters(string, mapping):
    chars = list(string)
    new_chars = list(chars)
    for idx in range(len(chars)):
        if chars[idx] in mapping:
            new_chars[idx] = mapping[chars[idx]]
        else:
            new_chars[idx] = "_"
    return "".join(new_chars)


def shift(chars, num_shift):
    new_chars = list(chars)
    for i in range(len(chars)):
        new_chars[i] = get_char[(get_val[chars[i]] + num_shift) % 26]
    return new_chars


def break_into_blocks(string, key_len):
    chars = list(string)
    d = {}
    for i in range(len(chars)):
        if i % key_len in d:
            old_val = list(d.get(i % key_len))
            old_val.append(chars[i])
            d[i % key_len] = old_val
        else:
            d[i % key_len] = [chars[i]]
    return d


def relative_shift(d, shifts):
    # shift all relative to j by -k letters
    for i, j, k in shifts:
        d[i - 1] = shift(d[i - 1], -k)
    return d


def zip_up(d):
    k = len(d.keys())
    i = 0
    new_chars = []
    while i < len(d[0]):
        for val in range(k):
            if i < len(d[val]):
                new_chars.append(d[val][i])
        i += 1
    return new_chars


string0 = "togmg gbymk kcqiv dmlxk kbyif vcuek cuuis vvxqs pwwej koqgg phumt whlsf yovww knhhm rcqfq vvhkw psued ugrsf " \
          "ctwij khvfa thkef fwptj ggviv cgdra pgwvm osqxg hkdvt whuev kcwyj psgsn gfwsl jsfse ooqhw tofsh aciin gfbif " \
          "gabgj adwsy topml ecqzw asgvs fwrqs fsfvq rhdrs nmvmk cbhrv kblxk gzi"
string0 = string0.upper().replace(" ", "")
shifts = [(4, 5, 12), (3, 5, 11), (2, 5, 22), (1, 5, 10)]
# print(string0)
# print(break_into_blocks(string0, 5))
# print(relative_shift(break_into_blocks(string0, 5), shifts))
zipped_adjusted = zip_up(relative_shift(break_into_blocks(string0, 5), shifts))
for i in range(26):
    ans = shift(zipped_adjusted, i)
    print(ans if ans[0] == "R" else 0)

string1 = "JNRZR BNIGI BJRGZ IZLQR OTDNJ GRIHT USDKR ZZWLG OIBTM NRGJN" \
          " IJTZJ LZISJ NRSBL QVRSI ORIQT QDEKJ JNRQW GLOFN IJTZX QLFQL" \
          " WBIMJ ITQXT HHTBL KUHQL JZKMM LZRNT OBIMI EURLW BLQZJ GKBJT" \
          " QDIQS LWJNR OLGRI EZJGK ZRBGS MJLDG IMNZT OIHRK MOSOT QHIJL" \
          " QBRJN IJJNT ZFIZL WIZTO MURZM RBTRZ ZKBNN LFRVR GIZFL KUHIM" \
          " MRIGJ LJNRB GKHRT QJRUU RBJLW JNRZI TULGI EZLUK JRUST QZLUK EURFT JNLKJ JNRXR S "
map1 = {"J": "T", "N": "H", "R": "E", "I": "A", "L": "O", "T": "I", "Z": "S", "S": "Y", "F": "W", "K": "U", "X": "K",
        "Q": "N", "B": "C", "G": "R", "V": "V", "O": "M", "D": "G", "W": "F", "M": "P", "E": "B", "U": "L", "H": "D"}

# print(substitute_known_letters(string1.replace(" ", ""), map1))


string2 = "GSZES GNUBE SZGUG SNKGX CSUUE QNZOQ EOVJN VXKNG XGAHS AWSZZ BOVUE SIXCQ NQESX NGEUG AHZQA" \
          "QHNSP CIPQA OIDLV JXGAK CGJCG SASUB FVQAV CIAWN VWOVP SNSXV JGPCV NODIX GJQAE VOOXC SXXCG" \
          "OGOVA XGNVU BAVKX QZVQD LVJXQ EXCQO VKCQG AMVAX VWXCG OOBOX VZCSO SPPSN VAXUB DVVAX QJQAJ" \
          "VSUXC SXXCV OVJCS NSJXV NOJQA MVBSZ VOOSH VSAWX QHGMV GWVSX CSXXC VBSNV ZVNVN SAWQZ ORVXJ CVOQE JCGUW NVA"
map2 = {"V": "E", "S": "A", "X": "T", "C": "H", "N": "R", "J": "C", "O": "S", "P": "P", "G": "I", "A": "N", "K": "W",
        "H": "G", "B": "Y", "Z": "M", "U": "L", "E": "F", "Q": "O", "W": "D", "I": "U", "D": "B", "L": "J", "F": "Z",
        "M": "V", "R": "K"}

# print(substitute_known_letters(string2.replace(" ", ""), map2))
