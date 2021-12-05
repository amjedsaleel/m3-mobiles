# Django
from django.urls import path

# local Django
from . import views

app_name = 'admin-panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout', views.logout, name='logout'),

    # Brand
    path('brands/', views.brand, name='brand'),
    path('add-brand/', views.add_brand, name='add-brand'),
    path('filter/<str:variant_id>/', views.brand_wise_variant, name='brand-wise-variant'),
    path('edit-brand/<str:brand_id>/', views.edit_brand, name='edit-brand'),
    path('delete-brand/<str:brand_id>/', views.delete_brand, name='delete-brand'),

    # Products
    path('products/', views.all_products, name='products'),
    path('add-product/', views.add_product, name='add-product'),
    path('edit-product/<str:product_id>/', views.edit_product, name='edit-product'),
    path('delete-product/<str:product_id>/', views.delete_product, name='delete-product'),

    # Variant
    path('add-variant/', views.add_variant, name='add-variant'),
    path('edit-variant/<str:variant_id>/', views.edit_variant, name='edit-variant'),
    path('delete-variant/<str:variant_id>/', views.delete_variant, name='delete-variant'),
    path('variant-details/<str:variant_slug>/', views.variant_details, name='variant-details'),

    # User
    path('users/', views.users_list, name='users'),
    path('block-user/<str:pk>/', views.block_user, name='block-user'),
    path('unblock-user/<str:pk>/', views.unblock_user, name='unblock-user'),

    # Order
    path('active-orders/', views.active_order_products, name='active-order-products'),
    path('orders-histpry/', views.order_history, name='orders-history'),
    path('update-order-status/<str:pk>/', views.update_order_status, name='update-order-status'),

    # Offers
    path('offers/', views.offers, name='offers'),
    path('add-variant-offer/', views.add_variant_offer, name='add-variant-offer'),
    path('add-product-offer/', views.add_product_offer, name='add-product-offer'),
    path('add-brand-offer/', views.add_brand_offer, name='add-brand-offer'),
    path('update-variant-offer/<str:pk>/', views.update_variant_offer, name='update-variant-offer'),
    path('update-product-offer/<str:pk>/', views.update_product_offer, name='update-product-offer'),
    path('update-brand-offer/<str:pk>/', views.update_brand_offer, name='update-brand-offer'),
    path('delete-variant-offer/<str:pk>/', views.delete_variant_offer, name='delete-variant-offer'),
    path('delete-product-offer/<str:pk>/', views.delete_product_offer, name='delete-product-offer'),
    path('delete-brand-offer/<str:pk>/', views.delete_brand_offer, name='delete-brand-offer'),

    # Coupon offers
    path('all-coupons/', views.coupons, name='all-coupons'),
    path('add-coupon/', views.add_coupon, name='add-coupon'),
    path('edit-copuon/<str:pk>/', views.edit_coupon, name='edit-coupon'),
    path('delete-coupon/<str:pk>/', views.delete_coupon, name='delete-coupon'),
    path('redeemed-coupons/', views.redeemed_coupon, name='redeemed-coupons'),

    # Report
    path('report/', views.report, name='report'),
    path('order-product-csv/', views.order_product_csv, name='order-product-csv'),
    path('brands-csv/', views.brands_csv, name='brands-csv'),
    path('products-csv', views.all_products_csv, name='products-csv'),
    path('brand-pdf/', views.brand_pdf, name='brand-pdf')
]
