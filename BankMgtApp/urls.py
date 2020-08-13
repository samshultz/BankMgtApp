from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from bankapp.views import profile, CustomPasswordChangeView
# from two_factor.urls import urlpatterns as tf_urls
from django.contrib.auth.decorators import login_required

admin.site.login = login_required(admin.site.login)


def homepage(request):
    return render(request, "index.html", {})

# def logout_from_all_sessions(request):
#     request.user.session_set.all().delete()

urlpatterns = [
    # path(r'', include(tf_urls)),
    path('', include('allauth_2fa.urls')),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name="account_change_password"),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', profile, name="profile"),
    path('admin/', admin.site.urls),
    path(r'', include('user_sessions.urls', 'user_sessions')),


    path('', homepage, name="homepage"),
]
