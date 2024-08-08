from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Créer une classe admin personnalisée pour le modèle User
class CustomUserAdmin(UserAdmin):
    # Vous pouvez personnaliser ici
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('username',)

# Enregistrer la classe admin personnalisée
admin.site.register(User, CustomUserAdmin)
