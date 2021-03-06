from ms_stuff.graph_wrapper.config import constants
from schedjuice4.serializers import DynamicFieldsModelSerializer, status_check
from rest_framework import serializers
import time

from .models import Work, StaffWork, Session, StaffSession, Category
from staff_stuff.models import Staff
from role_stuff.serializers import RoleOnlySerializer
             
from ms_stuff.graph_wrapper.group import GroupMS
from ms_stuff.graph_wrapper.user import UserMS
from student_stuff.models import Student, StudentWork

from .free_time_calc import is_free, is_session_collide


class StudentOnlySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Student
        fields = "__all__"


class StudentWorkSerializer(DynamicFieldsModelSerializer):
    student_details = StudentOnlySerializer(source="student",fields="id,email,dname,ename", read_only=True)

    class Meta:
        model = StudentWork
        fields = "__all__"

class CategoryOnlySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"

class StaffOnlySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Staff
        fields = "__all__"

class WorkOnlySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"

class StaffSessionOnlySerializer(DynamicFieldsModelSerializer):
    staff_details = StaffOnlySerializer(source="staff",fields="id,dname,ename,email,uname,profile_pic,card_pic", read_only=True)
    role_details = RoleOnlySerializer(source="role",fields="id,name,shorthand",read_only=True)

    class Meta:
        model = StaffSession
        fields = "__all__"

class SessionSerializer(DynamicFieldsModelSerializer):
    
    staffsessions = StaffSessionOnlySerializer(source="staffsession_set",fields="id,staff_details,role_details",many=True, read_only=True)

    def validate(self, attrs):
        x = super().validate(attrs)
        if attrs.get("time_from") and attrs.get("time_to"):
            if attrs.get("time_from") >= attrs.get("time_to"):
                raise serializers.ValidationError("time_to must be greater than time_from")

        if is_session_collide(attrs.get("time_from"),attrs.get("time_to"),attrs.get("work"),attrs.get("day")):
            raise serializers.ValidationError("Session is colliding with another session of this work.")

        return x

    class Meta:
        model = Session
        fields = "__all__"


class StaffSessionSerializer(DynamicFieldsModelSerializer):
    staff_details = StaffOnlySerializer(source="staff", fields="id,email,dname,ename,uname,profile_pic,card_pic",read_only=True)
    session_details = SessionSerializer(source="session",fields="id,work,day,time_from,time_to", read_only=True)
    role_details = RoleOnlySerializer(source="role", fields="id,name,shorthand,is_specific", read_only=True)


    def validate(self, data): 
        if data.get('role'):
            if not data.get("role").is_specific:
                raise serializers.ValidationError("Cannot assign non-specific role to StaffSession.")

        s = data.get("staff")
        se = data.get("session")
        obj = StaffSession.objects.filter(staff=s,session=se).first()
        if obj:
            raise serializers.ValidationError("Instance already exists.")
        
        obj = StaffWork.objects.filter(staff=s, work=se.work).first()
        if not obj:
            raise serializers.ValidationError("Staff is not related to Session's Work.")

        if not is_free(s,se):
            raise serializers.ValidationError("The staff is not free")

        return data


    class Meta:
        model = StaffSession
        fields = "__all__"



class StaffWorkSerializer(DynamicFieldsModelSerializer):
    staff_details = StaffOnlySerializer(source="staff",fields="id,email,dname,ename,uname,profile_pic,card_pic", read_only=True)
    work_details = WorkOnlySerializer(source="work", fields="id,name,status", read_only=True)
    role_details = RoleOnlySerializer(source="role", fields="id,name,shorthand,is_specific", read_only=True)

    def validate(self, data):
        if data.get('role'):
            if not data.get("role").is_specific:
                raise serializers.ValidationError("Cannot assign non-specific role to StaffWork.")

        s = data.get("staff")
        w = data.get("work")
        obj = StaffWork.objects.filter(staff=s,work=w).first()
        if obj is not None:
            raise serializers.ValidationError("Instance already exists.")
        return super().validate(data)

    def create(self, data):
        w = data["work"]
        u = data["staff"]
        res = UserMS(u.email).add_to_group(u.ms_id,w.ms_id,"owners")
        
        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json()})

        return super().create(data,)

    class Meta:
        model = StaffWork
        fields = "__all__"



class CategorySerializer(DynamicFieldsModelSerializer):
    works = WorkOnlySerializer(source="work_set",read_only=True,many=True)

    class Meta:
        model = Category
        fields = "__all__"



class WorkSerializer(DynamicFieldsModelSerializer):
    staff = StaffWorkSerializer(source="staffwork_set",fields="id,staff_details,role_details" , many=True, read_only=True)
    sessions = SessionSerializer(source="session_set", many=True, read_only=True)
    students = StudentWorkSerializer(source="studentwork_set",many=True, fields="id,student_details", read_only=True)
    category_details = CategoryOnlySerializer(source="category",fields="id,name", read_only=True)
    _status_lst = [
        "pending",
        "active",
        "ready",
        "ended",
        "on halt"
    ]
    def validate(self, data):
        if data.get("valid_from") and data.get("valid_to"):
            if data.get("valid_from") >= data.get("valid_to"):
                raise serializers.ValidationError("valid_from must be less than valid_to.")

        status = data.get("status")
        if not status_check(status, self._status_lst):
            raise serializers.ValidationError({"status":f"Status '{status}' not allowed. Allowed statuses are {self._status_lst}."})

        return super().validate(data) 


    
    def create(self, data):
        res = GroupMS.create_group(data)
        
        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json(), "step":"creating group"})
        
        # get the group id from Graph API which is in the headers.
        # save that together with the crated Work.
        gp_id = res.headers["Content-Location"].split("'")[1::2][0]
        data["ms_id"] = gp_id

        gp = GroupMS(gp_id)
        time.sleep(1.5)
        res = gp.create_channel("Announcement")
        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json(), "step":"creating channel"})
        
        data["channel_id"] = res.json()["id"]

        return super().create(data)


    class Meta:
        model = Work
        fields = "__all__"
        extra_kwargs = {
            "ms_id":{"required":False, "read_only":True},
            "channel_id":{"required":False, "read_only":True}
        }


