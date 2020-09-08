from mainapp import views
from django.urls import path
from django.conf.urls import url

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.contact, name='contact'),
    # path('search/', views.search, name='search'),

    path('mess-service/', views.mes_service_list, name="mes_list"),
    path('mess-service/<location_id>', views.mes_service_list, name="mes_list_by_category"),
    path('mess-details/<int:id>/', views.mes_service_details, name='mes_details'),

    path('tuition-service/', views.tuition_service_list, name="tuition_list"),
    path('tuition-service/<category_id>/', views.tuition_service_list, name="tuition_list_by_category"),
    path('tuition-service-details/<t_id>', views.tuition_service_details, name='tuition_details'),

    path('user-login/', views.custom_login, name='login'),
    path('user-logout/', views.logout_page, name='logout'),

    path('profile/', views.user_dashboard, name="profile"),
    # path('create-profile/', views.create_profile, name='create_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),

    path('create-mes-ad/', views.create_mes_ad, name='create_mes_ad'),
    path('update-mes-ad/<id>/<user_id>', views.update_mes_ad, name='update_mes_ad'),
    path('delete-mes-ad/<id>', views.delete_mes_ad, name='delete_mes_ad'),
    path('accounts/register/', views.user_registration, name='register'),
    path('activate/<uid>/<token>', views.active, name='activate'),

    path('create-tuition-ad/', views.create_tuition_ad, name='create_tuition_ad'),
    path('update-tuition-ad/', views.update_tuition_ad, name='update_tuition_ad'),
    path('delete-tuition-ad/', views.delete_tuition_ad, name='delete_tuition_ad'),

    # path('create-education-status/', views.create_education_status, name='CreateEducationProfile'),
    # path('delete-education-status/<e_id>', views.delete_education_status, name='delete-education-status'),

]
