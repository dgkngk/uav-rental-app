from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (login_view, logout_view, home_view,
                    UAVViewSet, rent_uav, signup_view,
                    ApiLoginView, ApiLogoutView, ApiSignupView,
                    return_uav, profile_view, update_rental,
                    api_uav_list, api_uav_list_json)

router = DefaultRouter()
router.register(r'uavs', UAVViewSet)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('rent/<int:uav_id>/', rent_uav, name='rent_uav'),
    path('return/<int:rental_id>/', return_uav, name='return_uav'),
    path('update-rental/<int:rental_id>/', update_rental, name='update_rental'),
    path('', home_view, name='home'),
    path('api/', include(router.urls)),
    path('signup/', signup_view, name='signup'),
    path('api/login/', ApiLoginView.as_view(), name='api-login'),
    path('api/logout/', ApiLogoutView.as_view(), name='api-logout'),
    path('api/signup/', ApiSignupView.as_view(), name='api-signup'),
    path('api/uavs/', api_uav_list, name='api-uavs'),
    path('api/uavs-json/', api_uav_list_json, name='api-uavs-json'),

]
