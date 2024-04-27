import re
import math

class LSASummarizer:
    def __init__(self, original_text):
        self.original_text = original_text

    def clean_text(self, text):
        """Clean the input text by removing special characters and digits."""
        clean_chars = []
        for char in text:
            if char.isalnum() or char.isspace() or char in ".,|?/\"':;!()-":
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

    def calculate_covariance_matrix(self, mean_centered_dtm):
        """Calculate the covariance matrix."""
        num_sentences = len(mean_centered_dtm)
        num_words = len(mean_centered_dtm[0])
        covariance_matrix = [[0] * num_words for _ in range(num_words)]
        for i in range(num_words):
            for j in range(num_words):
                cov = sum(mean_centered_dtm[k][i] * mean_centered_dtm[k][j] for k in range(num_sentences)) / num_sentences
                covariance_matrix[i][j] = cov
        return covariance_matrix

    def perform_eigenvalue_decomposition(self, covariance_matrix):
        """Perform eigenvalue decomposition."""
        n = len(covariance_matrix)
        eigenvalues = [0] * n
        eigenvectors = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                eigenvectors[i][j] = 1 if i == j else 0
        tolerance = 1.0e-10
        max_iterations = 1000
        for iteration in range(max_iterations):
            sum_of_off_diagonal = 0
            for i in range(n - 1):
                for j in range(i + 1, n):
                    sum_of_off_diagonal += covariance_matrix[i][j] ** 2
            if math.sqrt(sum_of_off_diagonal) < tolerance:
                break
            max_element = 0
            max_row = 0
            max_col = 0
            for i in range(n - 1):
                for j in range(i + 1, n):
                    if abs(covariance_matrix[i][j]) >= max_element:
                        max_element = abs(covariance_matrix[i][j])
                        max_row = i
                        max_col = j
            theta = 0.5 * math.atan2(2 * covariance_matrix[max_row][max_col],
                                     covariance_matrix[max_row][max_row] - covariance_matrix[max_col][max_col])
            c = math.cos(theta)
            s = math.sin(theta)
            for i in range(n):
                temp = covariance_matrix[max_row][i]
                covariance_matrix[max_row][i] = c * temp + s * covariance_matrix[max_col][i]
                covariance_matrix[max_col][i] = -s * temp + c * covariance_matrix[max_col][i]
            for i in range(n):
                temp = covariance_matrix[i][max_row]
                covariance_matrix[i][max_row] = c * temp + s * covariance_matrix[i][max_col]
                covariance_matrix[i][max_col] = -s * temp + c * covariance_matrix[i][max_col]
            for i in range(n):
                temp = eigenvectors[i][max_row]
                eigenvectors[i][max_row] = c * temp + s * eigenvectors[i][max_col]
                eigenvectors[i][max_col] = -s * temp + c * eigenvectors[i][max_col]
        for i in range(n):
            eigenvalues[i] = covariance_matrix[i][i]
        return eigenvalues, eigenvectors

    def score_sentences(self, dtm, U_reduced, S_reduced):
        """Score sentences based on their importance."""
        sentence_scores = []
        for sentence_vector in dtm:
            concept_scores = [0] * len(U_reduced[0])
            for i in range(len(U_reduced[0])):
                for j in range(len(sentence_vector)):
                    concept_scores[i] += sentence_vector[j] * U_reduced[j][i]
            weighted_scores = [concept_scores[i] * S_reduced[i][i] for i in range(len(U_reduced[0]))]
            sentence_score = sum(weighted_scores)
            sentence_scores.append(sentence_score)
        return sentence_scores

    def select_top_sentences(self, sentence_scores, sentences, num_sentences=1):
        """Select top sentences based on their scores."""
        top_indices = sorted(range(len(sentence_scores)), key=lambda i: sentence_scores[i], reverse=True)[:num_sentences]
        selected_sentences = [sentences[i] for i in top_indices]
        return selected_sentences

    def format_summary(self, sentences):
        """Format the summary by capitalizing each sentence and joining them into a paragraph."""
        formatted_sentences = [sentence.strip().capitalize() for sentence in sentences]
        formatted_paragraph = ". ".join(formatted_sentences)
        return formatted_paragraph + '.'

    def preprocess_text(self, text):
        """Preprocess text before summarization."""
        cleaned_text = self.clean_text(text)
        normalized_text = self.normalize_text(cleaned_text)
        return normalized_text

    def postprocess_summary(self, summary):
        """Postprocess summary to handle potential issues with symbols."""
        # Handle any specific post-processing requirements here
        # For example, you may want to ensure proper spacing around punctuation marks
        summary = re.sub(r'\s*([.,!?;:])\s*', r'\1 ', summary)
        return summary

    def summarize(self, summary_length):
        """Generate LSA-based summary."""
        preprocessed_text = self.preprocess_text(self.original_text)
        sentences = self.tokenize_sentences(preprocessed_text)
        tokenized_sentences = self.tokenize_words(sentences)
       

        term_document_matrix = self.create_term_document_matrix(tokenized_sentences)
        dtm = self.calculate_dtm(term_document_matrix)
        mean_centered_dtm = self.mean_center(dtm)
        covariance_matrix = self.calculate_covariance_matrix(mean_centered_dtm)
        eigenvalues, eigenvectors = self.perform_eigenvalue_decomposition(covariance_matrix)
        U = eigenvectors
        S = [[0] * len(eigenvalues) for _ in range(len(eigenvalues))]
        for i in range(len(eigenvalues)):
            S[i][i] = eigenvalues[i]
        Vt = [[0] * len(eigenvalues) for _ in range(len(eigenvalues))]
        for i in range(len(eigenvalues)):
            Vt[i] = [U[j][i] for j in range(len(eigenvalues))]
        threshold = 0.1
        selected_components = [i for i in range(len(eigenvalues)) if eigenvalues[i] >= threshold]
        U_reduced = [[U[j][i] for i in selected_components] for j in range(len(eigenvalues))]
        S_reduced = [[S[i][j] for j in selected_components] for i in selected_components]
        Vt_reduced = [[Vt[i][j] for j in selected_components] for i in range(len(eigenvalues))]
        sentence_scores = self.score_sentences(dtm, U_reduced, S_reduced)
        summary_sentences = self.select_top_sentences(sentence_scores, sentences, summary_length)
        formatted_summary = self.format_summary(summary_sentences)
        return formatted_summary


# Example usage
if __name__ == "__main__":
    # Sample input text
    input_text = "It's The World Soil Day is being observed today globally as well as in Nepal with the objective of raising public awareness on the significance of healthy soil\
          and for the sustainable management of the soil fertility.The United Nations General Assembly had in December 2013 declared December 5, 2014 as the World Soil Day and it\
              was formally marked throughout the world since then. Nepal has been observing the Day since 2015. The theme of the World Soil Day this year is 'Soils: where food begins.\
                ' Soil is at the heart of all agricultural activities, food security, nutrition security and climate conservation. The World Soil Day programme reiterates the \
                    importance of soil for mankind and the crucial need for its conservation and proper management while at the same time increasing its fertility, the Department\
                          of Agriculture said.Director General of the Department, Dr Rewati Raman Poudel said that the debate about food and nutritional security, sustainable\
                              agriculture development, conservation of bio-diversity and organic agriculture will have no meaning without the conservation, promotion and proper\
                                  management of soil. The soil fertility is deteriorating throughout the world including in Nepal in the recent years with the declining physical,\
                                      chemical and biological features of the soil. Therefore, this problem of declining soil fertility has been taken as the common global problem.\
                                          Poudel said the World Soil Day is being marked with the main goal of raising extensive public awareness to tackle this growing problem of\
                                              loss in soil fertility. The World Soil Day is being celebrated at the national level today in Nepal amidst various programmes under\
                                                  the aegis of the Department, Central Agricultural Laboratory, the National Soil Science Research Centre (NARC), Food and Nutrition Security\
                                                      Improvement Project, Rural Enterprises and Economic Development Project, United Nations, Food and Agriculture Organization and the Nepalese\
                                                          Society of Soil Science. The UN has said that over the last 70 years, the level of vitamins and nutrients in food has drastically decreased,\
                                                              and it is estimated that 2 billion people worldwide suffer from lack of micronutrients, known as hidden hunger because it is difficult to\
                                                                  detect. Soil degradation induces some soils to be nutrient depleted losing their capacity to support crops, while others have such a high\
                                                                      nutrient concentration that represent a toxic environment to plants and animals, pollutes the environment and cause climate change. World\
                                                                          Soil Day 2022 and its campaign Soils: Where food begins aims to raise awareness of the importance of maintaining healthy ecosystems\
                                                                              and human well-being by addressing the growing challenges in soil management, increasing soil awareness and encouraging societies to improve soil health."
    

    
    # Create an instance of LSASummarizer
    summarizer = LSASummarizer(input_text)
    
    # Specify the desired length of the summary
    summary_length = 3
    
    # Generate the LSA-based summary
    summary = summarizer.summarize(summary_length)
    
    # Print the summary
    print("LSA Summarization:")
    print(summary)
