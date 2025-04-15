from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.messaging_tools.smtp import AutoReply
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.middleware.csrf import get_token
import json
from log.LTBE import logging
import os
from rest_framework import status


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def error_log(request):
	try:
		if request.method == "GET":
			error_log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'error.log')
			try:
				with open(error_log_file_path, 'r') as error_log_file:
					error_log_content = error_log_file.read()
			except FileNotFoundError:
				error_log_content = 'Error log file not found.'

			# Clear the error log file
			open(error_log_file_path, 'w').close()

			# Return JSON response with CSRF token, health status, and error log content
			return JsonResponse({
				'error_log': error_log_content
			})
		else:
			return Response({'error': 'Unsupported method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
	except Exception as e:
		error_logged = f"Error in request: {e}"
		logging.error(error_logged)
		return Response({'error': error_logged}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_and_csrf_token(request):
	# Get CSRF token
	csrf_token = get_token(request)

	# Check health of the application and container
	health_status = {
		'django_app': 'healthy',
		'container': 'healthy' if os.path.exists('/app/') else 'unhealthy'
	}

	# Return JSON response with CSRF token, health status, and error log content
	return JsonResponse({
		'csrf_token': csrf_token,
		'health_status': health_status,
	})
