import time
from wordcloud import WordCloud
import pandas as pd
import os
from datetime import datetime
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from collections import defaultdict
import string
from nltk import pos_tag
import math

'''
따라서, TF-IDF 값은 TF 값과 IDF 값을 곱하여 계산합니다. 이 값이 높을수록 해당 단어는 문서 내에서 중요하다는 것을 나타냅니다.

구체적인 계산 공식은 아래와 같습니다.

TF(t, d) = (t가 문서 d에 나타난 횟수) / (문서 d에 있는 총 단어 수)

IDF(t, D) = log_e(총 문서 수 / (1 + t가 나타난 문서 수))

TF-IDF(t, d, D) = TF(t, d) * IDF(t, D)

'''
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
# COL_CONTENT = "Content"
# COL_DATE = "Creation Time"
COL_CONTENT = "diary_contents"
COL_DATE = "written_date"

#CSV_NAME = "data_5.csv"
CSV_NAME = "young_raw.csv"

CSV_PATH = os.path.join(CURRENT_PATH, CSV_NAME)
REMOVAL_WORDS = ['’','im']
PLOT_RAW_NUM = 15

def content_word_tokenize(text):
    sententces = sent_tokenize(text)
    tagged_sentences=[]
    tagged_words = []

    removal_words = set.union(set(stopwords.words('english')) , set(string.punctuation) , set(REMOVAL_WORDS))
    for sentence in sententces:
        tokens = word_tokenize(sentence)
        tagged_tokens = pos_tag(tokens)

        #lowercasing
        tagged_tokens = [(x.lower(),y) for x,y in tagged_tokens]

        #stopword removal
        tagged_tokens = [(x,y) for x,y in tagged_tokens if not x in removal_words]
        


        tagged_sentences.append(tagged_tokens)
        tagged_words = tagged_words + tagged_tokens

    return tagged_words


def calculate_tf(words_list,tf_data):
    for word in words_list:
        count = words_list.count(word)
        tf_data[word]=count/len(words_list)*100

def calculate_idf(words_list,df,idf_data):
    for word in set(words_list):
        cnt=0
        for diary in df[COL_CONTENT]:
            if word in diary:
                cnt = cnt+1
        idf_data[word]=math.log(len(df[COL_CONTENT])/(1+cnt))

def plot_bar(tf_idf_data,title,save_name):
    sorted_tf_idf_data = dict(sorted(tf_idf_data.items(),reverse=True, key=lambda item: item[1]))
    names = [str(x) + "("+ str(y)+")" for x,y in sorted_tf_idf_data.keys()]
    values = list(sorted_tf_idf_data.values())
    #plt.figure(figsize=(20, 10))
    plt.clf()
    plt.title(title)
    plt.bar(names[:PLOT_RAW_NUM], values[:PLOT_RAW_NUM])
    for i in range(len(names[:PLOT_RAW_NUM])):
        plt.text(names[i], values[i], str(math.floor(values[i]*100)/100), ha='center', va='bottom')  # 막대 그래프 생성
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'./keyword-analayze/{save_name}')

def plot_word_cloud(tf_idf_data,title,save_name):
    str_dict = {str(x[0]):y for x,y in tf_idf_data.items()}
    wordcloud = WordCloud(background_color='white').generate_from_frequencies(str_dict)

    # 워드 클라우드 시각화
    plt.clf()
    plt.title(title)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'./keyword-analayze/{save_name}')

df = pd.read_csv(CSV_PATH)

df[COL_CONTENT]=df[COL_CONTENT].apply(content_word_tokenize)

for index, value in enumerate(df[COL_CONTENT]):

    idf_data = defaultdict(int)
    tf_data = defaultdict(int)
    tf_idf_data = defaultdict(int)
    calculate_tf(value,tf_data)
    
    calculate_idf(value,df,idf_data)
    for key in tf_data.keys():
        tf_idf_data[key]=tf_data[key]*idf_data[key]
        
    
    plot_bar(tf_idf_data,str(df[COL_DATE][index]),f'bar_{str(df[COL_DATE][index])}_tfidf.png')
    plot_bar(tf_data,str(df[COL_DATE][index]),f'bar_{str(df[COL_DATE][index])}_tf.png')
    plot_bar(idf_data,str(df[COL_DATE][index]),f'bar_{str(df[COL_DATE][index])}_idf.png')
    plot_word_cloud(tf_idf_data,str(df[COL_DATE][index]),f'word_cloud_{str(df[COL_DATE][index])}_tfidf.png')
    plot_word_cloud(tf_data,str(df[COL_DATE][index]),f'word_cloud_{str(df[COL_DATE][index])}_tf.png')
    plot_word_cloud(idf_data,str(df[COL_DATE][index]),f'word_cloud_{str(df[COL_DATE][index])}_idf.png')

    print(index)
    

