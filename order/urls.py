# Django
from django.urls import path

# local Django
from . import views

app_name = 'order'

urlpatterns = [
    path('place-order/', views.place_order, name='place-order'),
    path('review-order/', views.review_order, name='review-order'),
    path('oreder-completed/', views.order_completed, name='order-completed')
]
