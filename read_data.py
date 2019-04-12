from bs4 import BeautifulSoup

class Review:
    def __init__(self):
        self.id = None
        self.sentences = []
        self.opinions = []

    def __str__(self):
        s = u"--- Review [{}] ---".format(self.id)
        s += u"\nSentences:"
        for sentence in self.sentences:
            s += u"\n  " + str(sentence)

        if self.opinions:
            s += u"\nText-Level Opinions:"
            for opinion in self.opinions:
                s += u"\n  " + str(opinion)
        return s.encode("utf-8")


class Sentence:
    def __init__(self):
        self.review_id = None
        self.id = None
        self.text = None
        self.out_of_scope = False
        self.opinions = []

    def __str__(self):
        s = u"[{}]: '{}'".format(self.id, self.text)
        if self.opinions:
            s += u"\n  Sentence-Level Opinions:"
            for o in self.opinions:
                s += u"\n  " + str(o)
            s += u"\n"
        return s.encode("utf-8")


class Opinion:
    def __init__(self):
        self.target = None
        self.category = None
        self.entity = None
        self.attribute = None
        self.polarity = None
        self.start = None
        self.end = None

    def __str__(self):
        if self.target:
            s = u"[{}; {}] '{}' ({}-{})".format(self.category, self.polarity, self.target, self.start, self.end)
        else:
            s = u"[{}; {}]".format(self.category, self.polarity)
        return s.encode("utf-8")


def read_semeval2014_task4(filepath, aspect_terms=True, aspect_categories=True):
    reviews = []
    with open(filepath, encoding='utf-8') as f:
        soup = BeautifulSoup(f, "xml")
        sentence_tags = soup.find_all("sentence")
        for s_tag in sentence_tags:
            sentence = Sentence()
            sentence.id = s_tag["id"]

            # dummy review
            review = Review()
            review.id = "Review_" + sentence.id

            sentence.review_id = review.id
            sentence.text = s_tag.find("text").get_text()

            if aspect_terms:
                aspect_term_tags = s_tag.find_all("aspectTerm")
                for a_tag in aspect_term_tags:
                    opinion = Opinion()

                    opinion.category = None
                    opinion.entity = None
                    opinion.attribute = None

                    try:
                        opinion.polarity = a_tag["polarity"]
                    except KeyError:
                        opinion.polarity = None

                    try:
                        opinion.target = a_tag["term"]
                        if opinion.target == "NULL":
                            opinion.target = None
                        else:
                            opinion.start = int(a_tag["from"])
                            opinion.end = int(a_tag["to"])
                    except KeyError:
                        pass
                    sentence.opinions.append(opinion)

            review.sentences.append(sentence)
            reviews.append(review)
    return reviews


def save_tsv(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as outer:
        for each_data in data:
            outer.write(each_data+'\n')

if __name__ == '__main__':
    reviews = read_semeval2014_task4(filepath=r"C:\Users\gzj\Desktop\SemEval2014数据集整理\测试集\ABSA_Gold_TestData\Restaurants_Test_Gold.xml")
    count = 0
    data = []
    for i in reviews:
        for j in i.sentences:
            for k in j.opinions:
                text = j.text.strip()
                sentence_with_t = text[:k.start] + '$T$' + text[k.end:]
                
                print(j.review_id)
                print(text)
                print(sentence_with_t)
                print(k.target)
                print(k.polarity)

                # if k.polarity == 'conflict':  # 去除conflict标签，做三分类
                #     continue
                
                data.append(sentence_with_t)
                data.append(k.target)
                data.append(k.polarity)

                count = count + 1
                print(str(count) + "-"*100)
    save_tsv(r'测试集\Restaurant_Test_Gold_4way', data)