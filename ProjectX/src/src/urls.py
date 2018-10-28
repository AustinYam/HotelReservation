"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from django.contrib.auth import views as auth_views


from HotelReservation import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),
    url(r'^contact/$', views.contact, name='contact'),

    # Registration & Authentication URLs
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'login.html'}, name='logout'),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'password_reset_complete.html'}, name='password_reset_complete'),

    url(r'^hotel-list/$', views.hotellist_view, name='hotel-list'),
    url(r'^result/$', views.search, name='search'),
    url(r'^booking-room/$', views.booking_room_view, name='booking'),
    url(r'^booking-room/(?P<pk>[0-9]+)/$', views.booking_room_view, name='booking_with_pk'),

    url(r'^reservation-detail/(?P<thehotelid>[0-9]+)/(?P<roomsid>[0-9]+)$', views.reservation_detail_view, name='reservation'),
    url(r'^storing/(?P<thehotelid>[0-9]+)/(?P<roomid>[0-9]+)/(?P<checkin>(\d{4}-\d{2}-\d{2}))/(?P<checkout>(\d{4}-\d{2}-\d{2}))/(?P<totalcost>\d+\.\d{2})/$', views.storingData, name='storing'),
    url(r'^confirmation/$', views.confirmation, name='thanks'),
    url(r"^mybooking/$", views.mybooking, name="mybooking"),
    url(r'^mybookings/cancel/(?P<id>[0-9]+)$', views.cancelbooking, name='cancelbooking'),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

# Debug the static file.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
