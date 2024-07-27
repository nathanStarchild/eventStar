from django.urls import path, include
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tickets/', views.tickets, name='tickets'),

    #ajax
    path('ajax/addHuman/', views.ajaxAddHuman, name='ajaxAddHuman'),
    path('ajax/payment/create/', views.ajaxCreatePayment, name='ajaxCreatePayment'),
    path('ajax/payment/<paymentId>/getAmount/', views.ajaxPaymentAmount, name='ajaxPaymentAmount'),
    path('ajax/ticket/create/', views.ajaxCreateTicket, name='ajaxCreateTicket'),

]