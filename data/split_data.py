from io import open

aaa = []
with open("phat_trien_ky_nang/raw.txt","r",encoding="utf-8") as f:
    for line in f:
       aaa.append(line)


with open("phat_trien_ky_nang/test.txt","w",encoding="utf-8") as f_w:
    for sen in aaa[:50]:
        f_w.write(sen)
    f_w.close()


with open("phat_trien_ky_nang/train.txt","w",encoding="utf-8") as f_w:
    for sen in aaa[50:]:
        f_w.write(sen)
    f_w.close()