from nltk.stem.snowball import SnowballStemmer
import string
import re
from collections import Counter

ff = open("job_text", "r")
ff.seek(0)
all_text = ff.read()

text_string = re.sub('[^a-zA-Z0-9 \n\.]', '', all_text)
text_string = text_string.replace('\n', ' ')

split_text = text_string.split(' ')
stemmer = SnowballStemmer("english")

placeholder = []
for el in split_text:
    placeholder.append(stemmer.stem(el))

counts = Counter(mat)


### read email, navigate cursor to beginning, and read all the text
ff = open("../text_learning/test_email.txt", "r")
ff.seek(0)
all_text = f.read()

text_string = re.sub('[^a-zA-Z0-9 \n\.]', '', all_text)
text_string = text_string.replace('\n', ' ')

text = nltk.Text(tokens)

### break body content into pieces
### stem each word and concatenate back together
split_text = text_string.split(' ')
stemmer = SnowballStemmer("english")

placeholder = []
for el in split_text:
    placeholder.append(stemmer.stem(el))
words = " ".join(placeholder)

### Drop any introduction / signature terms
### ["sara", "shackleton", "chris", "germani"]
# for el in ["sara", "shackleton", "chris", "germani"]:
#     if el in words:
#         words = words.replace(el, "")

### Put words into sparse matrix and remove any stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

with open("word_data.pkl", "r") as data_file:
    word_data = pickle.load(data_file)

vectorizer = TfidfVectorizer(stop_words = sw, lowercase = True)
inform_words = vectorizer.fit_transform(placeholder)
vocab_list = vectorizer.get_feature_names()

### Look at shape of sparese matrix
print(inform_words.shape)