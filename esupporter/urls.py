from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #user
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),

    path('mypage/', views.Mypage.as_view(), name='mypage'),

    # ES管理
    path('company_list/', views.CompanyListView.as_view(), name='company_list'),
    path('create_company/', views.CompanyCreateFormView.as_view(), name='create_company'),
    path("delete_company/<int:pk>/", views.CompanyDeleteView.as_view(), name="delete_company"),
    path('es_list/<int:pk>', views.ESListView.as_view(), name='es_list'),
    path('create_es/<int:pk>', views.ESCreateFormView.as_view(), name='create_es'),
    path("update_es/<int:pk>/", views.ESUpdateView.as_view(), name="update_es"),
    path("delete_es/<int:pk>/", views.ESDeleteView.as_view(), name="delete_es"),
    


    
    # AI要約
    path('question_list/', views.QuestionListView.as_view(), name='question_list'),
    path('create_question/', views.QuestionCreateFormView.as_view(), name='create_question'),
    path('question_detail/<int:pk>/',views.QuestionDetail.as_view(),name='question_detail'),  
    path('update_question/<int:pk>/',views.QuestionUpdateView.as_view(),name='update_question'),  
    # path('delete_question/<int:pk>/',views.QuestionDetail.as_view(),name='delet_question'),  



]