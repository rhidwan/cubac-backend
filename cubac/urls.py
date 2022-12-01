"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django
from django.contrib import admin
from django.urls import path, include
import user.views as user_view
# import admin_dashboard.views as dashboard_view
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import confirm_email
from django.contrib.auth import urls as auth_urls

def custom_page_not_found(request):
    return django.views.defaults.page_not_found(request, None)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    path('account/registration/verify-email/<str:key>/', confirm_email, name='account_confirm_email'),
    path('authentication/', include('django.contrib.auth.urls')),
    path('login/', user_view.user_login, name="login"),
    path('register', user_view.user_registration, name="register"),
    path('logout/', user_view.user_logout, name="logout"),
    path('change_password/', user_view.change_password, name="change_password"),
    path('update_user/', user_view.update_user_info, name="update_user_info"),
    path('make_staff_account/', user_view.make_staff_account, name="make_staff_account"),
    # path('project/create_account/', user_view.create_account, name="create_account"),
    path('', include('home.urls')),
     path('__debug__/', include('debug_toolbar.urls')),

    path('call/', include('call_applications.urls')),
    path('profile/', include('profiles.urls')),
    path('application/', include('applications.urls')),

    # path('password_reset/', auth_views.password_reset, name='password_reset'),
    # path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    # path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    # path('task/', include('todo.urls')),
    # path('project/', include('project.urls')),
    # path('daily_report/', include('daily_report.urls')),
    # path('callback/', include('callback.urls')),
    # path('installation/', include('installation.urls')),
    # path('report/', include('report.urls')),
    # path('modification/', include('modification.urls')),
    # path('servicing/', include('servicing.urls')),
    # path('callreport/', include('callreport.urls')),
    # path('payment/', include('payment.urls')),
    # path('notifications/', include('notifications.urls', namespace='notifications')),
    # path("404/", custom_page_not_found)   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)