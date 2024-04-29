from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    
    path("veterinarios/", view=views.vets_repository, name="vets_repo"),
    path("veterinarios/nuevo/", view=views.vets_form, name="vets_form"),
    path("veterinarios/editar/<int:id>/", view=views.vets_form, name="vets_edit"),
     path("veterinarios/eliminar/", view=views.vets_delete, name="vets_delete"),
     
    path("medicina/", view=views.medis_repository, name="medi_repo"),
    path("medicina/nuevo/", view=views.medis_form, name="medi_form"),
    path("medicina/editar/<int:id>/", view=views.medis_form, name="medi_edit"),
    path("medicina/eliminar/", view=views.medis_delete, name="medi_delete"),  
]
