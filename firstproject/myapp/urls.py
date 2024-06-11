from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.welcome_page, name="welcome"),
    path("login/", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("logout/", views.logout_account, name="logout"),
    path("editprofile/", views.editprofile_page, name="editprofile"),
    path("addproduct/", views.addproduct_page, name="addproduct"),
    path("productpage/<int:pk>", views.product_page, name="productpage"),
    path("add_to_cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("update_cart/", views.update_cart, name="update_cart"),
    path("remove_from_cart/<int:cart_item_id>", views.remove_from_cart, name="remove_from_cart"),
    path("ordersummary/", views.ordersummary_page, name="ordersummary"),
    path("ordersummary/checkout/", views.checkout_page, name="checkout"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("seller_orders/", views.seller_orders, name="seller_orders"),
    path("order_details/<int:order_id>", views.order_details, name="order_details"),
    path("seller_analytics/", views.seller_analytics, name="seller_analytics"),

    # Try
    path("navbarAndfooter/", views.navbarAndfooter, name="navbarAndfooter"),
    path("cart/",views.cart_page, name="cart"),
    path("home/", views.home_page, name="home"),
    path("profile/",views.profile_page, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
