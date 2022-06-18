from django.urls import path
from . import views 

urlpatterns = [
    path('', views.polls_read,name='home'),
    path('create', views.polls_create,name='create'),
    path('vote/<int:pk>/', views.polls_vote,name='vote'),
    path('result/<int:pk>/', views.polls_result,name='result'),
    path('yet_to_poll', views.polls_yet_to_poll,name='yet_to_poll'),
    path('already_polled', views.polls_already_polled,name='already_polled'),
    path('all_results', views.polls_all_results,name='all_results'),
    path('poll_details/<int:pk>', views.polls_details,name='poll_details'),
    path('poll_update/<int:pk>', views.polls_update,name='poll_update'),
    path('poll_delete/<int:pk>', views.polls_delete,name='poll_delete'),
    path('poll_duplicate/<int:pk>', views.polls_duplicate_polling_restricting,name='poll_duplicate'),
]
