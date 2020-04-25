import gensim
import networkx as nx
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from nltk.cluster.util import cosine_distance

import preprocessor


class Summarizer:

    def __init__(self, text, source,top_N):
        self.text = text
        self.source = source
        self.top_N = top_N

    def get_sentences(self):
        text = self.text.split(". ")
        for item in text:
            edited_item = np.char.lower(item)
            edited_item = np.array_str(edited_item)
            if self.source in edited_item:
                text.remove(item)
        sentences = {text.index(t): t for t in text}
        return sentences

    def doc2vec(self, sentences):
        fname = get_tmpfile('doc2vec.model')
        edited_sentences = {}
        train_corpus = []
        count = 0
        for index, sentence in sentences.items():
            processed_sentence = preprocessor.Preprocessor(sentence).preprocessData()
            if not processed_sentence:
                continue
            else:
                tokens = gensim.utils.simple_preprocess(processed_sentence)
                train_corpus.append(TaggedDocument(tokens, str(count)))
                edited_sentences[count] = sentence
                count = count + 1

        model = Doc2Vec(train_corpus, vector_size=10, dbow_words=1, dm=1, window=2, min_count=2)
        return (model, train_corpus, edited_sentences)

    def sentence_similarity(self, vector1, vector2):
        return abs(1 - cosine_distance(vector1, vector2))

    def build_similarity_matrix(self, model, corpus, sentences):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences) + 1, len(sentences) + 1))
        for index1, sentence1 in sentences.items():
            for index2, sentence2 in sentences.items():
                if index1 == index2:  # ignore if both are same sentences
                    continue
                similarity_matrix[index1][index2] = self.sentence_similarity(model.infer_vector(corpus[index1].words),
                                                                             model.infer_vector(corpus[index2].words))
        return similarity_matrix

    def summarize(self):
        sentences = self.get_sentences()
        model, train_corpus, edited_sentences = self.doc2vec(sentences)
        sentence_similarity_matrix = self.build_similarity_matrix(model, train_corpus, edited_sentences)
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
        scores = nx.pagerank(sentence_similarity_graph)
        # Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(edited_sentences)), reverse=True)
        summarize_text = []
        if len(ranked_sentence) >= self.top_N:
            for i in range(self.top_N):
                summarize_text.append("".join(edited_sentences[ranked_sentence[i][1]]))

            for item in summarize_text:
                if "  " in item:
                    summarize_text.remove(item)

            summary = ". ".join(summarize_text)
        else:
            summary = None

        return summary
