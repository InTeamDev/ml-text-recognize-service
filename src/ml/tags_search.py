from string import punctuation

import pymorphy2
import yake


class KeywordService:
    def __init__(
        self,
        text,
        language="ru",
        max_ngram_size=1,
        deduplication_threshold=0.9,
        deduplication_algo='seqm',
        windowSize=1,
        numOfKeywords=10000,
    ):
        self.text = text
        self.language = language
        self.max_ngram_size = max_ngram_size
        self.deduplication_threshold = deduplication_threshold
        self.deduplication_algo = deduplication_algo
        self.windowSize = windowSize
        self.numOfKeywords = numOfKeywords
        self.morph = pymorphy2.MorphAnalyzer()
        self.tokens = ['NOUN', 'NUMR', None]

    def extract_keywords(self):
        custom_kw_extractor = yake.KeywordExtractor(
            lan=self.language,
            n=self.max_ngram_size,
            dedupLim=self.deduplication_threshold,
            dedupFunc=self.deduplication_algo,
            windowsSize=self.windowSize,
            top=self.numOfKeywords,
            features=None,
        )
        keywords = custom_kw_extractor.extract_keywords(self.text)
        return keywords

    def lemmatize_text(self):
        words = self.text.split()
        lemmatized_words = list()
        for word in words:
            word_save = word
            punct = ""
            if word[-1] in punctuation:
                punct = word[-1]
                word = word[:-1]
                word_save = word
            word = self.morph.parse(word)[0].inflect({'sing'})
            if word is None:
                word = word_save
            else:
                word = word.normal_form
            word += punct
            lemmatized_words.append(word)
        lemmatized_text = ' '.join(lemmatized_words)
        return lemmatized_text

    def normalize_keywords(self, input_keywords):
        keywords = list()
        for keyword in input_keywords:
            if self.morph.parse(keyword[0])[0].tag.POS in self.tokens:  # type: ignore
                if keyword[0][-1] in punctuation:
                    keyword = (keyword[0][:-1], keyword[1])
                keywords.append(keyword)
        return keywords

    def sort_keywords_frequency(self, keywords):
        keywords.sort(key=lambda keyword: keyword[1])
        keywords = list(reversed(keywords))
        return keywords

    def return_first_max_frequency(self, keywords, count):
        return list(map(lambda keyword: keyword[0], keywords[:count]))

    def generate_tags(self):
        self.text = self.lemmatize_text()
        keywords = self.extract_keywords()
        keywords = self.normalize_keywords(keywords)
        keywords = self.sort_keywords_frequency(keywords)
        keywords = self.return_first_max_frequency(keywords, 20)
        return keywords
