from django.urls import path, include
from .views import *

urlpatterns = [
    # path('basic_info/create/', create_basic_info, name="create_basic_info"),
    path('', application, name="application"),
    path('<pk>/', application_detail, name="application_detail"),
    path('payment/init/<app_id>/', initiate_payment, name="initiate_payment" ),
    path('payment/status/', process_payment_update, name="process_payment_update"),
    path('seat_plan/<pk>/', generate_seat_plan, name="seat_plan")
]