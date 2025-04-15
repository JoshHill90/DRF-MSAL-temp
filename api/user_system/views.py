from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, TokenSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json
from django.middleware.csrf import get_token
from log.LTBE import logging
from utils.keys import MSAuth
import msal
from django.utils import timezone
from datetime import timedelta, datetime
import requests
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth import get_user_model, login
from .models import MsAuthLink
import pytz
from utils.messaging_tools.security import HexGen

User = get_user_model()

# Azure session token object
def session_token():
    #Create and return an MSAL confidential client application instance.
    authority = MSAuth.AUTHORITY
    client_id = MSAuth.CLIENT_ID
    client_secret = MSAuth.CLIENT_SECRET
    
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=authority,
        client_credential=client_secret,
    )
    return app


def get_or_refresh_access_token(linkage):
    # Check if access token is expired, refresh it if needed, and return the access token.
    
    # Calculate expiry time with offset
    expired_time_offset = timedelta(seconds=linkage.expiry)
    is_expired = linkage.timestamp + expired_time_offset
    
    ny_tz = pytz.timezone('America/New_York')
    # If token is expired, refresh it
    if is_expired < datetime.now(tz=ny_tz):
        print("Token expired, refreshing")
        # Token has expired, use refresh token to get a new one
        msal_app = session_token()

        result = msal_app.acquire_token_by_refresh_token(
            linkage.refresh_key,
            scopes=MSAuth.SCOPE
        )
        
        # Update the stored access_token and refresh_token
        new_access_token = result["access_token"]
        new_refresh_token = result["refresh_token"]
        linkage.key = new_access_token
        linkage.refresh_key = new_refresh_token
        linkage.expiry = result["expires_in"]
        linkage.save()

        return linkage.key
    
    # Token is still valid
    return linkage.key


# Initial endpoint that calls MS for OAuth flow
def auth_page(request):
    """Redirect to the Microsoft login page for OAuth authentication."""
    try:
        msal_app = session_token()

        # Create the authorization URL
        auth_url = msal_app.get_authorization_request_url(
            scopes=MSAuth.SCOPE,  
            redirect_uri=request.build_absolute_uri(reverse("getAToken")) 
        )
        # Redirect to MS login
        return redirect(auth_url)

    except Exception as e:
        return Response({"status": "failed", "message": str(e)}, status=400)


# Validates access token from MS and passes session token to the frontend
# Used to log the user in or create a new user for unrecognized emails
def redirect_auth(request):
    
    try:
        msal_app = session_token()

        # Retrieve the authorization code from the query parameters
        code = request.GET.get('code')
        if not code:
            return Response({"status": "failed", "message": "Authorization code not found."}, status=400)

        # Acquire token by authorization code
        result = msal_app.acquire_token_by_authorization_code(
            code=code,
            scopes=MSAuth.SCOPE,
            redirect_uri=request.build_absolute_uri(reverse("getAToken"))
        )

        access_token = result["access_token"]
        refresh_token = result["refresh_token"]
        username = result["id_token_claims"]["preferred_username"]

        # Fetch or create the user
        try: 
            is_user = User.objects.get(username=username)
        except User.DoesNotExist:
            is_user = None

        # If the user has accessed the app previously
        if is_user:
            # Clean up old linkage
            MsAuthLink.objects.filter(user=is_user).delete()
            # Create new linkage
            new_linkage = MsAuthLink.objects.create(
                user=is_user,
                expiry=result["expires_in"],
                key=access_token,
                refresh_key=refresh_token,
                temp_token=HexGen().hex_16()
            )
        # First time accessing the app, create a new user
        else:
            valid_user, created = User.objects.create(username=username)
            # Create new linkage
            new_linkage = MsAuthLink.objects.create(
                user=valid_user,
                expiry=result["expires_in"],
                key=access_token,
                refresh_key=refresh_token,
                temp_token=HexGen().hex_16()
            )

        if "error" in result:
            return Response({"status": "failed", "message": result.get("error_description")}, status=400)

        return redirect(f"http://localhost:5173/site/index.html?token={new_linkage.temp_token}")

    except Exception as e:
        return Response({"status": "failed", "message": str(e)}, status=400)


@api_view(['POST'])
def validate_access(request):
    """Validate the access token and log the user in, returning CSRF and session tokens."""
    query_token = request.GET.get('token', '')
    if query_token == "":
        return Response({"status": "failed", "message": "empty token"}, status=400)
    
    try:
        # Find the linkage using the temporary token
        linkage = MsAuthLink.objects.get(temp_token=query_token)

        # Log the user in
        login(request, linkage.user, backend='django.contrib.auth.backends.ModelBackend')
        token, created = Token.objects.get_or_create(user=linkage.user)

        # Generate CSRF token
        csrf_token = get_token(request)
        return Response(data=json.dumps({"token": token.key, "csrf_token": csrf_token}))
    
    except MsAuthLink.DoesNotExist:
        return Response({"status": "failed", "message": "Invalid token"}, status=404)

    except Exception as e:
        return Response({"status": "failed", "message": str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def user_validation(request):
    """Validate the user and retrieve their Microsoft profile data."""
    try:
        token = request.headers.get('Authorization')

        # Get the token from the Authorization header
        if token.startswith('Bearer '):
            token = token.split(' ')[1]

        validating_token = Token.objects.get(key=token)

        # Get or refresh the access token
        linkage = MsAuthLink.objects.get(user=validating_token.user)
        access_token = get_or_refresh_access_token(linkage)

        # Make a request to Microsoft Graph API
        api_result = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={'Authorization': 'Bearer ' + access_token},
            timeout=30,
        ).json()

        return Response(data=api_result, status=status.HTTP_200_OK)

    except Token.DoesNotExist:
        return Response({"status": "failed", "message": "Invalid token"}, status=404)

    except MsAuthLink.DoesNotExist:
        return Response({"status": "failed", "message": "User not linked"}, status=404)

    except Exception as e:
        return Response({"status": "failed", "message": str(e)}, status=400)
