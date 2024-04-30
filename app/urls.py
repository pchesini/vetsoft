from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),

    path("productos/", view=views.products_repository, name="products_repo"),
    path("productos/nuevo/", view=views.products_form, name="products_form"),
    path("productos/editar/<int:id>/", view=views.products_form, name="products_edit"),
    path("productos/eliminar/", view=views.products_delete, name="products_delete"),
    path("veterinarios/", view=views.vets_repository, name="vets_repo"),
    path("veterinarios/nuevo/", view=views.vets_form, name="vets_form"),
    path("veterinarios/editar/<int:id>/", view=views.vets_form, name="vets_edit"),
    path("veterinarios/eliminar/", view=views.vets_delete, name="vets_delete"),

    path("proveedor/", view=views.provider_repository, name="provider_repo"), 
    path("proveedor/nuevo/", view=views.provider_form, name="provider_form"),
    path("proveedor/editar/<int:id>/", view=views.provider_form, name="provider_edit"),
    path("proveedor/eliminar/", view=views.provider_delete, name="provider_delete"),

]
