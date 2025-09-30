import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, action
from django.conf import settings

# Create your views here.
# ==============================================
@api_view(["GET"])
def gov_data(request):
    dataset = "d_120ad7e0334d2c2a37ad62ae262f75fa"
    url = "https://data.gov.sg/api/action/datastore_search?resource_id="  + dataset

    api_key = getattr(settings, 'DATA_GOV_SG_API_KEY', None)

    if not api_key:
        return Response(
            {"error": "API key not configured"},
            status=500
        )
    
    headers = {"x-api-key": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(response.json())
        return Response(data)
    
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)