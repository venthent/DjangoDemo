from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from .views import AuthView,EmployeeView,OrganisationView

urlpatterns=[
    # path('emp/',EmployeesList.as_view()),
    # path('emp/<int:pk>',EmployeesList.as_view()),
    path('auth/',AuthView.as_view()),
    path('emp/',EmployeeView.as_view()),
    path('org/',OrganisationView.as_view())
]
