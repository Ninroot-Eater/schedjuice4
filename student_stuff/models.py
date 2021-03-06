from operator import mod
from ms_stuff.graph_wrapper.user import UserMS
from ms_stuff.exceptions import MSException

from ms_stuff.graph_wrapper.group import GroupMS

from work_stuff.models import Work
from django.db import models
from schedjuice4.models import CustomModel

from django.core.validators import RegexValidator

from datetime import date
from schedjuice4.id_utils import id_creator


# Create your models here.

class Student(CustomModel):

    email =  models.EmailField(unique=True)
    ms_id = models.CharField(max_length=256, unique=True)
    gmail = models.EmailField(unique=True,null=True)
    student_id = models.CharField(unique=True, null=True, max_length=256)

    password = models.CharField(max_length=256)
    dname = models.CharField(max_length=128, default="Display Name")
    ename = models.CharField(max_length=128, default="Nickname")
    description = models.TextField(default="Description...")
    status = models.CharField(max_length=128, default="active")
    dob = models.DateField(default=date(2000,1,1))
    gender = models.CharField(max_length=32, default="")
    ph_num = models.CharField(max_length=32,default="", validators=[RegexValidator(r'^\d{1,20}$')])
    profile_pic = models.ImageField(default="stu_profile/default.jpg", upload_to="stu_profile")
    cover_pic = models.ImageField(default="stu_cover/default.jpg",upload_to="stu_cover")
    card_pic = models.ImageField(default="stu_card/default.jpg", upload_to="stu_card")

    house_num = models.CharField(max_length=128, default="")
    street = models.CharField(max_length=128, default="")
    township = models.CharField(max_length=128, default="")
    city = models.CharField(max_length=128, default="")
    region = models.CharField(max_length=128, default="")
    country = models.CharField(max_length=16, default="mm")
    postal_code = models.CharField(max_length=12, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    read_only_fields = {
        "SDM":[],
        "ADM":["ms_id", "student_id"],
        "USR":[
            "student_id",
            "email",
            "ms_id",
            "gmail",
            "password",
            "dname",
            "ename",
            "dob",
            "gender",
            "ph_num",
            "house_num",
            "street",
            "township",
            "city",
            "region",
            "country",
            "postal_code"
        ]
             
    } 

    excluded_fields = {
        "SDM":[],
        "ADM":[],
        "USR":["house_num","street","township","city","region","postal_code"]
    }

    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = id_creator(Student.objects.exclude(student_id__isnull=True).all())
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not kwargs.pop("silent",None):
            res = UserMS(self.email).delete()
            if res.status_code not in range(199,300):
                raise MSException(detail=res.json())


        return super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"
        ordering = ["id"]


class StudentWork(CustomModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    read_only_fields = {
        "SDM":[],
        "ADM":["created_at","updated_at"],
    }    

    def delete(self, *args, **kwargs):
        if not kwargs.get("silent"):
            res = GroupMS(self.work.ms_id).remove_member(self.student.ms_id,"members")
            if res.status_code not in range(199,300):
                    raise MSException(detail=res.json())

        return super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "student_work"
        verbose_name_plural = "student_works"
        ordering = ["id"]




