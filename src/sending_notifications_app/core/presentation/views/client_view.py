import logging

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from core.business.services import create_client_service, update_client_service, delete_client_service
from core.presentation.serializers import ClientSerializer

# Настройка логгера
logger = logging.getLogger(__name__)

class ClientController(APIView):
    def post(self, request):
        data = request.data
        try:
            client = create_client_service(data)
            logger.info("Client created successfully")
            return JsonResponse(ClientSerializer(client).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Failed to create client: {e}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, client_id):
        data = request.data
        try:
            updated_client = update_client_service(client_id, data)
            logger.info(f"Client with ID {client_id} updated successfully")
            return JsonResponse(ClientSerializer(updated_client).data)
        except Exception as e:
            logger.error(f"Failed to update client with ID {client_id}: {e}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, client_id):

        try:
            delete_client_service(client_id)
            logger.info(f"Client with ID {client_id} deleted successfully")
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Failed to delete client with ID {client_id}: {e}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
