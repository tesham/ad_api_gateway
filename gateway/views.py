from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from api_gateway import settings

class AuthenticatedView(APIView):
    pass


class UnauthenticatedView(APIView):
    permission_classes = ()


class GatewayApiView(AuthenticatedView):

    def get_target_service_url(self, request):
        path = request.path
        url = ''
        if 'auth' in path:
            url = settings.AUTH_SERVICE
        elif 'ip' in path:
            url = settings.IP_SERVICE
        elif 'audit' in path:
            url = settings.AUDIT_SERVICE
        return url + path

    def get_forwarded_headers(self, request):
        # Forward relevant headers including auth headers
        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
        return headers

    def get(self, request, *args, **kwargs):
        target_url = self.get_target_service_url(request)
        headers = self.get_forwarded_headers(request)

        try:
            response = requests.get(target_url, headers=headers, params=request.GET)
            return Response(response.json(), status=response.status_code)
        except Exception as exe:
            return Response(
                dict(
                    message=str(exe)
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        # Determine the target service URL based on request data
        target_url = self.get_target_service_url(request)
        headers = self.get_forwarded_headers(request)
        try:
            # Forward the request to the target service
            response = requests.post(target_url, json=request.data, headers=headers)
            return Response(response.json(), status=response.status_code)
        except Exception as exe:
            return Response(
                dict(
                    message=str(exe)
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )