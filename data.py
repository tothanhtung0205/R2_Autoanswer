# -*- coding=utf-8 -*-
# author = "tungtt"


from underthesea import word_sent
from io import open

class Data(object):

    def __init__(self,train,corpus_file):

        self.data,self.ans_list = self.read_data(train)
        self.stw_list = self.get_stw_list()
        self.corpus = self.get_corpus_from_file(corpus_file)


    def get_corpus_from_file(self,corpus_file):
        corpus = []
        try:
            print("Get corpus from file.")
            with open(corpus_file, "r", encoding="utf-8") as f:
                for line in f:
                    corpus.append(line)
        except:
            print("Get corpus from data and write to file .")
            corpus = self.get_corpus(self.data,corpus_file)
        return corpus


    def remove_stw(self,sen):
        words_list = []
        stw_list = self.stw_list
        words = sen.split()
        for word in words:
            if word in stw_list:
                continue
            else:
                words_list.append(word)
        return u" ".join(words_list)

    def repace_wrong_tokenize(self,sen):
        # todo tao file replace
        sen = sen.replace(u"bài tập", u"bài_tập")
        sen = sen.replace(u"học tập", u"học_tập")
        sen = sen.replace(u"kỷ năng", u"kỹ_năng")
        sen = sen.replace(u"biểu hiện", u"biểu_hiện")
        sen = sen.replace(u"thành công_của", u"thành_công của")
        sen = sen.replace(u"học_tập trung", u"học tập_trung")
        sen = sen.replace(u" ko ",u" không ")
        sen = sen.replace(u" e ",u" em ")
        for c in sen:
            if c in [u"-", u"?", u"!", u",", u";", u".", u":", u'/',u'\'',u'\"']:
                sen = sen.replace(c, u" ")
        return sen


    def pre_process(self,sen):
        sen = word_sent(sen, format="text")
        sen = sen.lower()
        sen = self.repace_wrong_tokenize(sen)
        prced_sen = self.remove_stw(sen)
        return prced_sen


    def get_corpus(self,data, to_write):
        count = 0
        corpus = []
        with open(to_write, "w", encoding="utf-8") as f_w:
            for sen in data:
                if len(sen) > 1000:
                    continue
                prced_sen = self.pre_process(sen)
                corpus.append(prced_sen)
                f_w.write(prced_sen)
                f_w.write(u"\n")
                count += 1
                print("Write sen : " + str(count))
        f_w.close()
        return corpus


    def get_stw_list(seft):
        stw_list = []
        with open("dict/stopwords.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.replace("\n", "")
                stw_list.append(line)
        return stw_list


    def read_data(self,file_name):
        dataset = []
        answer = []
        with open(file_name, "r", encoding="utf-8") as f:
            for line in f:
                ques = line.split("--->")
                dataset.append(ques[0])
                answer.append(ques[1])
        return dataset, answer

    def get_test_data(self,file_name):
        test_list = []
        with open(file_name, "r", encoding="utf-8") as f_r:
            for line in f_r:
                sen = line.split(u"--->")[0]
                test_list.append(sen)
        return test_list

data = Data("data/train.txt" , "data/corpus_train.txt")
print data