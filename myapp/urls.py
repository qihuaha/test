from .views import CookbookDetailView, ChatView, CommunityDetailView, Materiallistview, StoreDetail, CookbookLikesView, \
 \
    Infodetailview, UploadImageView, RegisterView, LoginView, CookbookVideoView, \
    UpdateUserProfileView, CommunityListView, CookbookListView, Orderlv, Addresslv
from django.urls import path
from . import views

urlpatterns = [
    # path('items/', ItemListView.as_view(), name='item-list'),
    path('cookbook_page/', CookbookListView.as_view(), name='cookbook-page'),
    path('food_detail_page/<int:cookbook_id>', CookbookDetailView.as_view(), name='food_detail_page'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('community/', CommunityListView.as_view(), name='community'),
    path('community_detail/<int:community_id>', CommunityDetailView.as_view()),
    path('material/', Materiallistview.as_view()),
    path('address/', Addresslv.as_view()),
    path('submit_material/', views.submit_material),
    path('store/', StoreDetail.as_view()),
    path('cookbook/<int:cookbook_id>/likes/', CookbookLikesView.as_view(), name='cookbook_likes'),
    path('infodetail/', Infodetailview.as_view()),
    path('upload_image/', UploadImageView.as_view(), name='upload_image'),
    path('order/', Orderlv.as_view()),
    path('get_recipes_by_materials/', views.get_recipes_by_materials, name='get_recipes_by_materials'),
    path('cookbook/videos/', CookbookVideoView.as_view(), name='cookbook-videos'),
    path('materials/<str:name>/delete/', views.delete_material, name='delete_material'),
    path('submit_order/', views.submit_order),
    path('submit_address/', views.submit_address),
    # 3.10
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('update_user_profile/', UpdateUserProfileView.as_view(), name='update_user_profile'),
    #3.11

]
