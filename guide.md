pip install transformers
pip install sentencepiece
pip3 install torch torchvision torchaudio

##Home Page (home.html):

The user inputs the original text in the "Original Text" text area.
The user selects an algorithm from the dropdown list.
The user sets the summary length using the range slider.
The user clicks the "Summarize" button.


##JavaScript (your_script.js):

The summarizeText function is triggered when the "Summarize" button is clicked.
It retrieves the input text, selected algorithm, and summary length from the user.
The generateSummary function is called to generate a placeholder summary. (You can replace this with the actual logic for generating a summary.)
The saveSummaryToDatabase function is called to send the input text, algorithm, summary length, and generated summary to the Django view using AJAX.


##jango View (views.py):

The Django view summarize receives the POST request with input text, algorithm, summary length, and generated summary.
The t5_summarize function is called to generate the summary using the T5 model.
The generated summary, along with other details, is saved to the database using the Summary model.

##Database (models.py):

The Summary model stores information about each summarization task, including input text, algorithm, summary length, and generated summary.

##AJAX Response:

Once the summary is saved to the database, a response is sent back to the JavaScript using AJAX.


##JavaScript (your_script.js):

The handleAjaxResponse function processes the AJAX response.
If the response is valid, it calls updateGeneratedSummary to update the page with the generated summary, word count, and sentence count.


##Updated Home Page (home.html):

The "Summarized Text" section is updated with the generated summary, word count, and sentence count.



put slides in the slides/slides.pptx directory name as same;


latent_semantic_analysis(input_text,summary_length):
    ... apply all code here


    return summary