from django.urls import path, include
from django.contrib import admin
from users import views
from users.views import add_user, delete_user, edit_user, get_client_data, get_client_statut_data, get_routes_data, get_user_data, home, search_user, users, routes, promotions, devices
from users.views import( home, users, routes, promotions, devices, get_target,
    add_route, edit_route, delete_route, affectation_routes_users,
    load_devices, assign_user_to_route, assign_client_to_route,
    get_routes, get_route_clients, affectation_clients_routes, search_baskets, assign_promotions,add_basket, define_basket, load_entities,assign_entity)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', home, name='home'),
    path('routes/', routes, name='routes'),
    path('routes/add/', add_route, name='add_route'),
    path('routes/edit/<int:route_id>/', edit_route, name='edit_route'),
    path('routes/delete/<int:route_id>/', delete_route, name='delete_route'),
    path('routes/affectation-routes-users/', affectation_routes_users, name='affectation_routes_users'),
    path('routes/affectation-routes-users/', assign_user_to_route, name='assign_user_to_route'),
    path('promotions/search_baskets/', views.search_baskets, name='search_baskets'),
    path('promotions/get_basket/<int:basket_id>/', views.get_basket, name='get_basket'),
    path('routes/get-routes/', views.get_routes, name='get_routes'),
    path('routes/get-route-clients/', views.get_route_clients, name='get_route_clients'),
    path('routes/assign-client-to-route/', views.assign_client_to_route, name='assign_client_to_route'),
    path('routes/affectation-clients-routes/', views.affectation_clients_routes, name='affectation_clients_routes'),
    path('routes/<int:route_id>/data/', get_routes_data, name='get_routes_data'), 
    
    
    
    path('promotions/', promotions, name='promotions'),
    path('promotions/assign_promotions', assign_promotions, name='assign_promotions'),
    path('promotions/load_entities/', views.load_entities, name='load_entities'),
    path('promotions/assign_entity/', views.assign_entity, name='assign_entity'),
    path('promotions/define_basket/', views.define_basket, name='define_basket'),
    path('promotions/add_basket/', views.add_basket, name='add_basket'),

    path('promotions/create/', views.create_promotion, name='create_promotion'),
    path('promotions/get/<int:promotion_id>/', views.get_promotion, name='get_promotion'),
    path('promotions/edit/', views.edit_promotion, name='edit_promotion'),
    path('promotions/delete/', views.delete_promotion, name='delete_promotion'),
    path('promotions/update_checkbox/', views.update_checkbox, name='update_checkbox'),



    path('devices/', devices, name='devices'),
    path('devices/load/', load_devices, name='load_devices'),


    path('client/<int:client_id>/', views.clients, name='Clients'),
    path('client/', views.clients, name='Clients'),
    path('clients/<str:client_id>/edit/', views.edit_client, name='edit_client'),
    path('client/home_client/', views.home_client, name='home_client'),
    path('clients/<str:Client_Code>/delete/', views.delete_client, name='delete_client'),
    path('search_client/', views.search_client, name='search_client'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('clients/<str:client_id>/data/', get_client_data, name='get_client_data'),



    path('client/statut_Add/', views.statut_client, name='client_status'),
    path('client_status/<int:client_statut_id>/edit/', views.edit_statut_client, name='edit_statut_client'),
    path('client/home_client_status/', views.home_client_status, name='home_client_status'),
    path('client/<int:client_statut_id>/data/', views.get_client_statut_data, name='get_client_statut_data'),

    


    path('client/home_client_discount/', views.home_client_discounts, name='home_discounts'),
    path('client/client_discounts/', views.client_discounts, name='client_discounts'),
    path('client_discounts/<str:Client_Code>/edit/', views.edit_client_discounts, name='client_discounts_edit'),
    path('client_discounts/<str:Client_Code>/delete/', views.delete_discounts, name='delete_discounts'),
    path('upload_excel_discount/', views.upload_excel_discount, name='upload_excel_discount'),
    path('delete-selected-clients/', views.delete_selected_clients, name='delete_selected_clients'),
    path('search_client_discount/', views.search_client_discount, name='search_client_discount'),
    path('clientDiscount/<str:client_Code>/data/', views.get_client_Discount_data, name='get_client_Discount_data'),


    
    path('client/home_client_target/', views.home_client_target, name='home_target'),
    path('client/client_target/', views.client_target, name='client_target'),
    path('client_target/<str:Client_Code>/edit/', views.edit_client_target, name='client_target_edit'),
    path('client_target/<str:Client_Code>/delete/', views.delete_target, name='delete_target'),
    path('client_target/<str:Client_Code>/data/', views.get_target, name='get_target'),



    path('channels/Add/', views.channels, name='channels'),
    path('modifier_channel/<str:channel_code>/edit/', views.edit_channel, name='edit_channel'),
    path('channels/home_channel/', views.home_channel, name='home_channel'),
    path('channel/<str:channel_code>/delete/', views.delete_channel, name='delete_channel'),
    path('channel/<str:channel_code>/data/', views.get_channel_data, name='get_channel_data'),



    path('users/', users, name='users'),
    path('add_user/', add_user, name='add_user'),
    path('delete_user/<str:UserCode>/', delete_user, name='delete_user'),
    path('search/', views.search_user, name='search_user'),
    path('users/<str:UserCode>/data/', views.get_user_data, name='get_user_data'),
    path('users/<str:UserCode>/edit/', views.edit_user, name='edit_user'),





]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)