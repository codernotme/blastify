from django.urls import path
from .views import process_file
from .views import send_messages

urlpatterns = [
    path('process-file/', process_file, name='process_file'),
    path('send-messages/', send_messages, name='send_messages'),
]
