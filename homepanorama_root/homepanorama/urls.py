"""homepanorama URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from script_status.views import *
from plants.views import *

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('scriptstatus/<int:script_id>/', script_status_detail, name='scriptstatus'),
    path('plant/<int:plant_id>/', plant_detail, name='plant'),
    path('getAllPlantData/', get_all_plant_data, name='allplants'),
    path('getAllPlants/', get_all_plants, name="get_all_plants"),
    path('planthistory/<int:plant_id>/', plant_detail_history, name='planthistory'),
    path('reload_plant_data/', reload_plant_data, name="reload_plant_data"),
    path('create_update_plant/<int:plant_id>/', create_update_plant, name="create_update_plant"),
    path('getNewId/', get_new_id, name='get_new_id'),
    # path('getAvailableMacAddresses/', get_not_set_mac_addresses, name='get_not_set_mac_addresses'),

]
