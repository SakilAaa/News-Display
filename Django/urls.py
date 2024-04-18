from django.urls import path, include
import news.views as views

urlpatterns = [
    path('news_all/<int:page_id>', views.news_all),
    path('news_all/', views.news_all_jump),
    path('lookfor/', views.lookfor),
    path('lookfor/front/', views.frontpage),
    path('lookfor/<int:page_id>', views.lookfor_page),
    path('mainpage/', views.mainpage),
    path('category/', views.category),
    path('category/detail/<int:id>', views.category_detail_jump),
    path('category/detail/<int:category_id>/<int:page_id>', views.category_detail),
    path('news/', views.jump),
    path('news/<int:id>', views.show_news),
    path('comment/<int:id>', views.comment),
    path('comment/delete/<int:comment_id>', views.delete)
]
