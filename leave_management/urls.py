from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
path('',views.homepage,name = "homepage"),
path("account_login/",views.Login.as_view(),name="login"),
path('logout/', LogoutView.as_view(template_name='leave_management/logout.html'), name= 'logout'),
path("redirector/",views.redirector,name="redirector"),
path("leave_processor",views.leave_processor,name="leave_processor"),
path('landing_page/lecturer/',views.lecturer_landing_page,name="lecturer_landing_page"),
path('landing_page/dean/',views.dean_landing_page,name="dean_landing_page"),
path('landing_page/hod/',views.hod_landing_page,name="hod_landing_page"),
path('landing_page/welfare/',views.welfare_landing_page,name="welfare_landing_page"),
path('add_lecturer/',views.add_Lecturer.as_view(),name="Add_lecturer"),
path("add_school/",views.add_school.as_view(),name = "Add_school"),
path("add_h.o.d/",views.add_Hod.as_view(),name = "Add_hod"),
path("add_dean/",views.add_Dean.as_view(),name = "Add_dean"),
path("add_welfare/",views.add_Welfare.as_view(),name = "Add_welfare"),

]