import yake
import pymorphy2

class KeywordService:
    def __init__(self, text, language="ru", max_ngram_size=2, 
                 deduplication_threshold=0.9, deduplication_algo='seqm', windowSize=1, numOfKeywords=20):
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
        custom_kw_extractor = yake.KeywordExtractor(lan=self.language, n=self.max_ngram_size, dedupLim=self.deduplication_threshold, 
                                                    dedupFunc=self.deduplication_algo, windowsSize=self.windowSize, top=self.numOfKeywords, features=None)
        keywords = custom_kw_extractor.extract_keywords(self.text)
        keywords = [keyword[0] for keyword in keywords]
        return keywords

    def normalize_keywords(self, keywords):
        keywords = set([(self.morph.parse(keyword)[0].normal_form if len(keyword.split()) == 1 else keyword) 
                         for keyword in keywords if self.morph.parse(keyword)[0].tag.POS in self.tokens])
        return keywords

    def generate_tags(self):
        keywords = self.extract_keywords()
        keywords = self.normalize_keywords(keywords)
        return keywords
