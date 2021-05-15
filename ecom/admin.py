from django.contrib import admin
from .models import Consumer,Item,ConsumerOrder,Feedback
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Consumer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Item, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(ConsumerOrder, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)
# Register your models here.
