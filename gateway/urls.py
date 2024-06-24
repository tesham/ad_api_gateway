from django.urls import re_path
from .views import GatewayApiView

urlpatterns = [
    re_path(r'^(?P<path>.*)$', GatewayApiView.as_view(), name='gateway'),
]