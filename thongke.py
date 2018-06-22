# -*- coding=utf-8 -*-
# author = "tungtt"
from io import open
from tfidf_model import TfidfModel
SPLIT_LENGTH = 100

TRAIN_PATH = 'data/train.txt'

def tfidf_test(tfidf_model,test_file,result_file):
    print(" Test  on " + test_file)
    test_set = tfidf_model.get_test_data(test_file)
    count1 = 0
    count2 = 0
    count3 = 0
    with open(result_file,"w",encoding="utf-8") as f:
        for test_sen in test_set:

            sim =tfidf_model.get_similar_sen(test_sen,1)
            sim_mi = float(sim[0][2])
            sim_sen = sim[0]

            sim = u"\n".join([sim_sen[0],sim_sen[1],sim_sen[2]])
            prced_test_sen = tfidf_model.pre_process(test_sen)
            #todo
            if( sim_mi >= 0.4):
                count1 += 1
            if sim_mi >= 0.5:
                count2 += 1

            if(sim_mi >= 0.6):
                count3 +=1
                print(test_sen + u"\n" + sim + u'\n')

                f.write(test_sen + u"\n" + prced_test_sen + u'\n')
                f.write(u"-" * SPLIT_LENGTH + "\n")
                f.write(sim)
                f.write(u"\n" + u"_" * SPLIT_LENGTH + u"\n")

        f.close()
        print("Number of sen > 0.4 : %d " % count1)
        print("Number of sen > 0.5 : %d " % count2)
        print("Number of sen > 0.6 : %d " % count3)



if __name__ == "__main__":
    tfidf = TfidfModel("data/phat_trien_ky_nang/train.txt","data/phat_trien_ky_nang//corpus_train.txt")
    tfidf_test(tfidf, "data/phat_trien_ky_nang/test.txt", "thongke/phat_trien_ky_nang.txt")

