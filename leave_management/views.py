from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .models import  Lecturer,Lecturer_form,Dean,Dean_form,Head_of_Department,Head_of_Department_form,School,SchoolForm,Welfare,Welfare_form,Leave_Form,leave_request,User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
# Create your views here.
def redirector(request):
	print(dir(request.user))
	try:
		if request.user.lecturer is not None:
			return redirect("lecturer_landing_page")
	except User.lecturer.RelatedObjectDoesNotExist:
		pass
	try:
		if request.user.head_of_department is not None:
			return redirect("hod_landing_page")
	except User.head_of_department.RelatedObjectDoesNotExist:
		pass
		
	try:
		if request.user.dean is not None:
			return redirect("dean_landing_page")
	except User.dean.RelatedObjectDoesNotExist:
		pass
		
	try:
		if request.user.welfare is not None:
			return redirect("welfare_landing_page")
	except User.welfare.RelatedObjectDoesNotExist:
		pass		
	

class Login(LoginView):
	template_name = "leave_management/login.html"
	next = "landing_page"


def homepage(request):
	print(dir(request.user))
	if request.user.is_authenticated:
		return redirector(request)
	return render(request,"leave_management/index.htm",{})
	
def lecturer_landing_page(request):
	type = "L"
	current_user = request.user.lecturer
	leaves = current_user.leave_request_set.all()
	for leave in leaves:
		if leave.leave_status == "Pending":
			messages.info(request,f"Please wait. Your {leave.leave_type} for {leave.duration} is being processed")
		elif leave.leave_status == "Approved":
			messages.success(request,f"Congratulations. Your {leave.leave_type} for {leave.duration} is has been approved.")
		elif leave.leave_status == "Declined":
			messages.warning(request,f"Sorry. Your {leave.leave_type} for {leave.duration} has been declined")
	if request.method == "POST":
		leave_form = Leave_Form(request.POST)
		if leave_form.is_valid():
			form = leave_form.save(commit=False)
			form.lecturer = current_user
			form.school = current_user.School
			form.save()
			messages.success(request,"Leave request has been sent successfully. You will receive a reply soon.")
	else:
		leave_form = Leave_Form()
	
	return render(request,"leave_management/landing_page.html",{"type":type,"current_user":current_user,"leave_form":leave_form,})
	
def leave_processor(request):
	if request.method == "POST":
		leave_obj = leave_request.objects.get(pk=int(request.POST.get("pk")))
		approved = request.POST.get("approved")
		if approved == "True":
			approved = True
		else:
			approved = False
		type = request.POST.get("type")
		print(request.POST)
		print(approved)
		if type == "H":
			if approved:
				print("Approved")
				leave_obj.is_hod_approved = True
				leave_obj.save()
				messages.success(request,f"You have approved this leave request for {leave_obj.lecturer.user.get_full_name()}")
			else:
				leave_obj.leave_status = "Declined"
				leave_obj.save()
				#send mail
				send_mail("Leave request",f"Sorry to inform you. But your leave request for a {leave_obj.leave_type} for {leave_obj.duration} has been declined by the head of department.","Links2webcontact@gmail.com",[leave_obj.lecturer.user.email,])
				messages.warning(request,f"You declined this leave request  for {leave_obj.lecturer.user.get_full_name()}")
				
			return redirect("hod_landing_page")
		elif type == "D":
			if approved:
				leave_obj.is_dean_approved = True
				leave_obj.save()
				messages.success(request,f"You have approved this leave request  for {leave_obj.lecturer.user.get_full_name()}")
			else:
				leave_obj.leave_status = "Declined"
				leave_obj.save()
				messages.warning(request,f"You declined this leave request for {leave_obj.lecturer.user.get_full_name()}")
				#send mail
				send_mail("Leave request",f"Sorry to inform you. But your leave request for a {leave_obj.leave_type} for {leave_obj.duration} has been declined by the Dean.","Links2webcontact@gmail.com",[leave_obj.lecturer.user.email,])
			return redirect("dean_landing_page")
		elif type == "W":
			if approved:
				leave_obj.is_welfare_approved = True
				leave_obj.leave_status = "Approved"
				leave_obj.save()
				messages.success(request,f"You have approved this leave request  for {leave_obj.lecturer.user.get_full_name()}")
				send_mail("Leave request",f"Congratulations. We are happy to tell you that your leave request for a {leave_obj.leave_type} for {leave_obj.duration} has been approved.","Links2webcontact@gmail.com",[leave_obj.lecturer.user.email,])
			else:
				leave_obj.leave_status = "Declined"
				leave_obj.save()
				messages.warning(request,f"You declined this leave request for {leave_obj.lecturer.user.get_full_name()}")
				send_mail("Leave request",f"Sorry to inform you. But your leave request for a {leave_obj.leave_type} for {leave_obj.duration} has been declined by the welfare.","Links2webcontact@gmail.com",[leave_obj.lecturer.user.email,])
				#send mail
			return redirect("welfare_landing_page")


			
def hod_landing_page(request):
	type = "H"
	current_user = request.user.head_of_department
	leaves = current_user.School.school_leave.all()
	for leave in leaves:
		if leave.leave_status != "Pending" and leave.is_hod_approved == False:
			messages.warning(request,f"You declined {leave.lecturer.user.get_full_name()} {leave.leave_type} for {leave.duration}.")
	
		elif leave.is_hod_approved:
			messages.success(request,f"You approved {leave.lecturer.user.get_full_name()} {leave.leave_type} for {leave.duration}.")
	
	return render(request,"leave_management/landing_page.html",{"type":type,"current_user":current_user,})	
	
def dean_landing_page(request):
	type = "D"
	current_user = request.user.dean
	leaves = current_user.School.school_leave.all()
	for leave in leaves:
		if leave.leave_status != "Pending" and leave.is_hod_approved == True and leave.is_dean_approved == False:
			messages.warning(request,f"You declined {leave.lecturer.user.get_full_name()} {leave.leave_type} for {leave.duration}.")
	
		elif leave.is_dean_approved:
			messages.success(request,f"You approved {leave.lecturer.user.get_full_name()} {leave.leave_type} for {leave.duration}.")
	
	return render(request,"leave_management/landing_page.html",{"type":type,"current_user":current_user,})
	
def welfare_landing_page(request):
	type = "W"
	current_user = request.user.welfare
	leaves = current_user.School.school_leave.all()
	for leave in leaves:
		if leave.leave_status == "Declined":
			messages.warning(request,f"The leave for  {leave.lecturer.user.get_full_name()} {leave.leave_type} for {leave.duration} has been declined.")
	
		elif leave.is_welfare_approved:
			messages.success(request,f"The leave for  {leave.lecturer.user.get_full_name()} {leave.leave_type} for {leave.duration} has been fully approved.")
	
	return render(request,"leave_management/landing_page.html",{"type":type,"current_user":current_user,})
			
	
	
class add_school(SuccessMessageMixin,CreateView):
	template_name = "leave_management/add_page.html"
	model = School
	success_url = reverse_lazy("Add_school")
	form_class = SchoolForm
	success_message = "School added successfully"
	extra_context = {"School":True}

class add_Lecturer(CreateView):
	template_name = "leave_management/add_page.html"
	model = Lecturer
	success_url = reverse_lazy("Add_lecturer")
	form_class = Lecturer_form
	def get_context_data(self,**kwargs):
		if "userform" not in kwargs.keys():
			kwargs["userform"] = UserCreationForm()
		if "form" not in kwargs.keys():
			kwargs["form"] = self.form_class()

		return kwargs
	def form_valid(self,form):
		user = UserCreationForm(self.request.POST)
		print(dir(self.request.user))
		
		if user.is_valid():
			user = user.save()
			user.first_name = self.request.POST.get("first_name")
			user.last_name = self.request.POST.get("last_name")
			user.email = self.request.POST.get("email")
			user.save()
		
			if form.is_valid():
				form = form.save(commit=False)
				form.user = user
				form.save()
				messages.success(self.request,"Lecturer has been added successfully")
				return redirect(self.success_url)
			else:
				user.delete()
				return self.render_to_response(self.get_context_data(form=form,userform=user))
		else:
			return self.render_to_response(self.get_context_data(form=form,userform=user))
	
	
		
class add_Hod(CreateView):
	template_name = "leave_management/add_page.html"
	model = Head_of_Department
	success_url = reverse_lazy("Add_hod")
	form_class = Head_of_Department_form
	def get_context_data(self,**kwargs):
		if "userform" not in kwargs.keys():
			kwargs["userform"] = UserCreationForm()
		if "form" not in kwargs.keys():
			kwargs["form"] = self.form_class()
		return kwargs
	def form_valid(self,form):
		user = UserCreationForm(self.request.POST)
		if user.is_valid():
			user = user.save()
			user.first_name = self.request.POST.get("first_name")
			user.last_name = self.request.POST.get("last_name")
			user.email = self.request.POST.get("email")
			user.save()
			if form.is_valid():
				form = form.save(commit=False)
				form.user = user
				form.save()
				messages.success(self.request,"H.O.D has been added successfully")
				return redirect(self.success_url)
			else:
				user.delete()
				return self.render_to_response(self.get_context_data(form=form,userform=user))
		else:
			return self.render_to_response(self.get_context_data(form=form,userform=user))
	
	
		
class add_Dean(CreateView):
	template_name = "leave_management/add_page.html"
	model = Dean
	success_url = reverse_lazy("Add_dean")
	form_class = Dean_form
	def get_context_data(self,**kwargs):
		if "userform" not in kwargs.keys():
			kwargs["userform"] = UserCreationForm()
		if "form" not in kwargs.keys():
			kwargs["form"] = self.form_class()

		return kwargs
	def form_valid(self,form):
		user = UserCreationForm(self.request.POST)
		if user.is_valid():
			user = user.save()
			user.first_name = self.request.POST.get("first_name")
			user.last_name = self.request.POST.get("last_name")
			user.email = self.request.POST.get("email")
			user.save()
			if form.is_valid():
				form = form.save(commit=False)
				form.user = user
				form.save()
				messages.success(self.request,"Dean has been added successfully")
				return redirect(self.success_url)
			else:
				user.delete()
				return self.render_to_response(self.get_context_data(form=form,userform=user))
		else:
			return self.render_to_response(self.get_context_data(form=form,userform=user))
	
	
		
class add_Welfare(CreateView):
	template_name = "leave_management/add_page.html"
	model = Welfare
	success_url = reverse_lazy("Add_welfare")
	form_class = Welfare_form
	def get_context_data(self,**kwargs):
		if "userform" not in kwargs.keys():
			kwargs["userform"] = UserCreationForm()
		if "form" not in kwargs.keys():
			kwargs["form"] = self.form_class()

		return kwargs
	def form_valid(self,form):
		user = UserCreationForm(self.request.POST)
		if user.is_valid():
			user = user.save()
			user.first_name = self.request.POST.get("first_name")
			user.last_name = self.request.POST.get("last_name")
			user.email = self.request.POST.get("email")
			user.save()
			if form.is_valid():
				form = form.save(commit=False)
				form.user = user
				form.save()
				messages.success(self.request,"Welfare has been added successfully")
				return redirect(self.success_url)
			else:
				user.delete()
				return self.render_to_response(self.get_context_data(form=form,userform=user))
		else:
			return self.render_to_response(self.get_context_data(form=form,userform=user))
	
	
		
	
			
		
		
		
		
		
		
		

