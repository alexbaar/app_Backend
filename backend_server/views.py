# Import necessary modules and classes

from .models import Users, warehouse, acc_details, messages
from .serializers import UserSerializer, AccDetailsSerializer, MessagesSerializer
from .forms import UserCreationForm,SignUpForm,LoginForm
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .auth_form_serializers import LoginSerializer, SignupSerializer
from django.http import JsonResponse
from .models import Users
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm  
from django.shortcuts import redirect
from .auth_form_serializers import LoginSerializer, SignupSerializer
from rest_framework.exceptions import ValidationError
from .models import warehouse  
from django.http import JsonResponse
from .models import warehouse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import warehouse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    return render(request, "home.html")

def redirect_home(request):
    return render(request, "redirect_home.html")



# View to handle GET, PUT, and DELETE requests for a specific user
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, email):
    user = acc_details.objects.get(email=email)

    if request.method == 'GET':
        # Retrieve details of a specific user
        serializer = AccDetailsSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Update details of a specific user
        data = request.data
        # Remove username from the update data
        serializer = AccDetailsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # Return errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        # Delete a specific user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#get specific user details
@api_view(['GET'])
def get_user_details(request, emaill, format=None):
    try:
        user = acc_details.objects.get(email=emaill)
    except acc_details.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Retrieve details of a specific user
        serializer = AccDetailsSerializer(user)
        return Response(serializer.data)


# View for user signup using SignupSerializer
def signup(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.POST)
        if serializer.is_valid():
            # Perform actions for valid signup data, like creating a new user
            return redirect('login')
    else:
        serializer = SignupSerializer()
    return render(request, 'signup.html', {'serializer': serializer})



@api_view(['POST'])
def login(request, format=None):
    if request.method == 'POST':
        fetched_email = request.data.get("email")
        fetched_password = request.data.get("password")

        fetched = warehouse.objects.filter(email=fetched_email).exists()
        if fetched:
            user = warehouse.objects.get(email=fetched_email)

            if fetched_password != user.password:
                print("incorrect password ")
                return Response({"message": "incorrect password"}, status=202)
            else:
                return JsonResponse({'email': user.email, 'id': user.id})
        else:
            return Response("This username does not exist in the warehouse records.", status=203)



        
    elif request.method == 'GET':
        # Render the signup form for GET requests
        return render(request, 'login.html')


    # if request.method == 'POST':

    #     fetched_username = request.data.get("username")
    #     fetched_password = request.data.get("password")

    #     print(fetched_username)
    #     print(fetched_password)


    #     # Optionally, return a response indicating success or any other necessary data
    #     return Response({"message": "Data logged in successfully"}, status=201)


#  test_take_input to use the warehouse model
@api_view(['POST', 'GET'])
def test_take_input(request, format=None):
    if request.method == 'POST':
        fetched_email = request.data.get("email")
        fetched_username = request.data.get("user")
        fetched_password = request.data.get("password")

        email_is_exist = warehouse.objects.filter(email=fetched_email).exists()
        username_is_exist = warehouse.objects.filter(username=fetched_username).exists()

        if email_is_exist:
            return Response("This email already exists in the warehouse records.", status=203)
        elif username_is_exist:
            return Response("This username already exists in the warehouse records.", status=203)
        else:
            input_into_db = warehouse(email=fetched_email, username=fetched_username, password=fetched_password)
            input_into_db.save()
            # Optionally, return a response indicating success or any other necessary data
            return redirect('home')
    elif request.method == 'GET':
        # Render the signup form for GET requests
        return render(request, 'signup.html')

    
    
#  user_list to retrieve users from the warehouse model
@api_view(['GET', 'POST'])
def user_list(request, format=None):
    if request.method == 'GET':
        # Retrieve all users from the warehouse model
        users = acc_details.objects.all()
        # Serialize all users
        serializer = AccDetailsSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Create a new user in the warehouse model
        serializer = AccDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#                                   HELP MESSAGES

# Create 
@api_view(['POST'])
def message_create(request, format=None):
    if request.method == 'POST':
        # Create a new message
        serializer = MessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




@api_view(['POST'])
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = warehouse.objects.get(email=email)
            if user.password == password:
                request.session['email'] = user.email
                request.session['id'] = user.id  # Start the session with user email
                return Response({
                    'message': 'Login successful',
                    'email': user.email,
                    'id': user.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        except warehouse.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



    


@api_view(['DELETE', 'GET'])
@csrf_exempt
def delete_user(request, id,format=None):
    if request.method == 'GET':
        # Extract password from the request data
        user_password = request.GET.get('password')

        try:
            # Get the user instance. Adjust this if your user reference is different.
            user = warehouse.objects.get(pk=id)
            #print(user_password)
            print(user_password)
            # Authenticate the user to check if the password is correct
            if (user.password == user_password):
                # Delete the user if authentication is successful
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                # Return 403 Forbidden if the password is incorrect
                return Response(status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            # Return 404 Not Found if the user does not exist
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        # This else part is technically unnecessary since @api_view restricts to DELETE only
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    