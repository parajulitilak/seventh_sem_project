# summarizer_project/summarizer_app/t5_summarizer.py
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re

class T5Summarizer:
    def __init__(self):
        self.model = T5ForConditionalGeneration.from_pretrained("summarizer_app/models/pubmed_model")
        self.tokenizer = T5Tokenizer.from_pretrained("t5-base")

    def preprocess_text(self, text):
        """Clean the input text by removing special characters and digits."""
        clean_chars = []
        for char in text:
            if char.isalnum() or char.isspace() or char in ".,|?=":
                clean_chars.append(char)
        clean_text = "".join(clean_chars).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)  # Remove extra whitespace within text
        return clean_text

    def format_summary(self, summary):
        """Format the summary by capitalizing first letter and adding a full stop at the end."""
        summary = summary.strip()
        if summary.startswith(":"):
            summary = summary[1:].strip()
        summary = summary.capitalize()
        if not summary.endswith('.'):
            summary += '.'
        return summary

    # def summarize(self, original_text, summary_length):
    #     original_text = self.preprocess_text(original_text)
    #     inputs = self.tokenizer.encode("summarize: " + original_text, return_tensors="pt", max_length=512, truncation=True)
    #     summary_ids = self.model.generate(inputs, max_length=summary_length, length_penalty=5.0, num_beams=4, early_stopping=False)
    #     summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    #     formatted_summary = self.format_summary(summary)
    #     return formatted_summary
    
    def summarize(self, original_text, summary_length, max_length=512, length_penalty=2.0, num_beams=4, early_stopping=True):
        original_text = self.preprocess_text(original_text)
        inputs = self.tokenizer.encode("summarize: " + original_text, return_tensors="pt", max_length=max_length, truncation=True)
        summary_ids = self.model.generate(inputs, max_length=summary_length, length_penalty=length_penalty, num_beams=num_beams, early_stopping=early_stopping)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        formatted_summary = self.format_summary(summary)
        return formatted_summary
