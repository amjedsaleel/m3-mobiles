# Django
from django.urls import path

# local Django
from . import views

app_name = 'order'

urlpatterns = [
    path('place-order/', views.place_order, name='place-order'),
    path('buy-now/place-order/', views.buy_now_place_order, name='buy-now-place-order'),
    path('review-order/', views.review_order, name='review-order'),
    path('buy-now/review-order/', views.buy_now_review_order, name='buy-now-review-order'),
    path('oreder-completed/', views.order_completed, name='order-completed')
]
