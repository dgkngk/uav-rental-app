from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import UAV, Rental
from .serializers import UAVSerializer, RentalSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly


# utility functions
def get_all_active_uavs(request):
    # Retrieve all uavs that are not rented
    uavs = UAV.objects.all().exclude(is_rented=True)
    # Filter uavs based on search query if query is present
    uav_query = {}
    brand = request.GET.get('brand')
    if brand:
        uav_query['brand__icontains'] = brand
    model = request.GET.get('model')
    if model:
        uav_query['model__icontains'] = model
    weight = request.GET.get('weight')
    if weight:
        uav_query['weight__icontains'] = weight
    category = request.GET.get('category')
    if category:
        uav_query['category__icontains'] = category
    return uavs.filter(**uav_query)


# api views
class ApiLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class ApiLogoutView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        token = request.data.get('token')
        if token:
            try:
                token = Token.objects.get(key=token)
                token.delete()
            except Token.DoesNotExist:
                pass
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiSignupView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_uav_list(request):
    uavs = get_all_active_uavs(request)
    serializer = UAVSerializer(uavs, many=True)
    return Response(serializer.data)


def api_uav_list_json(request):
    uavs = get_all_active_uavs(request)
    serializer = UAVSerializer(uavs, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def make_rental(request):
    serializer = RentalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


class UAVViewSet(viewsets.ModelViewSet):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer
    permission_classes = [IsAdminOrReadOnly]


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAdminOrReadOnly]


# views
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome to UAV Rental App, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(redirect_field_name='next', login_url='login')
def home_view(request):
    # Retrieve all uavs that are not rented
    uavs = get_all_active_uavs(request)
    return render(request, 'home.html', {'active_uavs': uavs})


@login_required
def rent_uav(request, uav_id):
    # Retrieve the UAV object or return a 404 error if not found
    uav = get_object_or_404(UAV, id=uav_id)

    if request.method == 'POST':
        # Process rental request
        Rental.objects.create(user=request.user, uav=uav,
                              rental_start=request.POST.get('start_date'),
                              rental_end=request.POST.get('end_date'),
                              is_active=True)
        uav.is_rented = True
        uav.save()
        messages.success(request, f"You have successfully rented the UAV {uav.brand} - {uav.model}.")
        return redirect('home')  # Redirect to homepage after rental
    return render(request, 'rent_uav.html', {'uav': uav})


@login_required
def return_uav(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    rental.end_date = timezone.now()
    rental.is_active = False
    rental.uav.is_rented = False
    rental.uav.save()
    rental.save()
    messages.success(request, f"The UAV {rental.uav.brand} - {rental.uav.model} has been successfully returned.")
    return redirect('profile')  # Redirect to homepage after returning UAV


@login_required
def update_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date', None)
        if not start_date:
            messages.error(request, 'Please enter a start date.')
            return redirect('profile')
        if not end_date:
            messages.error(request, 'Please enter an end date.')
            return redirect('profile')
        rental.rental_start = start_date
        rental.rental_end = end_date
        rental.save()
        messages.success(request, 'Rental updated successfully.')
        return redirect('profile')  # Redirect back to the profile page
    return redirect('profile')


@login_required
def profile_view(request):
    # Retrieve all rentals
    rented_uavs = Rental.objects.filter(user=request.user, is_active=True)
    # Filter rented UAVs based on search query if query is present
    rental_query = {}
    rental_start_date = request.GET.get('rental_start_date')
    if rental_start_date:
        rental_query['rental_start__gte'] = rental_start_date
    rental_end_date = request.GET.get('rental_end_date')
    if rental_end_date:
        rental_query['rental_end__lte'] = rental_end_date
    if rental_query:
        rented_uavs = rented_uavs.filter(**rental_query)

    return render(request, 'profile.html', {'rented_uavs': rented_uavs})



