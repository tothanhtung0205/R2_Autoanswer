# -*- coding=utf-8 -*-
# author = "tungtt"
from time import time
from data import Data
import numpy as np
from io import open
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from underthesea import word_sent
from collections import Counter
from sklearn.externals import joblib
from sklearn.cluster import KMeans

class TfidfModel(Data):

    def __init__(self,train,corpus_file):
        super(TfidfModel,self).__init__(train,corpus_file)
        self.vect = TfidfVectorizer()
        t0 = time()
        self.corpus_tfidf_matrix = self.vect.fit_transform(self.corpus)
        print("Calculate tfidf in %f s" %(time() - t0) )


    def update(self,new_sen,new_ans):
        """
        add new_sen to corpus and re-calculate corpus_tfidf_matrix
        :param new_sen:
        :return:
        """
    # if float(self.get_similar_sen(new_sen,1)[0][2]) < 0.9:
        self.data.append(new_sen)
        new_prced_sen = self.pre_process(new_sen)
        self.corpus.append(new_prced_sen)
        self.ans_list.append(new_ans)
        self.corpus_tfidf_matrix = self.vect.fit_transform(self.corpus)
        print("Updated new sentences")


    def write_dict(self,file_name):
        """
        Write word dictionary to file_name
        :param file_name: filename to write
        :return:
        """
        dict = self.vect.get_feature_names()
        with open(file_name,"w",encoding="utf-8") as f_w:
            for word in dict:
                f_w.write(word)
                f_w.write(u'\n')
        f_w.close()


    def get_new_sen_tfidf(self,new_sen,vect):
        """
        preprocess new_sen , remove word that not exist in dictionary
        Calculate TFIDF of new sentence
        :param new_sen:
        :return: tfidf_vec of new_sen
        """
        new_sen = self.pre_process(new_sen)
        new_sen = new_sen.split()
        dict = vect.get_feature_names()
        idf = vect.idf_
        removed_sen = []
        for word in new_sen:
            if (word in dict):
                removed_sen.append(word)
        print(u"New sen preprocessed : ")
        print(u" ".join(removed_sen) )
        print("-"*100)
        tf = Counter(removed_sen)
        tf_vect = [0] * len(dict)
        for i, word in enumerate(dict):
            if word in removed_sen:
                x = tf[word]
                tf_vect[i] = x
        tfidf_vec = [a * b for a, b in zip(tf_vect, idf)]
        return tfidf_vec


    def get_similar_sen(self,new_sen,num_sens):
        """
        get 4 similar sen in corpus of new_sen
        :param new_sen:
               num_sens : number of similar sens
        :return: list of 4 similar sentences with new_sen
         element of list : [raw_sen,corpus_sen,cosine,answer]
        """

        tfidf_matrix = self.corpus_tfidf_matrix
        data = self.data
        ans_list = self.ans_list
        corpus = self.corpus
        vect = self.vect

        similar_sen_list = []
        tfidf_new = self.get_new_sen_tfidf(new_sen,vect)
        tfidf_new = [tfidf_new]
        t0 = time()
        cos_sim = cosine_similarity(tfidf_new, tfidf_matrix)
        #print("Calculate cosine similar in %f s" %(time()-t0))
        cos_sim = cos_sim[0]
        for i in xrange(num_sens):
            max_val = max(cos_sim)
            max_idx = np.where(cos_sim == max_val)
            max_idx = max_idx[0][0]
            raw_sen = data[max_idx]
            sen = corpus[max_idx]
            ans = ans_list[max_idx]
            similar_sen_list.append([raw_sen, sen, unicode(max_val), ans])
            cos_sim[max_idx] = -1
        return (similar_sen_list)


    def get_sim(self,new_sen):
        """
        get 4 similar sens with new_sen
        :param new_sen:
        :return: list of similar sen that cosine > 0.4
        """
        sen_list = self.get_similar_sen(new_sen,4)
        arr = []
        for sen in sen_list:
            if float(sen[2]) > 0.5:
                arr.append([sen[0],sen[3]])
        # return [[sen[0],sen[3]] for sen in sen_list]
        print arr
        return arr



    def get_dictionary(self,file_name):
        vect = TfidfVectorizer()
        tfidf_matrix = vect.fit_transform(self.data)
        dict = vect.get_feature_names()
        a = vect.idf_
        idf_map = zip(a, dict)
        idf_sorted = sorted(idf_map, key=lambda x: x[0])

        with open(file_name, "w", encoding="utf-8") as f:

            for word in idf_sorted:
                f.write(word[1])
                f.write(u"\n")

        f.close()


if __name__ == "__main__":

    model = TfidfModel('data/phat_trien_ky_nang/train.txt','data/phat_trien_ky_nang/corpus_train.txt')
    model.get_dictionary('data/phat_trien_ky_nang/stopwords.txt')