# summarizer_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Summary
# from transformers import T5Tokenizer, T5ForConditionalGeneration
import re
import json


#added this on recommendation from jagdish sir.
from .models import Summary
def dashboard(request):
    summaries = Summary.objects.filter(user=request.user)
    return render(request, 'summarizer_app/dashboard.html', {'summaries': summaries})

def get_summary_details(request, input_text_id):
    # Retrieve summary details from the database based on input_text_id
    # Assuming you have a model named InputText and Summary associated with it
    input_text = InputText.objects.get(id=input_text_id)
    summary = Summary.objects.get(input_text=input_text)
    
    # Prepare summary data
    summary_data = {
        'inputText': summary.input_text,
        'summarizedText': summary.summarized_text
    }
    
    # Return summary data as JSON response
    return JsonResponse(summary_data)

#---------------------------------------------------------------------------------

def front_page(request):
    return render(request, 'summarizer_app/front_page.html')


def summary_page(request, summary_id):
    summary = get_object_or_404(Summary, pk=summary_id)
    return render(request, 'summarizer_app/summary_page.html', {'summary': summary})


def login_redirect(request):
    return redirect('summarizer_app:login')

def redirect_after_login(request):
    next_url = request.GET.get('next', 'summarizer_app:homepage')  # Default to homepage
    return redirect(next_url)


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, 'Registration successful. Please login.')
                return render(request, 'registration/register.html', {'registration_success': True})  # Render the same page with registration success message
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'registration_success': False})


def user_login(request):
    error_displayed = False  # Initialize error_displayed to False by default
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('summarizer_app:homepage')
        else:
            messages.error(request, 'Invalid username or password.')
            error_displayed = True  # Set error_displayed to True only if login attempt fails

    return render(request, 'registration/login.html', {'error_displayed': error_displayed})



def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('summarizer_app:homepage')

def about_us(request):
    return render(request, 'summarizer_app/about_us.html')

def slides(request):
    return render(request, 'summarizer_app/slides.html')

def homepage(request):
    return render(request, 'summarizer_app/homepage.html')

def summary_page(request, summary_id):
    summary = get_object_or_404(Summary, pk=summary_id)
    return render(request, 'summarizer_app/summary_page.html', {'summary': summary})

def home(request):
    return render(request, 'summarizer_app/home.html')

from transformers import T5ForConditionalGeneration, T5Tokenizer
def t5_summarize(original_text, summary_length):
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")

    inputs = tokenizer.encode("summarize: " + original_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=summary_length, length_penalty=2.0, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

from django.contrib.auth.decorators import login_required

@csrf_exempt
def delete_all_history(request):
    if request.method == 'DELETE':
        # Retrieve the authenticated user
        user = request.user

        # Delete all rows associated with the user
        Summary.objects.filter(user=user).delete()

        # Return a success response
        return JsonResponse({'message': 'All history deleted successfully.'})

    # Handle other HTTP methods if necessary
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@login_required
def delete_account(request):
    if request.method == 'DELETE':
        user = request.user
        # Here, perform any additional cleanup or actions before deleting the user
        user.delete()
        # Return a success response
        return JsonResponse({'message': 'Account deleted successfully'})
    else:
        # If the request method is not DELETE, return a method not allowed response
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.shortcuts import get_object_or_404
@csrf_exempt
def delete_history_item(request, history_id):
    if request.method == 'DELETE':
        # Retrieve the history item
        history_item = get_object_or_404(Summary, pk=history_id)
        
        # Check if the logged-in user is the owner of the history item
        if request.user == history_item.user:
            history_item.delete()  # Delete the history item
            return JsonResponse({'message': 'History item deleted successfully'})
        else:
            return HttpResponseForbidden("You don't have permission to delete this history item.")
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

#import our model classes below; made later my tilak;; before we used functional within views.py now using class
from .topic_extractor import TopicExtractor
from .lsa_summarizer import LSASummarizer
from .t5_summarizer import T5Summarizer
from .models import Summary

tfidf_details = None
lsa_summary_details = {}
tfidf_details = {}

# Modify the summarize function
@csrf_exempt
def summarize(request):
    global tfidf_details

    def count_words(text):
        # Use a simple regex to split words
        words = re.findall(r'\b\w+\b', text)
        return len(words)


    def count_sentences(text):
        # Use a regex to split sentences, including commas as part of the sentence ending
        sentences = re.split(r'(?<=[.!?])\s*(?=[A-Z])', text)
        return len(sentences)

    user_history = []

    if request.method == 'GET':
        # Retrieve user history from the database
        # user_history = Summary.objects.filter(user=request.user).values('id', 'input_text', 'short_topic', 'generated_summary')
        user_history = Summary.objects.filter(user=request.user).values('id', 'input_text', 'short_topic', 'summarized_text')
        # print("\n\nuser_histroy completed.\n\n",)
        return JsonResponse(list(user_history), safe=False)

    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        algorithm = request.POST.get('algorithm')
        summary_length = request.POST.get('summary_length')
        summarized_text = request.POST.get('generated_summary')

        # user_history = Summary.objects.filter(user=request.user).values('id', 'input_text', 'short_topic', 'generated_summary')
        # user_history = Summary.objects.filter(user=request.user).values('id', 'input_text', 'short_topic')
        # print("\n\nUser History : ", user_history)
        # if not user_history:
        #     user_history = []  # Empty list if no history found
        #     return JsonResponse(list(user_history), safe=False)

        # print(f"Received data: input_text={input_text}, algorithm={algorithm}, summary_length={summary_length}, generated_summary={generated_summary}")
        

        # **Dynamic Algorithm Selection:**
        algorithms = {
            "T5": t5_summarize,  # Replace with your actual T5 summarization function
            "T5_our": "T5_our",  # Add your function for the fine-tuned T5 model
            "LSA": "LSA",  # Add your LSA summarization implementation
        }

        summarize_function = algorithms.get(algorithm)
        if algorithm == "T5_our":
            summary_length = max(min(int(summary_length), 512), 1)
            # Instantiate the T5Summarizer class
            summarizer = T5Summarizer()
            # Use the summarize method of the T5Summarizer class
            # summarized_text = summarizer.summarize(input_text, int(summary_length))
            summarized_text = summarizer.summarize(input_text, summary_length, max_length=512, length_penalty=2.0, num_beams=4, early_stopping=True)
            # Generate short topic dynamically using TopicExtractor
            topic_extractor = TopicExtractor()
            short_topic = topic_extractor.extract_topics(summarized_text)

            #global tfidf_details
            tfidf_details = topic_extractor.intermediate_results(summarized_text)
        elif summarize_function == "LSA":
            # Create an instance of LSASummarizer and call its summarize method
            lsa_summarizer = LSASummarizer(input_text)

            #below summarized text contains all steps involved in LSA
            summarized_text = lsa_summarizer.summarize(int(summary_length))
            # Generate short topic dynamically using TopicExtractor
            topic_extractor = TopicExtractor()
            short_topic = topic_extractor.extract_topics(summarized_text['formatted_summary'])

            word_count = count_words(summarized_text['formatted_summary'])
            sentence_count = count_sentences(summarized_text['formatted_summary'])
            formatted_sentence = summarized_text['formatted_summary']

            cleantext = summarized_text['clean_text']
            normalizedtext = summarized_text['normalized_text']
            tokenized_sentences = summarized_text['tokenized_sentences']
            tokenized_words = summarized_text['tokenized_words']
            term_document_matrix = summarized_text['term_document_matrix']
            dtm = summarized_text['dtm']
            mean_centered_dtm = summarized_text['mean_centered_dtm']

            covariancematrix = summarized_text['covariance_matrix']
            eigenvalues = summarized_text['eigenvalues'].real.tolist()
            eigenvalues = [str(val) for val in eigenvalues]
            eigenvectors = summarized_text['eigenvectors'].real.tolist()
            eigenvectors = [str(val) for val in eigenvectors]
            sentence_scores = summarized_text['sentence_scores']
            sentence_scores = [str(val) for val in sentence_scores]
            summary_sentences = summarized_text['summary_sentences']

            # print(f"Short Topic: {short_topic}")

            # Save the summarized text, short topic, and other details to the database
            summary = Summary.objects.create(
                user=request.user,
                input_text=input_text,
                algorithm=algorithm,
                summary_length=summary_length,
                summarized_text=summarized_text['formatted_summary'],  # Use summarized_text instead of generated_summary
                short_topic=short_topic
            )

            summary.save()
            print("LSA details are saved to db")

            summary_details = {
                'input_text' : input_text,
                'generated_summary': formatted_sentence,
                'word_count': word_count,
                'sentence_count': sentence_count,
                'short_topic': short_topic,

                'clean_text': cleantext,
                'normalized_text': normalizedtext,
                'tokenized_sentences': tokenized_sentences,
                'tokenized_words': tokenized_words,
                'term_document_matrix': json.dumps(term_document_matrix),
                'dtm': dtm,
                'mean_centered_dtm': mean_centered_dtm,

                'covariance_matrix': covariancematrix.tolist(),

                'eigenvalues': json.dumps(eigenvalues),
                'eigenvectors': json.dumps(eigenvectors),

                'sentence_scores' : sentence_scores,
                'summary_sentences' : summary_sentences,
            }

            global lsa_summary_details
            lsa_summary_details = summary_details

            #global tfidf_details
            tfidf_details = topic_extractor.intermediate_results(summarized_text['formatted_summary'])

            # print('tfidf from views',tfidf_details)

            return JsonResponse(summary_details)

        elif summarize_function:
            summarized_text = summarize_function(input_text, int(summary_length))
            # Generate short topic dynamically using TopicExtractor
            topic_extractor = TopicExtractor()
            short_topic = topic_extractor.extract_topics(summarized_text)

            #global tfidf_details
            tfidf_details = topic_extractor.intermediate_results(summarized_text)
        else:
            return JsonResponse({'error': 'Invalid algorithm'})  # Handle invalid algorithm

        # # Assuming 't5_summarize' is your actual summarization function
        # summarized_text = t5_summarize(input_text, int(summary_length))

        # print(f"Generated Summary: {summarized_text}")

        # print(f"Short Topic: {short_topic}")

        # Save the summarized text, short topic, and other details to the database
        summary = Summary.objects.create(
            user=request.user,
            input_text=input_text,
            algorithm=algorithm,
            summary_length=summary_length,
            summarized_text=summarized_text,  # Use summarized_text instead of generated_summary
            short_topic=short_topic
        )

        summary.save()

        print("\nSummary saved to the database.")

        # Count words and sentences in the summarized text
        word_count = count_words(summarized_text)
        sentence_count = count_sentences(summarized_text)
        print('sentenceeeee count ',sentence_count)

        # Construct a dictionary with the summary details
        summary_details = {
            'generated_summary': summarized_text,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'short_topic': short_topic
        }

        # Return the summary details as JSON response
        return JsonResponse(summary_details)
        # return render(request, 'summarizer_app/home.html', {'summary_details': summary_details, 'user_history': user_history})
        #return render(request, 'summarizer_app/home.html', {'summary_details': summary_details, 'user_history': user_history})

    return JsonResponse({'error': 'Invalid Request'})

def fetch_lsa_summary_details(request):
    global lsa_summary_details
    summary_details = lsa_summary_details
    # print('s_details',summary_details)
    # Return the LSA summary details as a JSON response
    return JsonResponse(summary_details)


def fetch_tfidf_details(request):
    print('fetch_tfidf_details runed')
    global tfidf_details  # Move the global declaration to the top of the function
    return JsonResponse(tfidf_details)
