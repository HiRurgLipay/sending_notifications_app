from django.urls import path
from core.presentation.views import ClientController, MailingController, MailingStatisticsView, DetailedMessageStatisticsView


urlpatterns = [
    path('api/clients/add/', ClientController.as_view(), name='create_client'),
    path('api/clients/update/<int:client_id>/', ClientController.as_view(), name='update_client'),
    path('api/clients/delete/<int:client_id>/', ClientController.as_view(), name='delete_client'),

    path('api/mailings/add/', MailingController.as_view(), name='create_mailing'),
    path('api/mailings/update/<int:mailing_id>/', MailingController.as_view(), name='update_mailing'),
    path('api/mailings/delete/<int:mailing_id>/', MailingController.as_view(), name='delete_mailing'),
    
    path('api/mailing/<int:mailing_id>/statistics/', MailingStatisticsView.as_view(), name='mailing_statistics'),
    path('api/mailing/<int:mailing_id>/detailed_statistics/', DetailedMessageStatisticsView.as_view(), name='detailed_message_statistics'),
]
