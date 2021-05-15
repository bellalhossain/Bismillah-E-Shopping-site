from django.contrib import admin
from django.urls import path
from ecom import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name=''),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='ecom/logout.html'),name='logout'),
    path('aboutus', views.aboutus),
    path('contactus', views.contactus_view,name='contactus'),
    path('search', views.search_view,name='search'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('view-feedback', views.feedback_view, name='view-feedback'),
    path('Subscribe', views.subscribe,name='Subscribe'),
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='ecom/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard, name='admin-dashboard'),

    path('view-consumer', views.view_consumer, name='view-consumer'),
    path('delete-consumer/<int:pk>', views.delete_customer_view,name='delete-consumer'),
    path('update-consumer/<int:pk>', views.update_view_of_consumer, name='update-consumer'),

    path('admin-products', views.view_of_admin_item, name='admin-products'),
    path('admin-add-item', views.admin_add_item, name='admin-add-item'),
    path('delete-item/<int:pk>', views.delete_item_view, name='delete-item'),
    path('update-item/<int:pk>', views.update_item_view, name='update-item'),

    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_status, name='update-order'),


    path('customersignup', views.consumer_signup_view),
    path('customerlogin', LoginView.as_view(template_name='ecom/customerlogin.html'),name='customerlogin'),
    path('consumer-home', views.consumer_home, name='consumer-home'),
    path('my-order', views.consumer_order_view, name='my-order'),
    path('my-profile', views.consumer_profile_view, name='my-profile'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('download-invoice/<int:orderID>/<int:productID>', views.get_invoice_view, name='download-invoice'),


    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart, name='cart'),
    path('remove-from-cart/<int:pk>', views.delete_cart, name='remove-from-cart'),
    path('consumer-address', views.consumer_address, name='consumer-address'),
    path('payment-success', views.payment_view, name='payment-success'),


]
