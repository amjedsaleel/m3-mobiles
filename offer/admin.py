from django.contrib import admin

from .models import BrandOffer, ProductOffer, VariantOffer, Coupon, RedeemedCoupon

# Register your models here.

admin.site.register(BrandOffer)
admin.site.register(ProductOffer)
admin.site.register(VariantOffer)
admin.site.register(Coupon)
admin.site.register(RedeemedCoupon)
