from django.urls import path
from .views import AlimonyList, AlimonyDetail, CreateAlimony


urlpatterns = [ 
    path('<slug:category>/<slug:slug>/', AlimonyDetail.as_view(), name='alimony-detail'),
    path('add-alimony/', CreateAlimony.as_view(), name='add_alimony'),
    path('', AlimonyList.as_view(), name='alimony-list'),
]