from django.urls import path, include
from django.contrib import admin
from users import views
from users.views import add_existing_product_to_basket, add_user, delete_user, edit_user, get_client_data, get_client_statut_data, get_routes_data, get_user_data, home, search_user, users, routes, promotions
from users.views import( home, users, routes, promotions, get_target,
    add_route, edit_route, delete_route, affectation_routes_users, assign_user_to_route, assign_client_to_route,
    get_routes, get_route_clients, affectation_clients_routes,add_basket, define_basket)
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
    path('routes/assign_user_to_route/', assign_user_to_route, name='assign_user_to_route'),
    path('routes/get-routes/', views.get_routes, name='get_routes'),
    path('routes/get-route-clients/', views.get_route_clients, name='get_route_clients'),
    path('routes/assign-client-to-route/', views.assign_client_to_route, name='assign_client_to_route'),
    path('routes/affectation-clients-routes/', views.affectation_clients_routes, name='affectation_clients_routes'),
    path('routes/<int:route_id>/data/', get_routes_data, name='get_routes_data'), 
    
    
    
    path('promotions/', promotions, name='promotions'),


    path('promotions/define_basket/', views.define_basket, name='define_basket'),
    path('promotions/add_basket/', views.add_basket, name='add_basket'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_product_to_basket/<int:basket_id>/', views.add_product_to_basket, name='add_product_to_basket'),
    path('view_products/<int:basket_id>/', views.view_products, name='view_products'),
    path('add_existing_product_to_basket/<int:item_basket_id>/', add_existing_product_to_basket, name='add_existing_product_to_basket'),
    path('delete_product/<int:item_basket_id>/<int:product_id>/', views.delete_existing_product , name="deleteProduct"),
    
    
    
    path('promotions/<int:promotion_id>/edit/', views.edit_promotion, name='edit_promotion'),
    path('promotions/delete/<int:promotion_id>/', views.delete_promotion, name='delete_promotion'),
    path('promotions/<int:promotion_id>/data/', views.get_promotion_data, name='get_promotion_data'),
    path('create_promotion/', views.create_promotion, name='create_promotion'),
    path('promotions/<int:promotion_id>/details/', views.get_promotion_details, name='get_promotion_details'),




    path('promotions/', views.promotions_list, name='promotions_list'),
    path('promotions/<int:promotion_id>/clients/', views.get_promotion_clients, name='get_promotion_clients'),
    path('promotions/assign_client/', views.assign_client_to_promotion, name='assign_client_to_promotion'),


    path('devices/home_device/', views.home_device, name='devices'),
    path('devices/', views.list_devices, name='list_devices'),
    path('devices/add/', views.add_device, name='add_device'),
    path('devices/<str:device_serial>/edit/', views.edit_device, name='edit_device'),
    path('devices/<str:device_serial>/remove/', views.remove_device_from_user, name='remove_device_from_user'),
    path('devices/<str:device_serial>/data/', views.get_device_data, name='get_device_data'),



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


    path('users/data/', views.get_users, name='get_users'),

    path('users/', users, name='users'),
    path('add_user/', add_user, name='add_user'),
    path('users/<str:UserCode>/delete/', views.delete_user, name='delete_user'),
    path('search/', views.search_user, name='search_user'),
    path('users/<str:UserCode>/data/', views.get_user_data, name='get_user_data'),
    path('users/<str:UserCode>/edit/', views.edit_user, name='edit_user'),


    path('groupes/', views.home_groupe, name='home_groupe'),
    path('groupes/add/', views.add_groupe, name='add_groupe'),
    path('groupes/<str:Code_groupe>/edit/', views.edit_groupe, name='edit_groupe'),
    path('groupes/<str:Code_groupe>/delete/', views.delete_groupe, name='delete_groupe'),
    path('groupes/<str:Code_groupe>/data/', views.get_group_data, name='get_group_data'),



]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)