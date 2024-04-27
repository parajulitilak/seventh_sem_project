import re
import numpy as np

class LSASummarizer:
    def __init__(self, original_text):
        self.original_text = original_text

    def clean_text(self, text):
        """Clean the input text by removing special characters and digits."""
        clean_chars = []
        for char in text:
            if char.isalnum() or char.isspace() or char in ".,|?=":
                clean_chars.append(char)
        clean_text = "".join(clean_chars).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)  # Remove extra whitespace within text
        return clean_text

    def normalize_text(self, text):
        """Normalize text by applying advanced stemming and converting to lowercase."""
        return text.lower()

    def tokenize_sentences(self, text):
        """Split text into sentences based on common sentence ending punctuation."""
        sentences = []
        current_sentence = ""
        for char in text:
            if char in ".!?":
                sentences.append(current_sentence)
                current_sentence = ""
            else:
                current_sentence += char
        sentences.append(current_sentence)  # Add the last sentence
        return sentences

    def tokenize_words(self, sentences):
        """Split sentences into lists of words."""
        tokenized_sentences = []
        for sentence in sentences:
            words = sentence.split()
            tokenized_sentences.append(words)
        return tokenized_sentences

    def create_term_document_matrix(self, tokenized_sentences):
        """Create a term-document matrix where rows represent words and columns represent sentences."""
        term_document_matrix = {}
        for sentence_index, sentence in enumerate(tokenized_sentences):
            for word in sentence:
                if word not in term_document_matrix:
                    term_document_matrix[word] = [0] * len(tokenized_sentences)
                term_document_matrix[word][sentence_index] += 1
        return term_document_matrix

    def calculate_dtm(self, term_document_matrix):
        """Transpose the term-document matrix to create the document-term matrix."""
        dtm = [[term_document_matrix[word][i] for word in term_document_matrix] for i in range(len(term_document_matrix[next(iter(term_document_matrix))]))]
        return dtm

    def mean_center(self, dtm):
        """Mean-center the document-term matrix."""
        for column in range(len(dtm[0])):
            column_mean = sum(row[column] for row in dtm) / len(dtm)
            for row in dtm:
                row[column] -= column_mean
        return dtm

    def calculate_covariance_matrix_optimized(self, mean_centered_dtm):
        """Calculate the covariance matrix efficiently using NumPy."""
        dtm_array = np.array(mean_centered_dtm)  # Convert to NumPy array for faster operations
        covariance_matrix = np.cov(dtm_array.T)  # Calculate covariance using NumPy's optimized function
        return covariance_matrix

    def perform_eigenvalue_decomposition(self, covariance_matrix):
        """Perform eigenvalue decomposition."""
        eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]
        return eigenvalues, eigenvectors

    def score_sentences(self, dtm, U_reduced, S_reduced):
        """Score sentences based on their importance."""
        sentence_scores = []
        for sentence_vector in dtm:
            concept_scores = np.dot(sentence_vector, U_reduced)
            weighted_scores = concept_scores * S_reduced
            sentence_score = np.sum(weighted_scores)
            sentence_scores.append(sentence_score)
        return sentence_scores

    def select_top_sentences(self, sentence_scores, sentences, num_sentences=1):
        """Select top sentences based on their scores."""
        top_indices = np.argsort(sentence_scores)[-num_sentences:][::-1]
        selected_sentences = [sentences[i] for i in top_indices]
        return selected_sentences

    def format_summary(self, sentences):
        """Format the summary by capitalizing each sentence and joining them into a paragraph."""
        formatted_sentences = [sentence.strip().capitalize() for sentence in sentences]
        formatted_paragraph = ". ".join(formatted_sentences)
        return formatted_paragraph + '.'

    def summarize(self, summary_length):

        intermediate_result ={}

        """Generate LSA-based summary."""
        clean_text = self.clean_text(self.original_text)
        intermediate_result['clean_text'] = clean_text

        normalized_text = self.normalize_text(clean_text)
        intermediate_result['normalized_text'] = normalized_text

        tokenized_sentences = self.tokenize_sentences(normalized_text)
        intermediate_result['tokenized_sentences'] = tokenized_sentences

        tokenized_words = self.tokenize_words(tokenized_sentences)
        intermediate_result['tokenized_words'] = tokenized_words

        term_document_matrix = self.create_term_document_matrix(tokenized_words)
        intermediate_result['term_document_matrix'] = term_document_matrix

        dtm = self.calculate_dtm(term_document_matrix)
        intermediate_result['dtm'] = dtm

        mean_centered_dtm = self.mean_center(dtm)
        intermediate_result['mean_centered_dtm'] = mean_centered_dtm

        covariance_matrix = self.calculate_covariance_matrix_optimized(mean_centered_dtm)
        intermediate_result['covariance_matrix'] = covariance_matrix

        eigenvalues, eigenvectors = self.perform_eigenvalue_decomposition(covariance_matrix)
        intermediate_result['eigenvalues'] = eigenvalues
        intermediate_result['eigenvectors'] = eigenvectors

        U = np.column_stack(eigenvectors)
        S = np.diag(eigenvalues)
        Vt = U.T
        threshold = 0.1
        selected_components = np.where(eigenvalues >= threshold)[0]
        U_reduced = U[:, selected_components]
        S_reduced = S[selected_components, selected_components]
        Vt_reduced = Vt[:, selected_components]

        sentence_scores = self.score_sentences(dtm, U_reduced, S_reduced)
        intermediate_result['sentence_scores'] = sentence_scores

        summary_sentences = self.select_top_sentences(sentence_scores, tokenized_sentences, summary_length)
        intermediate_result['summary_sentences'] = summary_sentences

        formatted_summary = self.format_summary(summary_sentences)
        intermediate_result['formatted_summary'] = formatted_summary




        return intermediate_result

    

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
    

    
#     # Create an instance of LSASummarizer
#     summarizer = LSASummarizer(input_text)
    
#     # Specify the desired length of the summary
#     summary_length = 1
    
#     # Generate the LSA-based summary
#     summary = summarizer.lsa_summarize(summary_length)
    
#     # Print the summary
#     print("LSA Summarization:")
#     print(summary)