import re
import math
import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag
from nltk.tokenize import word_tokenize

class TopicExtractor:
    def __init__(self):
        self.word_counts = {}
        self.document_count = 0

    def preprocess_text(self, text):
        # Convert text to lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text

    def update_word_counts(self, words):
        # Update word counts
        for word in words:
            if word in self.word_counts:
                self.word_counts[word] += 1
            else:
                self.word_counts[word] = 1
        self.document_count += 1

    def calculate_tfidf(self, word):
        # Calculate TF-IDF for a word
        tf = self.word_counts[word] / sum(self.word_counts.values())
        idf = math.log(self.document_count / (1 + sum(1 for count in self.word_counts.values() if count > 0)))
        return tf * idf

    def extract_topics(self, text):
        # Preprocess text
        text = self.preprocess_text(text)
        # Tokenize text into words
        words = word_tokenize(text)
        # Tag words with parts of speech
        tagged_words = pos_tag(words)
        # Filter out non-noun words
        noun_words = [word for word, pos in tagged_words if pos.startswith('N')]
        # Update word counts
        self.update_word_counts(noun_words)
        # Calculate TF-IDF for each word
        tfidf_scores = {word: self.calculate_tfidf(word) for word in noun_words}
        # Sort words by TF-IDF score in descending order
        sorted_words = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
        # Extract top N words as topics
        num_topics = min(5, len(sorted_words))  # Extract top 5 topics
        topics = [word for word, _ in sorted_words[:num_topics]]
        # Generate short topic sentence
        short_topic = " ".join(topics) + "."
        return short_topic
    
    def intermediate_results(self, text):
        preprocessed_text = self.preprocess_text(text)
        words = word_tokenize(preprocessed_text)
    
   
        tagged_words = pos_tag(words)

        noun_words = [word for word, pos in tagged_words if pos.startswith('N')]
    
  
        self.update_word_counts(noun_words)
        tfidf_scores = {word: self.calculate_tfidf(word) for word in noun_words}

        sorted_words = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

        num_topics = min(5, len(sorted_words))  # Extract top 5 topics
        topics = [word for word, _ in sorted_words[:num_topics]]

        short_topic = " ".join(topics) + "."

        intermediate_results = {
            "input_text" : text,
            "preprocessed_text": preprocessed_text,
            "tokenized_words": words,
            "tagged_words": tagged_words,
            "noun_words": noun_words,
            "tfidf_scores": tfidf_scores,
            "sorted_words": sorted_words,
            "top_topics": topics,
            "short_topic": short_topic
        }
    
        return intermediate_results


# # Example usage
# if __name__ == "__main__":
#     # Sample input text
#     input_text = "It's The World Soil Day is being observed today globally as well as in Nepal with the objective of raising public awareness on the significance of healthy soil\
#           and for the sustainable management of the soil fertility.The United Nations General Assembly had in December 2013 declared December 5, 2014 as the World Soil Day and it\
#               was formally marked throughout the world since then. Nepal has been observing the Day since 2015. The theme of the World Soil Day this year is 'Soils: where food begins.\
#                 ' Soil is at the heart of all agricultural activities, food security, nutrition security and climate conservation. The World Soil Day programme reiterates the \
#                     importance of soil for mankind and the crucial need for its conservation and proper management while at the same time increasing its fertility, the Department\
#                           of Agriculture said.Director General of the Department, Dr Rewati Raman Poudel said that the debate about food and nutritional security, sustainable\
#                               agriculture development, conservation of bio-diversity and organic agriculture will have no meaning without the conservation, promotion and proper\
#                                   management of soil. The soil fertility is deteriorating throughout the world including in Nepal in the recent years with the declining physical,\
#                                       chemical and biological features of the soil. Therefore, this problem of declining soil fertility has been taken as the common global problem.\
#                                           Poudel said the World Soil Day is being marked with the main goal of raising extensive public awareness to tackle this growing problem of\
#                                               loss in soil fertility. The World Soil Day is being celebrated at the national level today in Nepal amidst various programmes under\
#                                                   the aegis of the Department, Central Agricultural Laboratory, the National Soil Science Research Centre (NARC), Food and Nutrition Security\
#                                                       Improvement Project, Rural Enterprises and Economic Development Project, United Nations, Food and Agriculture Organization and the Nepalese\
#                                                           Society of Soil Science. The UN has said that over the last 70 years, the level of vitamins and nutrients in food has drastically decreased,\
#                                                               and it is estimated that 2 billion people worldwide suffer from lack of micronutrients, known as hidden hunger because it is difficult to\
#                                                                   detect. Soil degradation induces some soils to be nutrient depleted losing their capacity to support crops, while others have such a high\
#                                                                       nutrient concentration that represent a toxic environment to plants and animals, pollutes the environment and cause climate change. World\
#                                                                           Soil Day 2022 and its campaign Soils: Where food begins aims to raise awareness of the importance of maintaining healthy ecosystems\
#                                                                               and human well-being by addressing the growing challenges in soil management, increasing soil awareness and encouraging societies to improve soil health."
    
#     # Create an instance of TopicExtractor
#     topic_extractor = TopicExtractor()
    
#     # Extract short topic from input text
#     short_topic = topic_extractor.extract_topics(input_text)
#     print("Short Topic:", short_topic)
