from nltk.stem.snowball import SnowballStemmer
import string

### read email, navigate cursor to beginning, and read all the text
ff = open("data_job_text", "r")
ff.seek(0)
all_text = ff.read()

### split off metadata (this may change depending upon email format)
content = all_text.split("X-FileName:")
words = ""

### grab the body content of the email
text_string = content[1].translate(string.maketrans("", ""), string.punctuation)

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
for el in ["sara", "shackleton", "chris", "germani"]:
    if el in words:
        words = words.replace(el, "")

### Put words into sparse matrix and remove any stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(stop_words = sw, lowercase = True)
inform_words = tfidf_vectorizer.fit_transform(word_data)
vocab_list = vectorizer.get_feature_names()

### Look at shape of sparese matrix
print(inform_words.shape)