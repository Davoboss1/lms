from django.db import models
from django.forms import ModelForm,widgets
from django.contrib.auth.models import User

# Create your models here.
class School(models.Model):
	School_Name = models.CharField(max_length=250,)
	School_Address = models.CharField(max_length=250)
	def __str__(self):
		return self.School_Name

Marital_Choices = (('Single','Single'),('Married','Married'),('Divorced','Divorced'),('Widowed','Widowed'),)
sex_choices = (
	("Male","Male"),
	("Female","Female"),	)

class SchoolForm(ModelForm):
	class Meta:
		model = School
		fields = ("__all__")

class base_data(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	date_of_birth = models.DateField()
	sex = models.CharField(max_length=6,choices=sex_choices)
	phone_no = models.CharField(max_length=20)
	Marital_Status = models.CharField(max_length=10,choices=Marital_Choices)
	def __str__(self):
		return self.user.get_full_name()
	class Meta:
		abstract = True

class Dean(base_data):
	School = models.OneToOneField(School,on_delete=models.CASCADE)

class Dean_form(ModelForm):
	class Meta:
		model = Dean
		fields = ('__all__')
		exclude = ("user",)
		widgets = {"date_of_birth":widgets.DateInput(attrs={"type":"date"}),"phone_no":widgets.TextInput(attrs={"type":"tel"}),}
	
class Welfare(base_data):
	School = models.OneToOneField(School,on_delete=models.CASCADE)

class Welfare_form(ModelForm):
	class Meta:
		model = Welfare
		fields = ('__all__')
		exclude = ("user",)
		widgets = {"date_of_birth":widgets.DateInput(attrs={"type":"date"}),"phone_no":widgets.TextInput(attrs={"type":"tel"}),}
	
class Head_of_Department(base_data):
	School = models.OneToOneField(School,on_delete=models.CASCADE)
	
class Head_of_Department_form(ModelForm):
	class Meta:
		model = Head_of_Department
		fields = ('__all__')
		exclude = ("user",)
		widgets = {"date_of_birth":widgets.DateInput(attrs={"type":"date"}),"phone_no":widgets.TextInput(attrs={"type":"tel"}),}
	
	
class Lecturer(base_data):
	School = models.ForeignKey(School,on_delete=models.CASCADE)
	
class Lecturer_form(ModelForm):
	class Meta:
		model = Lecturer
		fields = ('__all__')
		exclude = ("user",)
		widgets = {"date_of_birth":widgets.DateInput(attrs={"type":"date"}),"phone_no":widgets.TextInput(attrs={"type":"tel"}),}
	
class leave_request(models.Model):
	duration_choices = (
	("1 week","1 week"),
	("2 weeks","2 weeks"),
	("3 weeks","3 weeks"),
	("1 month","1 month"),
	("2 months","2 months"),
	("3 months","3 months"),
	("6 months","6 months"),
	)
	leave_type_choices = (
	("Emergency Leave","Emergency Leave"),
	("Sickness Leave","Sickness Leave"),
	("Maternity Leave","Maternity Leave"),
	("Vacational Leave","Vacational Leave"),
	("Annual Leave","Annual Leave"),
	)
	leave_status_choices = (
	("Pending","Pending"),
	("Declined","Declined"),
	("Approved","Approved"),
	)
	school = models.ForeignKey(School,on_delete=models.CASCADE,related_name="school_leave")
	lecturer = models.ForeignKey(Lecturer,on_delete=models.CASCADE)
	duration = models.CharField(max_length=20,choices = duration_choices)
	leave_type = models.CharField(max_length=50,choices=leave_type_choices)
	leave_message = models.CharField(max_length=200,null=True,blank=True)
	leave_status = models.CharField(max_length=10,choices = leave_status_choices,default="Pending")
	is_hod_approved = models.BooleanField(default=False)
	is_dean_approved = models.BooleanField(default=False)
	is_welfare_approved = models.BooleanField(default=False)
	
	@property
	def is_fully_approved(self):
		if self.is_hod_approved == True and self.is_dean_approved == True and self.is_welfare_approved == True:
			return True
		else:
			return False
	def __str__(self):
		return f"{self.lecturer} leave request."

class Leave_Form(ModelForm):
	class Meta:
		model = leave_request
		fields = ("duration","leave_type","leave_message")
		
		widgets = {"leave_message":widgets.Textarea(),}
	
	
	