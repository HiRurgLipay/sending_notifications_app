import logging
from rest_framework import status
from rest_framework.response import Response
from core.business.services import create_mailing_service, update_mailing_service, delete_mailing_service
from core.presentation.serializers import MailingSerializer
from rest_framework.views import APIView


logger = logging.getLogger(__name__)


class MailingController(APIView):
    def post(self, request):
        data = request.data
        try:
            mailing = create_mailing_service(data)
            logger.info("Mailing created successfully")
            return Response(MailingSerializer(mailing).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Failed to create mailing: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, mailing_id):
        data = request.data
        try:
            updated_mailing = update_mailing_service(mailing_id, data)
            logger.info(f"Mailing with ID {mailing_id} updated successfully")
            return Response(MailingSerializer(updated_mailing).data)
        except Exception as e:
            logger.error(f"Failed to update mailing with ID {mailing_id}: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, mailing_id):
        try:
            delete_mailing_service(mailing_id)
            logger.info(f"Mailing with ID {mailing_id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Failed to delete mailing with ID {mailing_id}: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
