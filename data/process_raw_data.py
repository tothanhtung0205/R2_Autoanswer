import pandas as pd
from io import open
from bs4 import BeautifulSoup

def replace_space(text):
    text = " ".join(text.split())
    return text


def parse_html(file_name_csv):
    dataset = []
    df = pd.read_csv(file_name_csv,encoding="utf-8")
    a = df.values
    for row in a:
        col2 = BeautifulSoup(row[1]).text
        col2 = replace_space(col2)
        col3 = u""+str(row[0])
        #col3 = replace_space(col3)
        dataset.append([col2,col3])
    return dataset


def check_similar2(elm,data):
    ques = elm[0]
    for elm2 in data:
        ques2 = elm2[0]
        if ques2 == ques:
            print("duplicate sentence ")
            return True
    return False


def remove_duplicate(data):
    direct_list = []
    for elm in data:
        if check_similar2(elm,direct_list):
            continue
        else:
            direct_list.append(elm)
    return direct_list


def write_to_file(direct_list,file_name):
    with open(file_name,"w",encoding="utf-8") as f_w:
        for i,line in enumerate(direct_list):
            line = u"--->".join(line)
            if(len(line) > 1000):
                continue
            f_w.write(line)
            f_w.write(u"\n")
            print("Write sen " + str(i))
        f_w.close()

def process_data(csv_file,data_file):
    data = parse_html(csv_file)
    nomed_data = remove_duplicate(data)
    write_to_file(nomed_data,data_file)

if __name__ == "__main__":
    process_data("H2472_DATA/phat_trien_ky_nang.csv","phat_trien_ky_nang/raw.txt")