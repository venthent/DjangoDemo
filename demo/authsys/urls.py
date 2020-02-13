from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from .views import EmployeesList,AuthView

urlpatterns=[
    path('emp/',EmployeesList.as_view()),
    path('emp/<int:pk>',EmployeesList.as_view()),
    path('auth/',AuthView.as_view()),
]
