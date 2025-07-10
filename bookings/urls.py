from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    signup, login_user, logout_user, welcome, events,
    about_college, about_previous_vitopia, wishlist, add_to_wishlist, remove_from_wishlist,
    create_order, verify_payment, payment_success  # ✅ Add payment views
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('welcome/', welcome, name='welcome'),
    path('events/', events, name='events'),
    
    path('about_college/', about_college, name='about_college'),
    path('about_previous_vitopia/', about_previous_vitopia, name='about_previous_vitopia'),
    path("wishlist/", wishlist, name="wishlist"),
    
   
    path("add_to_wishlist/<int:item_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("remove-from-wishlist/<int:item_id>/", remove_from_wishlist, name="remove_from_wishlist"),

    # ✅ Payment Routes
    path("create-order/", create_order, name="create_order"),
    path("verify-payment/", verify_payment, name="verify_payment"),
    path("payment-success/", payment_success, name="payment_success"),
]

# ✅ Serve media files (for development mode only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
