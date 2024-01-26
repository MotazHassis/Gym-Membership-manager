from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login),
    path('registration', views.registration),
    path('main', views.main),
    path('add_member', views.add_member),
    path('member_list', views.member_list),
    path('note', views.note),
    path('view_items', views.view_items),
    path('add_items', views.add_items),
    path('logout', views.logout),
    path('member_profile/<int:id>', views.member_profile),
    path('delete_member/<int:id>', views.delete),
    path('update_member/<int:id>', views.update_member),
    path('update_member_pic/<int:id>', views.update_member_pic),
    path('renew_membership/<int:id>', views.renew_membership),
    path('delete_item/<int:id>', views.delete_item),
    path('add_remove_item/<int:operation>/<int:id>', views.add_remove_item),
    path('item_profile/<int:id>', views.item_profile),
    path('change_admin_setting', views.change_admin_setting),
    path('search', views.search),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
