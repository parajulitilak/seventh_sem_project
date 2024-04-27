# summarizer_app/urls.py
from django.urls import path
from . import views
from summarizer_app.views import homepage,front_page,fetch_lsa_summary_details,fetch_tfidf_details


app_name = 'summarizer_app'

urlpatterns = [
    path('', views.front_page, name='front_page'),
    # path('homepage_new/', views.homepage_new, name='homepage_new'),
    path('about_us/', views.about_us, name='about_us'),
    path('slides/', views.slides, name='slides'),
    path('homepage/', homepage, name='homepage'),  # Set the homepage as the root URL
    path('summarization/', views.home, name='home'),  # Set the summarization task URL
    path('summarization/summarize/', views.summarize, name='summarize'),
    path('summarization/summary/<int:summary_id>/', views.summary_page, name='summary_page'),
    # Add other paths as needed
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get-summary-details/<int:input_text_id>/', views.get_summary_details, name='get_summary_details'),
    # path('fetch-lsa-summary-details', fetch_lsa_summary_details, name='fetch_lsa_summary_details'),
    path('fetch-lsa-summary-details/', fetch_lsa_summary_details, name='fetch_lsa_summary_details'),
    path('fetch-tfidf-details/', fetch_tfidf_details, name='fetch_tfidf_details'),





    # path('restricted/', views.restricted_view, name='restricted'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('redirect_after_login/', views.redirect_after_login, name='redirect_after_login'),
    path('delete-all-history', views.delete_all_history, name='delete_all_history'),
    path('delete-history/<int:history_id>/', views.delete_history_item, name='delete_history_item'),
    path('delete-account/', views.delete_account, name='delete_account'),


    # path('delete-history/<int:history_id>/', views.delete_history_item, name='delete_history_item'),
    
]