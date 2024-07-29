from django.utils import timezone
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import openpyxl
from .models import Channels, Client_Statut, Client_Target, Device, InternalUser, CustomUser, Routes, Clients,PromoItemBasketHeaders,PromoHeaders,Client_Discounts, UserGroupe
from .forms import ChannelsForm, Client_TargetForm, DeviceForm, PromotionSearchForm, NewPromotionForm, RouteForm, UserForm, AssignPromotionSearchForm, BasketForm, UserGroupeForm, client_discountsForm, client_statutForm, clientForm
from django.views.decorators.http import require_GET
from django.core import serializers
from django.db.utils import DatabaseError
from django.db.models import Q
from django.template.loader import render_to_string


import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home/home.html')

@login_required
def edit_route(request, route_id):
    if request.method == 'POST':
        route_description = request.POST.get('route_description')
        region_code = request.POST.get('region_description')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Routes
                SET Route_Description = %s, Region_Code = %s
                WHERE Route_ID = %s
            """, [route_description, region_code, route_id])

        messages.success(request, 'Route updated successfully.')
        return redirect('routes')



'''@login_required
def edit_user(request, user_code):
    if request.method == 'POST':
        # Get the data from the form
        user_name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_number')
        grouping = request.POST.get('grouping')
        is_blocked = request.POST.get('is_blocked')
        login_name = request.POST.get('login_name')
        area_code = request.POST.get('area_code')
        city_id = request.POST.get('city_id')
        route_code = request.POST.get('route_code')
        parent_code = request.POST.get('parent_code')

        try:
            with connection.cursor() as cursor:
                # Execute the update query
                cursor.execute("""
                    UPDATE users
                    SET UserName = %s,
                        PhoneNumber = %s,
                        Grouping = %s,
                        IsBlocked = %s,
                        LoginName = %s,
                        AreaCode = %s,
                        CityID = %s,
                        RouteCode = %s,
                        ParentCode = %s
                    WHERE UserCode = %s
                """, [
                    user_name, phone_number, grouping, is_blocked,
                    login_name, area_code, city_id, route_code,
                    parent_code, user_code
                ])

            # If no exceptions were raised, display a success message
            messages.success(request, 'User updated successfully.')
        except Exception as e:
            # Log the error if needed and display an error message
            messages.error(request, f'Error updating user: {str(e)}')

        # Redirect to the users list page
        return redirect('users')

    # If not a POST request, render the form with the current user data
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT UserName, PhoneNumber, Grouping, IsBlocked, LoginName, AreaCode, CityID, RouteCode, ParentCode
                FROM users
                WHERE UserCode = %s
            """, [user_code])
            user = cursor.fetchone()

        # Check if user exists
        if not user:
            messages.error(request, 'User not found.')
            return redirect('users')

        # Prepare the user data to render the form
        user_data = {
            'user_code': user_code,
            'user_name': user[0],
            'phone_number': user[1],
            'grouping': user[2],
            'is_blocked': user[3],
            'login_name': user[4],
            'area_code': user[5],
            'city_id': user[6],
            'route_code': user[7],
            'parent_code': user[8],
        }

        return render(request, 'users/edit_user.html', {'user': user_data})


def users(request):
    # Extract query parameters from the request
    user_code = request.GET.get('user_code', '').strip()
    user_name = request.GET.get('user_name', '').strip()
    phone_number = request.GET.get('phone_number', '').strip()
    type_user = request.GET.get('type_user', '').strip()

    # Initialize base query
    query = """
        SELECT UserCode, UserName, PhoneNumber, ug.Grouping, IsBlocked,
               LoginName, AreaCode, CityID, RouteCode, ParentCode
        FROM users u
        LEFT JOIN User_Groups ug ON u.Grouping = ug.Grouping
        WHERE 1=1
    """

    # Add conditions to the query based on the provided parameters
    if user_code:
        query += f" AND UserCode LIKE '%{user_code}%'"

    if user_name:
        query += f" AND UserName LIKE '%{user_name}%'"

    if phone_number:
        query += f" AND PhoneNumber LIKE '%{phone_number}%'"

    if type_user:
        query += f" AND Grouping = '{type_user}'"

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query)
        users_data = cursor.fetchall()

    # Prepare the users list
    users_list = [{
        'UserCode': row[0],
        'UserName': row[1],
        'PhoneNumber': row[2],
        'Grouping': row[3],
        'IsBlocked': row[4],
        'LoginName': row[5],
        'AreaCode': row[6],
        'CityID': row[7],
        'RouteCode': row[8],
        'ParentCode': row[9],
    } for row in users_data]

    # Render the template with the filtered users
    return render(request, 'users/home.html', {'users': users_list})



def user_parameters(request, user_code):
    try:
        print(f"Fetching parameters for user code: {user_code}")

        # Query to fetch all parameters with default values
        sql_query_all_params = """
            SELECT ID, ParameterName, DefaultValue
            FROM Parameters
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query_all_params)
            all_parameters_data = cursor.fetchall()

        # Create a dictionary for all parameters with default values
        all_parameters = {row[1]: {'ParameterName': row[1], 'ParameterValue': row[2], 'DefaultValue': row[2]} for row in all_parameters_data}

        # Query to fetch user-specific parameters
        sql_query_user_params = """
            SELECT up.ParameterName, up.ParameterValue
            FROM User_Parameters up
            WHERE up.UserCode = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query_user_params, [user_code])
            user_parameters_data = cursor.fetchall()

        # Update the parameters with user-specific values
        for param_name, param_value in user_parameters_data:
            if param_name in all_parameters:
                all_parameters[param_name]['ParameterValue'] = param_value

        # Convert dictionary back to list for JSON response
        user_parameters = list(all_parameters.values())

        return JsonResponse(user_parameters, safe=False)
    except Exception as e:
        print(f"Error fetching user parameters: {e}")
        return JsonResponse({'error': str(e)}, status=500)
def user_parameters(request, user_code):
    try:
        # Query to fetch all parameters with default values
        sql_query_all_params = """
            SELECT ID, ParameterName, DefaultValue
            FROM Parameters
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query_all_params)
            all_parameters_data = cursor.fetchall()

        # Create a dictionary for all parameters with default values
        all_parameters = {row[1]: {'ParameterName': row[1], 'ParameterValue': row[2], 'DefaultValue': row[2]} for row in all_parameters_data}

        # Query to fetch user-specific parameters
        sql_query_user_params = """
            SELECT up.ParameterName, up.ParameterValue
            FROM User_Parameters up
            WHERE up.UserCode = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query_user_params, [user_code])
            user_parameters_data = cursor.fetchall()

        # Update the parameters with user-specific values
        for param_name, param_value in user_parameters_data:
            if param_name in all_parameters:
                all_parameters[param_name]['ParameterValue'] = param_value

        # Convert dictionary back to list for JSON response
        user_parameters = list(all_parameters.values())

        return JsonResponse(user_parameters, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# View to save user details'''
'''@csrf_exempt
def save_user(request):
    if request.method == 'POST':
        user_code = request.POST.get('UserCode')
        user_name = request.POST.get('UserName')
        phone_number = request.POST.get('PhoneNumber')
        grouping = request.POST.get('Grouping')
        is_blocked = request.POST.get('IsBlocked')
        login_name = request.POST.get('LoginName')
        area_code = request.POST.get('AreaCode')
        city_id = request.POST.get('CityID')
        route_code = request.POST.get('RouteCode')
        parent_code = request.POST.get('ParentCode')

        user, created = InternalUser.objects.update_or_create(
            UserCode=user_code,
            defaults={
                'UserName': user_name,
                'PhoneNumber': phone_number,
                'Grouping': grouping,
                'IsBlocked': is_blocked,
                'LoginName': login_name,
                'AreaCode': area_code,
                'CityID': city_id,
                'RouteCode': route_code,
                'ParentCode': parent_code,
            }
        )

        return JsonResponse({'status': 'success', 'created': created})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def list_users(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT UserCode, UserName, PhoneNumber, Grouping, IsBlocked,
                   LoginName, AreaCode, CityID, RouteCode, ParentCode
            FROM users
        """)
        users_data = cursor.fetchall()

    users_list = []
    for row in users_data:
        user = {
            'UserCode': row[0],
            'UserName': row[1],
            'PhoneNumber': row[2],
            'Grouping': row[3],
            'IsBlocked': row[4],
            'LoginName': row[5],
            'AreaCode': row[6],
            'CityID': row[7],
            'RouteCode': row[8],
            'ParentCode': row[9],
        }
        users_list.append(user)

    return render(request, 'list_users.html', {'users': users_list})

def fetch_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT UserCode, UserName FROM Users")
        rows = cursor.fetchall()
    users = [{'UserCode': row[0], 'UserName': row[1]} for row in rows]
    return users'''

def get_users(request):
    users = InternalUser.objects.all().values('UserCode', 'UserName', 'CityID')
    return JsonResponse({'users': list(users)})



# User login view for customers (authentication)
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# User logout view
def user_logout(request):
    logout(request)
    return redirect('home')


def promotions(request):
    form = PromotionSearchForm(request.GET or None)
    params = {}
    query = """
        SELECT 
            Promotion_ID, 
            Promotion_Description, 
            Promotion_Type, 
            Start_Date, 
            End_Date, 
            Is_Forced, 
            Is_Active, 
            Priority, 
            Promotion_Apply
        FROM 
            Promo_Headers
        WHERE 1=1
    """

    if request.GET:
        if form.is_valid():
            promotion_id = form.cleaned_data.get('promotion_id')
            promotion_description = form.cleaned_data.get('promotion_description')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if promotion_id:
                query += " AND Promotion_ID = %(promotion_id)s"
                params['promotion_id'] = promotion_id

            if promotion_description:
                query += " AND Promotion_Description LIKE %(promotion_description)s"
                params['promotion_description'] = f"%{promotion_description}%"

            if start_date:
                query += " AND Start_Date >= %(start_date)s"
                params['start_date'] = start_date

            if end_date:
                query += " AND End_Date <= %(end_date)s"
                params['end_date'] = end_date

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        promotions = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'form': form,
        'promotions': promotions
    }

    return render(request, 'promotions/home.html', context)
def create_promotion(request):
    if request.method == 'POST':
        form = NewPromotionForm(request.POST)
        if form.is_valid():
            promotion_description = form.cleaned_data['promotion_description']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            priority = form.cleaned_data['priority']
            max_applied = form.cleaned_data['max_applied']
            is_active = form.cleaned_data['is_active']
            is_forced = form.cleaned_data['is_forced']
            promotion_type = form.cleaned_data['promotion_type']
            promotion_apply = form.cleaned_data['promotion_apply']

            query = """
                INSERT INTO Promo_Headers (
                    Promotion_Description,
                    Start_Date,
                    End_Date,
                    Priority,
                    Is_Active,
                    Is_Forced,
                    Promotion_Type,
                    Promotion_Apply
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = [
                promotion_description,
                start_date,
                end_date,
                priority,
                is_active,
                is_forced,
                promotion_type,
                promotion_apply
            ]
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection

def assign_promotions(request):
    form = AssignPromotionSearchForm(request.GET or None)
    params = {}
    query = """
        SELECT 
            Promotion_ID, 
            Promotion_Description, 
            Start_Date, 
            End_Date
        FROM 
            Promo_Headers
        WHERE 1=1
    """

    if request.GET:
        if form.is_valid():
            promotion_type = form.cleaned_data.get('promotion_type')
            search_date = form.cleaned_data.get('search_date')

            if promotion_type:
                query += " AND Promotion_Type = %(promotion_type)s"
                params['promotion_type'] = promotion_type

            if search_date:
                query += " AND %(search_date)s BETWEEN Start_Date AND End_Date"
                params['search_date'] = search_date

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        promotions = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'form': form,
        'promotions': promotions,
    }
    return render(request, 'promotions/assign_promotions.html', context)

def load_entities(request):
    promotion_id = request.GET.get('promotion_id')
    filter_type = request.GET.get('filter_type')
    available_entities = []
    assigned_entities = []

    if filter_type == 'users':
        available_query = """
            SELECT UserCode, UserName
            FROM Users
            WHERE UserCode NOT IN (
                SELECT UserCode
                FROM Promo_Assignments
                WHERE Promotion_ID = %s
            )
        """
        assigned_query = """
            SELECT u.UserCode, u.UserName
            FROM Users u
            JOIN Promo_Assignments up ON u.UserCode = up.UserCode
            WHERE up.Promotion_ID = %s
        """
    elif filter_type == 'clients':
        available_query = """
            SELECT Client_Code, Client_Description
            FROM Clients
            WHERE Client_Code NOT IN (
                SELECT Client_Code
                FROM Promo_Assignments
                WHERE Promotion_ID = %s
            )
        """
        assigned_query = """
            SELECT c.Client_Code, c.Client_Description
            FROM Clients c
            JOIN Promo_Assignments cp ON c.Client_Code = cp.Client_Code
            WHERE cp.Promotion_ID = %s
        """

    with connection.cursor() as cursor:
        cursor.execute(available_query, [promotion_id])
        available_entities = cursor.fetchall()

        cursor.execute(assigned_query, [promotion_id])
        assigned_entities = cursor.fetchall()

    available_html = ""
    assigned_html = ""

    if filter_type == 'users':
        available_html += """
            <tr>
                <th>User Code</th>
                <th>User Name</th>
            </tr>
        """
        assigned_html += """
            <tr>
                <th>User Code</th>
                <th>User Name</th>
            </tr>
        """
    elif filter_type == 'clients':
        available_html += """
            <tr>
                <th>Client Code</th>
                <th>Client Description</th>
            </tr>
        """
        assigned_html += """
            <tr>
                <th>Client Code</th>
                <th>Client Description</th>
            </tr>
        """

    for entity in available_entities:
        available_html += f"<tr><td>{entity[0]}</td><td>{entity[1]}</td></tr>"

    for entity in assigned_entities:
        assigned_html += f"<tr><td>{entity[0]}</td><td>{entity[1]}</td></tr>"

    return JsonResponse({
        'available': available_html,
        'assigned': assigned_html
    })

@csrf_exempt
def assign_entity(request):
    if request.method == 'POST':
        try:
            entity_id = request.POST.get('entity_id')
            promotion_id = request.POST.get('promotion_id')
            filter_type = request.POST.get('filter_type')
            action = request.POST.get('action')

            if not entity_id or not promotion_id or not filter_type or not action:
                return JsonResponse({'error': 'Missing parameters'}, status=400)

            with connection.cursor() as cursor:
                if filter_type == 'users' and action == 'assign':
                    cursor.execute("""
                        INSERT INTO Promo_Assignments (Promotion_ID, UserCode)
                        VALUES (%s, %s)
                    """, [promotion_id, entity_id])
                elif filter_type == 'users' and action == 'unassign':
                    cursor.execute("""
                        DELETE FROM Promo_Assignments 
                        WHERE Promotion_ID = %s AND UserCode = %s
                    """, [promotion_id, entity_id])
                elif filter_type == 'clients' and action == 'assign':
                    cursor.execute("""
                        INSERT INTO Promo_Assignments (Promotion_ID, Client_Code)
                        VALUES (%s, %s)
                    """, [promotion_id, entity_id])
                elif filter_type == 'clients' and action == 'unassign':
                    cursor.execute("""
                        DELETE FROM Promo_Assignments 
                        WHERE Promotion_ID = %s AND Client_Code = %s
                    """, [promotion_id, entity_id])
                else:
                    return JsonResponse({'error': 'Invalid action or filter type'}, status=400)

            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f"Error assigning entity: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def define_basket(request):
    baskets = PromoItemBasketHeaders.objects.all()
    form = BasketForm()  # Assuming you have a form defined for adding new baskets

    context = {
        'baskets': baskets,
        'form': form,
    }
    return render(request, 'promotions/define_basket.html', context)


def add_basket(request):
    if request.method == 'POST':
        form = BasketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('define_basket')  # Redirect back to the define_basket page after adding
    else:
        form = BasketForm()


def get_promotion(request, promotion_id):
    query = """
        SELECT * FROM Promo_Headers WHERE Promotion_ID = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [promotion_id])
        row = cursor.fetchone()

    if row:
        promotion = {
            'Promotion_ID': row[1],
            'Promotion_Description': row[5],
            'Promotion_Type': row[2],
            'Start_Date': row[3],
            'End_Date': row[4],
            'Is_Forced': row[8],
            'Is_Active': row[9],
            'Priority': row[13],
            'Promotion_Apply': row[14]
            # Include all fields
        }
        return JsonResponse({'success': True, 'promotion': promotion})
    else:
        return JsonResponse({'success': False, 'error': 'Promotion not found'})

# View for editing a promotion
def edit_promotion(request):
    if request.method == 'POST':
        promotion_id = request.POST.get('promotion_id')
        promotion_description = request.POST.get('promotion_description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        is_active = request.POST.get('is_active')
        is_forced = request.POST.get('is_forced')
        promotion_type = request.POST.get('promotion_type')
        promotion_apply = request.POST.get('promotion_apply')

        query = """
            UPDATE Promo_Headers
            SET Promotion_Description = %s,
                Start_Date = %s,
                End_Date = %s,
                Priority = %s,
                Is_Active = %s,
                Is_Forced = %s,
                Promotion_Type = %s,
                Promotion_Apply = %s
            WHERE Promotion_ID = %s
        """
        params = [
            promotion_description,
            start_date,
            end_date,
            priority,
            is_active,
            is_forced,
            promotion_type,
            promotion_apply,
            promotion_id
        ]
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# View for deleting a promotion
def delete_promotion(request):
    if request.method == 'POST':
        promotion_id = request.POST.get('promotion_id')

        query = """
            DELETE FROM Promo_Headers WHERE Promotion_ID = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [promotion_id])
            return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@require_GET
def search_baskets(request):
    query = request.GET.get('query', '')
    baskets = PromoItemBasketHeaders.objects.filter(item_basket_description__icontains=query)
    basket_data = [{'item_basket_id': basket.item_basket_id, 'item_basket_description': basket.item_basket_description} for basket in baskets]
    return JsonResponse({'success': True, 'results': basket_data})

def get_basket(request, basket_id):
    basket = get_object_or_404(PromoItemBasketHeaders, pk=basket_id)
    return JsonResponse({'success': True, 'basket': {'item_basket_id': basket.item_basket_id, 'item_basket_description': basket.item_basket_description}})
@csrf_exempt
def update_checkbox(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            promotion_id = data.get('promotion_id')
            field = data.get('field')
            value = data.get('value')

            # Use raw SQL to update the database
            with connection.cursor() as cursor:
                cursor.execute(
                    f"UPDATE Promo_Headers SET {field} = %s WHERE Promotion_ID = %s",
                    [value, promotion_id]
                )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_regions():
    with connection.cursor() as cursor:
        cursor.execute("SELECT Region_Code, Region_Description FROM Regions")
        rows = cursor.fetchall()
    regions = [{'Region_Code': row[0], 'Region_Description': row[1]} for row in rows]
    return regions

def routes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.Route_ID, r.Route_Description, r.Region_Code, rg.Region_Description, r.RVSCode, r.RVSDescription
            FROM Routes r
            LEFT JOIN Regions rg ON r.Region_Code = rg.Region_Code
        """)
        routes_data = cursor.fetchall()

    routes_list = [{
        'Route_ID': row[0],
        'Route_Description': row[1],
        'Region_Code': row[2],
        'Region_Description': row[3],
        #'CreateBy': row[4],
        'HasClients': False,
        'RVSCode': row[4],
        'RVSDescription': row[5]
    } for row in routes_data]
    form = RouteForm()

    regions = get_regions()
    return render(request, 'routes/home.html', {'routes': routes_list, 'regions': regions, 'form': form})

def add_route(request):
    if request.method == 'POST':
        route_description = request.POST.get('route_description')
        region_code = request.POST.get('region_description')

        route = Routes(
            Branch_Code = '',
            Route_Description = route_description,
            Route_Alt_Description = '',
            Region_Code = region_code,
            
         )
        route.save()
        messages.success(request, 'Route added successfully.')
        return redirect('routes')

    regions = get_regions()
    return render(request, 'routes/home.html', {'regions': regions})


def edit_route(request, route_id):
    route = get_object_or_404(Routes, Route_ID=route_id)
    if request.method == "POST":
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('routes') 
    else:
        form = RouteForm(instance=route)
    return render(request, 'routes/home.html', {'form': form, 'route': route})

def delete_route(request, route_id):
    route = get_object_or_404(Routes, Route_ID=route_id)
    if request.method == 'POST':
        route.delete()
        return redirect('routes')
    return render(request, 'routes/home.html', {'route': route})


def get_routes_data(request, route_id):
    route= get_object_or_404(Routes, Route_ID=route_id)
    data = {
        'Branch_Code' :  route.Branch_Code,
        'Route_Description' : route.Route_Description,
        'Route_Alt_Description' : route.Route_Alt_Description,
        'Region_Code': route.Region_Code

    }
     
    return JsonResponse(data)



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'authentication/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')


def affectation_clients_routes(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        action = request.GET.get('action')
        if action == 'get_routes':
            routes = Routes.objects.all().values('Route_ID', 'Route_Description')
            return JsonResponse(list(routes), safe=False)
        elif action == 'get_route_clients':
            route_id = request.GET.get('route_id')
            if not route_id:
                return JsonResponse({'error': 'No route ID provided'}, status=400)

            assigned_clients = Clients.objects.filter(Route_ID=route_id).values('Client_Code', 'Client_Description')
            available_clients = Clients.objects.filter(Route_ID=1).values('Client_Code', 'Client_Description')
            return JsonResponse({'assigned_clients': list(assigned_clients), 'available_clients': list(available_clients)})

    return render(request, 'routes/affectation_clients_routes.html')

def get_routes(request):
    routes = Routes.objects.filter(RVSCode__isnull=False).exclude(RVSCode='').values('Route_ID', 'Route_Description', 'RVSCode', 'RVSDescription')
    return JsonResponse({'routes': list(routes)})


def get_route_clients(request):
    route_id = request.GET.get('route_id')
    if route_id and route_id != '1':
        assigned_clients = Clients.objects.filter(Route_ID=route_id).values('Client_Code', 'Client_Description')
        available_clients = Clients.objects.filter(Route_ID=1).values('Client_Code', 'Client_Description')
    else:
        assigned_clients = []
        available_clients = Clients.objects.filter(Route_ID=1).values('Client_Code', 'Client_Description')

    return JsonResponse({'assigned_clients': list(assigned_clients), 'available_clients': list(available_clients)})




##################################

def assign_client_to_route(request):
    if request.method == 'POST':
        client_code = request.POST.get('client_code')
        route_id = request.POST.get('route_id')
        action = request.POST.get('action', 'assign')

        try:
            # Récupérer le client
            client = Clients.objects.get(Client_Code=client_code)
            
            if action == 'assign':
                # Récupérer l'instance de la route
                route_instance = Routes.objects.get(Route_ID=route_id)
                client.Route_ID = route_instance
            elif action == 'remove':
                # Optionnel : Vous pouvez définir Route_ID à None si vous utilisez une relation Nullable
                client.Route_ID = Routes.objects.get(Route_ID=1)  # Route_ID=1 pour aucune route

            client.save()
            return JsonResponse({'success': True})
        except Clients.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Client not found'})
        except Routes.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Route not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

#affct_
def affectation_routes_users(request):
    
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        action = request.GET.get('action')
        if action == 'get_users':
            users = InternalUser.objects.all().values('UserCode', 'UserName', 'CityID')
            return JsonResponse(list(users), safe=False)
        elif action == 'get_user_routes':
            user_code = request.GET.get('user_code')
            if not user_code:
                return JsonResponse({'error': 'No user code provided'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT Route_ID, Route_Description FROM Routes WHERE RVSCode = '' ")
                unlinked_routes = cursor.fetchall()

                cursor.execute("SELECT Route_ID, Route_Description FROM Routes WHERE RVSCode = %s", [user_code])
                linked_routes = cursor.fetchall()

            unlinked_routes = [{'Route_ID': row[0], 'Route_Description': row[1]} for row in unlinked_routes]
            linked_routes = [{'Route_ID': row[0], 'Route_Description': row[1]} for row in linked_routes]

            return JsonResponse({'unlinked_routes': unlinked_routes, 'linked_routes': linked_routes})
        

    users = InternalUser.objects.all().values('UserCode', 'UserName', 'CityID')
    return render(request, 'routes/affectation_routes_users.html', {'users': users})

@csrf_exempt
def assign_user_to_route(request):
    if request.method == 'POST':
        route_id = request.POST.get('route_id')
        user_code = request.POST.get('user_code')
        action = request.POST.get('action')
        if not route_id or not user_code:
            return JsonResponse({'success': False, 'error': 'Invalid data'})
                    
        with connection.cursor() as cursor:
            if action == 'remove':
                cursor.execute("UPDATE Routes SET RVSCode = '' WHERE Route_ID = %s", [route_id])
            else:
                cursor.execute("SELECT Route_ID FROM Routes WHERE RVSCode = %s", [user_code])
                existing_route = cursor.fetchone()
                
                if existing_route:
                    return JsonResponse({'success': False, 'error': 'User is already assigned to a route'})
                cursor.execute("UPDATE Routes SET RVSCode = %s WHERE Route_ID = %s", [user_code, route_id])
                
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



#device
def list_devices(request):
    devices = Device.objects.select_related('UserCode', 'Route_ID').all().values(
        'device_serial', 
        'device_name', 
        'UserCode__UserCode', 
        'device_status', 
        'type', 
        'Route_ID__Route_ID'
    )
    form = DeviceForm()
    return render(request, 'devices/home.html', {'devices': devices, 'form': form})

def add_device(request):
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('devices')
    else:
        form = DeviceForm()
    return render(request, 'devices/home.html', {'form': form})


def get_device_data(request, device_serial):
    device = get_object_or_404(Device, device_serial=device_serial)
    data = {
        'device_serial': device.device_serial,
        'device_name': device.device_name,
        'UserCode': device.UserCode.UserCode if device.UserCode else None,
        'device_status': device.device_status,
        'type': device.type,
        'Route_ID': device.Route_ID.Route_ID if device.Route_ID else None
    }

    return JsonResponse(data)


def edit_device(request, device_serial):
    device = get_object_or_404(Device, device_serial=device_serial)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('devices')  
    else:
        form = DeviceForm(instance=device)
    return render(request, 'devices/home.html', {'form': form})

def remove_device_from_user(request, device_serial):
    device = get_object_or_404(Device, device_serial=device_serial)
    if request.method == 'POST':
        device.delete()
        return redirect('devices')
    return render(request, 'devices/home.html', {'device': device})

def home_device(request):
    devices = Device.objects.all()
    form = DeviceForm()
    return render(request, 'devices/home.html', {'devices': devices, 'form': form})



#client
def clients(request):
    if request.method == 'POST':
        form = clientForm(request.POST)
        if form.is_valid():
            form.save()
           
            return redirect('home_client')
    else:
        form = clientForm()
    
    return render(request, 'client/home_client.html', {'form': form})

def get_client_data(request, client_id):
    client = get_object_or_404(Clients, Client_Code=client_id)
    data = {
        'Client_Code': client.Client_Code,
        'Area_Code': client.Area_Code,
        'Client_Description': client.Client_Description,
        'Client_Alt_Description': client.Client_Alt_Description,
        'Payment_Term_Code': client.Payment_Term_Code,
        'Email': client.Email,
        'Address': client.Address,
        'Alt_Address': client.Alt_Address,
        'Contact_Person': client.Contact_Person,
        'Phone_Number': client.Phone_Number,
        'Barcode': client.Barcode,
        'Client_Status_ID': client.Client_Status_ID
    }

    return JsonResponse(data)

def edit_client(request, client_id):
    client = get_object_or_404(Clients, Client_Code=client_id)
    if request.method == "POST":
        form = clientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('home_client') 
    else:
        form = clientForm(instance=client)
    return render(request, 'client/home_client.html', {'form': form, 'client': client})

def home_client(request):
    clients = Clients.objects.all()
    clients_status= Client_Statut.objects.all()
    form = clientForm()
    return render(request, 'client/home_client.html', {'clients': clients, 'form': form,'clients_status':clients_status})

def delete_client(request, Client_Code):
    client = get_object_or_404(Clients, Client_Code=Client_Code)
    client.delete()
    return redirect('home_client')  

def search_client(request):
    clients = None
    query = ''
    if request.method == 'POST':
        query = request.POST.get('query', '')
        search_type = request.POST.get('search_type', 'client_code')
        if search_type == 'client_code':
            clients = Clients.objects.filter(Client_Code__icontains=query)
        elif search_type == 'description':
            clients = Clients.objects.filter(Client_Description__icontains=query)
        else:
            clients = Clients.objects.all()
    form = clientForm()
    return render(request, 'client/home_client.html', {'clients': clients, 'form': form, 'query': query})

#upload from excel 
def upload_excel(request):
    if request.method == 'POST' and request.FILES['xlxfile']:
        excel_file = request.FILES['xlxfile']
        
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=3, values_only=True):
            client_code = row[0]
            route = get_object_or_404(Routes, pk=row[12])

            if Clients.objects.filter(Client_Code=client_code).exists():
                messages.error(request, f"Client avec le code {client_code} existe déjà.")
            else:
                client = Clients(
                    Client_Code=client_code,
                    Area_Code=row[1],
                    Client_Description=row[2],
                    Client_Alt_Description=row[3],
                    Payment_Term_Code=row[4],
                    Email=row[5],
                    Address=row[6],
                    Alt_Address=row[7],
                    Contact_Person=row[8],
                    Phone_Number=row[9],
                    Barcode=row[10],
                    Client_Status_ID=row[11],
                    Route_ID=route
                )
                client.save()
                
                messages.success(request, f"Client {client.Client_Code} ajouté")

        for row in sheet.iter_rows(min_row=2, values_only=True):
            print(row)
            
        return redirect('home_client')
    return render(request, 'client/upload_excel.html')


#statut client
def statut_client(request):
    if request.method == 'POST':
        form = client_statutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_client_status')  
    else:
        form = client_statutForm()
        
    return render(request, 'client/status_client.html', {'form': form})

def get_client_statut_data(request, client_statut_id):
    client_statut = get_object_or_404(Client_Statut, Client_Statut_ID=client_statut_id)
    data = {
        'Client_Statut_ID': client_statut.Client_Statut_ID,
        'Statut_Description': client_statut.Statut_Description
    }
    return JsonResponse(data)

def edit_statut_client(request, client_statut_id):
    client = get_object_or_404(Client_Statut, Client_Statut_ID=client_statut_id)
    if request.method == "POST":
        form = client_statutForm(request.POST, instance=client)
        if form.is_valid():
            client.Client_Statut_ID = client_statut_id
            form.save()
            return redirect('home_client_status') 
    else:
        form = client_statutForm(instance=client)
    return render(request, 'client/status_client_modifier.html', {'form': form, 'client': client})


def home_client_status(request):
    clients = Client_Statut.objects.all()  
    form = client_statutForm()
    return render(request, 'client/home_client_status.html', {'client': clients, 'form': form})

#client discounts
def home_client_discounts(request):
    message = request.GET.get('message', '')
    form = client_discountsForm()
    clients = Client_Discounts.objects.all()
    return render(request, 'client/home_discounts.html', {'clients': clients, 'message': message, 'form' : form})



def get_client_Discount_data(request, client_Code):
    client_Discount = get_object_or_404(Client_Discounts, Client_Code=client_Code)
    data = {
        'Client_Code': client_Discount.Client_Code,
        'Trx_Code': client_Discount.Trx_Code,
        'Discounts': client_Discount.Discounts,
        'Month': client_Discount.Month,
        'Years': client_Discount.Years,
        'Discounts_label': client_Discount.Discounts_label,
        'Applied': client_Discount.Applied,
        'Stamp_Date': client_Discount.Stamp_Date,  
        'Affected_item_code': client_Discount.Affected_item_code,
    }
    return JsonResponse(data)



def client_discounts(request):
    error_message = None
    if request.method == "POST":
        client_code = request.POST.get("Client_Code")
        clients = Clients.objects.filter(Client_Code=client_code)
        
        if clients.exists():
            form = client_discountsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home_discounts')
            
        else:
            error_message = "Aucun client ne correspond à ce code client."
            form = client_discountsForm()
            return render(request, 'client/client_discounts.html', {'form': form, 'error_message': error_message})
    else:
        form = client_discountsForm()

    return render(request, 'client/client_discounts.html', {'form': form, 'error_message': error_message})


def edit_client_discounts(request, Client_Code):
    client = get_object_or_404(Client_Discounts, Client_Code=Client_Code)
    if request.method == "POST":
        form = client_discountsForm(request.POST, instance=client)
        if form.is_valid():
            client.Client_Code = Client_Code
            form.save()
            return redirect('home_discounts') 
    else:
        form = client_discountsForm(instance=client)
        form.fields['Client_Code'].widget.attrs['readonly'] = True
    return render(request, 'client/client_discounts_edit.html', {'form': form, 'client': client})

def delete_discounts(request, Client_Code):
    client = get_object_or_404(Client_Discounts, Client_Code=Client_Code)
    client.delete()
    return redirect('home_discounts') 


def delete_selected_clients(request):
    if request.method == 'POST':
        client_ids = request.POST.getlist('client_ids')
        if client_ids:
            Client_Discounts.objects.filter(Client_Code__in=client_ids).delete()
            messages.success(request, 'Selected clients have been deleted.')
        else:
            messages.error(request, 'No clients selected for deletion.')
    return redirect('home_discounts')
  
def search_client_discount(request):
    clients = None
    query = ''
    if request.method == 'POST':
        query = request.POST.get('query', '')
        search_type = request.POST.get('search_type', 'client_code')
        if search_type == 'client_code':
            clients = Client_Discounts.objects.filter(Client_Code=query)
        else:
            clients = Client_Discounts.objects.all()
    return render(request, 'client/home_discounts.html', {'clients': clients, 'query': query})
  
def upload_excel_discount(request):
    if request.method == 'POST' and request.FILES['xlxfile']:
        excel_file = request.FILES['xlxfile']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=3, values_only=True):
            clients = Clients.objects.filter(Client_Code=row[0])
           
            if clients.exists():
                client = Client_Discounts(
                    Client_Code=row[0],
                    Trx_Code='',
                    Discounts=row[2],
                    Month=row[3],
                    Years=row[4],
                    Discounts_label=row[5],
                    Applied=0,
                    Stamp_Date=timezone.now(),
                    Affected_item_code='en instance'
                
                )
                client.save()  
                print(f"Client {client.Client_Code} ajouté")
            else:
                message = f"Les clients disponible sont tous ajoutés"

        for row in sheet.iter_rows(min_row=2, values_only=True):
            print(row)
        return redirect(f'/client/home_client_discount/?message={message}')     
    return render(request, 'client/upload_excel_discount.html')
    

#client target

def home_client_target(request):
    clients = Client_Target.objects.all() 
    form = Client_TargetForm()
    return render(request, 'client/home_client_target.html', {'clients': clients, 'form': form})

def get_target(request, Client_Code):
    client_t = get_object_or_404(Client_Target, Client_Code=Client_Code)
    data = {
        'Client_Code': client_t.Client_Code,
        'Month': client_t.Month,
        'years': client_t.years,
        'Targed_Achieved': client_t.Targed_Achieved,
        'Target_value': client_t.Target_value,

    }
    
    return JsonResponse(data)


def client_target(request):
    error_message = None
    if request.method == "POST":
        client_code = request.POST.get("Client_Code")
        clients = Clients.objects.filter(Client_Code=client_code)
        
        if clients.exists():
            form = Client_TargetForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home_target')
            
        else:
            error_message = "Aucun client ne correspond à ce code client."
            form = Client_TargetForm()
            return render(request, 'client/client_target.html', {'form': form, 'error_message': error_message})
    else:
        form = Client_TargetForm()

    return render(request, 'client/client_target.html', {'form': form, 'error_message': error_message})


def edit_client_target(request, Client_Code):
    client = get_object_or_404(Client_Target, Client_Code=Client_Code)
    if request.method == "POST":
        form = Client_TargetForm(request.POST, instance=client)
        if form.is_valid():
            client.Client_Code = Client_Code
            form.save()
            return redirect('home_target') 
    else:
        form = Client_TargetForm(instance=client)
        form.fields['Client_Code'].widget.attrs['readonly'] = True
    return render(request, 'client/client_target_edit.html', {'form': form, 'client': client})

def delete_target(request, Client_Code):
    client = get_object_or_404(Client_Target, Client_Code=Client_Code)
    client.delete()
    return redirect('home_target') 


#channels
def channels(request):
    if request.method == 'POST':
        form = ChannelsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_channel')
    else:
        form = ChannelsForm()
    
    channels_list = Channels.objects.all()  
    
    return render(request, 'client/channel.html', {'form': form, 'channels': channels_list})


def get_channel_data(request, channel_code):
    channel = get_object_or_404(Channels, channel_code=channel_code)
    data = {
        'channel_code': channel.channel_code,
        'Channel_description': channel.Channel_description
    }
    return JsonResponse(data)

def edit_channel(request, channel_code):
    client = get_object_or_404(Channels, channel_code=channel_code)
    if request.method == "POST":
        form = ChannelsForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('home_channel') 
    else:
        form = ChannelsForm(instance=client)
    return render(request, 'client/modifier_channel.html', {'form': form, 'client': client})

def home_channel(request):
    clients = Channels.objects.all()
    form = ChannelsForm()
    return render(request, 'client/home_channel.html', {'form': form, 'clients': clients})

def delete_channel(request, channel_code):
    client = get_object_or_404(Channels, channel_code=channel_code)
    client.delete()
    return redirect('home_channel')  







#users


def users(request):
    users = InternalUser.objects.all()
    groupe = UserGroupe.objects.all()
    form = UserForm()
    return render(request, 'users/home.html', {'users': users, 'form': form, 'groupe': groupe})

def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = UserForm()
    return render(request, 'users/list_users.html', {'form': form})



def get_user_data(request, UserCode):
    user = get_object_or_404(InternalUser, UserCode=UserCode)
    data = {
        'UserCode': user.UserCode,
        'UserName': user.UserName,
        'PhoneNumber': user.PhoneNumber,
        'Grouping': user.Grouping,
        'IsBlocked': user.IsBlocked,
        'LoginName': user.LoginName,
        'AreaCode': user.AreaCode,
        'CityID': user.CityID,
        'RouteCode': user.RouteCode,
        'ParentCode': user.ParentCode
    }

    return JsonResponse(data)






def edit_user(request, UserCode):
    user = get_object_or_404(InternalUser, UserCode=UserCode)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            print(user.IsBlocked)  
            return redirect('users')
    else:
        form = UserForm(instance=user)
    
    return render(request, 'users/home.html', {'form': form, 'user': user})

def delete_user(request, UserCode):
    user = get_object_or_404(InternalUser, UserCode=UserCode)
    user.delete()
    return redirect('users') 


def delete_groupe(request, UserCode):
    user = get_object_or_404(UserGroupe, UserCode=UserCode)
    if request.method == 'POST':
        user.delete()
        return redirect('users')
    return render(request, 'users/home.html', {'user': user})

def search_user(request):
    users = None
    query = ''
    if request.method == 'POST':
        query = request.POST.get('query', '')
        search_type = request.POST.get('search_type', 'UserCode')
        if search_type == 'UserCode':
            users = InternalUser.objects.filter(UserCode__icontains=query)
        elif search_type == 'UserName':
            users = InternalUser.objects.filter(UserName__icontains=query)
        elif search_type == 'PhoneNumber':
            users = InternalUser.objects.filter(PhoneNumber=query)
        elif search_type == 'CityID':
            users = InternalUser.objects.filter(CityID=query)
        else:
            users = InternalUser.objects.all()
    form = UserForm()
    return render(request, 'users/home.html', {'users': users, 'form': form, 'query': query})


#groupe

def home_groupe(request):
    groupes = UserGroupe.objects.all()
    return render(request, 'users/Groupes.html', {'groupes': groupes})

def add_groupe(request):
    if request.method == 'POST':
        form = UserGroupeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_groupe')
    else:
        form = UserGroupeForm()
    return render(request, 'users/Groupes.html', {'form': form})

def edit_groupe(request, Code_groupe):
    groupe = get_object_or_404(UserGroupe, Code_groupe=Code_groupe)
    if request.method == 'POST':
        form = UserGroupeForm(request.POST, instance=groupe)
        if form.is_valid():
            form.save()
            return redirect('home_groupe')
    else:
        form = UserGroupeForm(instance=groupe)
    return render(request, 'users/Groupes.html', {'form': form, 'groupe': groupe})

def delete_groupe(request, Code_groupe):
    groupe = get_object_or_404(UserGroupe, Code_groupe=Code_groupe)
    if request.method == 'POST':
        groupe.delete()
        return redirect('home_groupe')
    return render(request, 'users/Groupes.html', {'groupe': groupe})

def get_group_data(request, Code_groupe):
    group = get_object_or_404(UserGroupe, Code_groupe=Code_groupe)
    data = {
        'Code_groupe': group.Code_groupe,
        'Groupe_description': group.Groupe_description,
    }

    return JsonResponse(data)