from django import forms
from .models import Channels, Client_Discounts, Client_Statut, Client_Target, Clients, Device, InternalUser, Produit, PromoDetails, PromoHeaders, PromoItemBasketHeaders, Routes, UserGroupe
from django.db import connection


class UserForm(forms.ModelForm):
    grouping_choices = [(groupe.Code_groupe, groupe.Groupe_description) for groupe in UserGroupe.objects.all()]
    print(grouping_choices) 
    Grouping = forms.ChoiceField(choices=grouping_choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:


        model = InternalUser
        fields = [
            'UserCode',
            'UserName',
            'PhoneNumber',
            'Grouping',
            'IsBlocked',
            'LoginName',
            'AreaCode',
            'CityID',
            'RouteCode',
            'ParentCode'
        ]
        widgets = {
            'IsBlocked': forms.CheckboxInput(),
        }
        


class UserGroupeForm(forms.ModelForm):
    class Meta:
        model = UserGroupe
        fields  = [
            'Code_groupe',
            'Groupe_description'
        ]



class AssignPromotionSearchForm(forms.Form):
    promotion_type = forms.ChoiceField(
        choices=[
            ('', 'All Types'),  # Default option for no filter
            ('Trade Sales', 'Trade Sales'),
            ('Consumer Sales', 'Consumer Sales'),
            # Add other types as needed
        ],
        required=False,
        label='Promotion Type'
    )
    search_date = forms.DateField(
        required=False,
        label='Search Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    filter_type = forms.ChoiceField(
        choices=[('users', 'Users'), ('clients', 'Clients')],
        label='Filter by',
        required=True
    )

    def get_promotion_choices(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Promotion_ID, Promotion_Description FROM Promo_Headers")
            promotions = cursor.fetchall()
        return [(promo[0], promo[1]) for promo in promotions]

class BasketForm(forms.ModelForm):
    class Meta:
        model = PromoItemBasketHeaders
        fields = [
            'item_basket_id',
            'item_basket_description'
        ]
        


class PromotionSearchForm(forms.Form):
    promotion_id = forms.IntegerField(required=False, label='Promotion ID')
    promotion_description = forms.CharField(max_length=100, required=False, label='Description')
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)


class NewPromotionForm(forms.Form):
    promotion_description = forms.CharField(
        label='Promotion Description',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label='End Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    priority = forms.IntegerField(
        label='Priority',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    max_applied = forms.IntegerField(
        label='Max Applied',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    is_active = forms.ChoiceField(
        label='Active',
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_forced = forms.ChoiceField(
        label='Forced',
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    promotion_type = forms.ChoiceField(
        label='Promotion Type',
        choices=[('Trade Sales', 'Trade Sales'), ('Consumer Sales', 'Consumer Sales')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    promotion_apply = forms.ChoiceField(
        label='Apply',
        choices=[('ISELL', 'ISELL'), ('E-Ordering', 'E-Ordering'), ('Other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class PromoHeadersForm(forms.ModelForm):
    class Meta:
        model = PromoHeaders
        fields = [
            'promotion_description', 
            'promotion_type', 
            'start_date', 
            'end_date',
            'is_forced', 
            'is_active',  
            'priority', 
            'promotion_apply', 
        ]
        widgets = {
            'promotion_description': forms.TextInput(attrs={'class': 'form-control'}),
            'promotion_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_forced': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),            
            'promotion_apply': forms.Select(attrs={'class': 'form-control'}),
            'basket': forms.Select(attrs={'class': 'form-control'}),
        }



class PromoDetailsForm(forms.ModelForm):
    class Meta:
        model = PromoDetails
        fields = [
            'basket',
            'quantity_buy',
            'types_buy',
            'quantity_get',
            'types_get'

        ]
    widgets = {
        'basket': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    }






class clientForm(forms.ModelForm):
    status_choices = [(status.Client_Statut_ID, status.Statut_Description) for status in Client_Statut.objects.all()]
    print(status_choices) 
    Client_Status_ID = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}, choices=[(0, '0')] + status_choices))
    
    class Meta:
        model = Clients
        fields = [
            'Client_Code',
            'Area_Code',
            'Client_Description',
            'Client_Alt_Description',
            'Payment_Term_Code',
            'Email',
            'Address',
            'Alt_Address',
            'Contact_Person',
            'Phone_Number',
            'Barcode',
            'Client_Status_ID'
        ]
        widgets = {
            'Client_Code': forms.TextInput(attrs={'class': 'form-control'}),
            'Area_Code': forms.TextInput(attrs={'class': 'form-control'}),
            'Client_Description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Client_Alt_Description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Payment_Term_Code': forms.TextInput(attrs={'class': 'form-control'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'Address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Alt_Address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Contact_Person': forms.TextInput(attrs={'class': 'form-control'}),
            'Phone_Number': forms.TextInput(attrs={'class': 'form-control'}),
            'Barcode': forms.TextInput(attrs={'class': 'form-control'}),
        }

class client_statutForm(forms.ModelForm):
    class Meta:
        model = Client_Statut
        fields  = [
            'Client_Statut_ID',
            'Statut_Description'
        ]


                

class client_discountsForm(forms.ModelForm):
    class Meta:
        model = Client_Discounts
        fields  = [
            'Client_Code',
            'Discounts',
            'Month',
            'Years',
            'Discounts_label',
            'Stamp_Date',
            'Affected_item_code'
            
            ]
        
        widgets = {
            'Client_Code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Client Code'}),
            'Discounts': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Discounts', 'step': '0.01'}),
            'Month': forms.TextInput(attrs={'class': 'form-control'}),
            'Years': forms.TextInput(attrs={'class': 'form-control'}),
            'Discounts_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Discount Label'}),
            'Stamp_Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'Affected_item_code': forms.TextInput(attrs={'class':'form-control'})
        }


class Client_TargetForm(forms.ModelForm):
    class Meta:
        model = Client_Target
        fields  = [
            'Client_Code',
            'Month',
            'years',
            'Targed_Achieved',
            'Target_value',
            'Stamp_Date'
            ]
        def __init__(self, *args, **kwargs):
            super(clientForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

class ChannelsForm(forms.ModelForm):
    class Meta:
        model = Channels
        fields  = [
            'channel_code',
            'Channel_description',
        ]


class RouteForm(forms.ModelForm):
    class Meta:
        model = Routes
        fields = [
            'Route_Description',
            'Route_Alt_Description',
            'Region_Code',
            'RVSCode',
            'RVSDescription'
        ]


class DeviceForm(forms.ModelForm):
    

    class Meta:
        model = Device
        fields = [
            'device_serial',
            'device_name',
            'UserCode',
            'device_status',
            'type',
            'Route_ID'
        ]

        widgets = {
            'device_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_status': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
        }



class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
        'CodeProduit',
        'ProduitDescription',
        'AltProduitDescription',
        'typeProduit'
        ]
