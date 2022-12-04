from django.urls import path, include
from .views import *

urlpatterns = [
    # path('basic_info/create/', create_basic_info, name="create_basic_info"),
    path('list/', applications, name="applications"),
    path('apply_now/<pk>/', application, name="apply_for_call_application"),
    path('transactions/', list_transaction, name="list_transaction"),
    
    path('transaction/<pk>/', transaction_detail, name="transaction_detail"),
    path('manual/transaction/edit/<pk>/', manual_transaction_edit, name="edit_manual_transaction_detail"),
    
    path('admit_card/', admit_card, name="admit_card"),
    
    path('application_form/generate/async/bulk/<pk>/',generate_bulk_application_form_async, name="generate_bulk_application_form_async" ),
    path('admit_card/generate/async/bulk/<pk>/',generate_bulk_admit_card_async, name="generate_bulk_admit_card_async" ),
    path('admit_card/generate/bulk/<pk>/',generate_bulk_admit_card, name="generate_bulk_admit_card" ),
    path('admit_card/generate/<pk>/',generate_admit_card, name="generate_admit_card" ),
    path('application_form/generate/bulk/<pk>/', generate_bulk_application_form, name="generate_bulk_application_form"),
    path('application_form/generate/<pk>/', generate_application_form, name="generate_application_form"),

    path('task/status/', get_page_request_status, name="get_task_status"),
    path('seat_plan/', seat_plan, name="seat_plan"),
    path('api/', api_application, name="api_application"),
    path('api/<pk>/', api_application_detail, name="api_application_detail"),
    path('payment/init/<app_id>/', initiate_payment, name="initiate_payment" ),
    path('payment/status/', process_payment_update, name="process_payment_update"),
    path('seat_plan/<pk>/', generate_seat_plan, name="seat_plan"),
    path('<pk>/seat_plan/', seat_plan_detail, name="seat_plan_detail" ),
    path('application/<pk>/', application_detail, name="application_detail" ),
    path('<pk>/transaction/', application_transaction, name="application_transaction"),
]