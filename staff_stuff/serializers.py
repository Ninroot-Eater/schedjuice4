import time

from rest_framework import serializers
from schedjuice4.serializers import DynamicFieldsModelSerializer, status_check
from work_stuff.serializers import StaffSessionSerializer

from .models import Department, Staff, Tag, StaffTag, StaffDepartment, Job
from work_stuff.serializers import StaffWorkSerializer
from role_stuff.serializers import RoleOnlySerializer

from ms_stuff.graph_wrapper.tasks import start_user_creation_flow
from ms_stuff.graph_wrapper.group import GroupMS
from ms_stuff.graph_wrapper.user import UserMS

# Only-serializers

class DepartmentOnlySerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Department
        fields = "__all__"

class StaffOnlySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Staff
        fields = "__all__"

class TagOnlySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"



class JobSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Job
        fields = "__all__"



class StaffDepartmentSerializer(DynamicFieldsModelSerializer):
    staff_details = StaffOnlySerializer(source="staff", fields="id,dname,ename,uname,profile_pic,email,card_pic",read_only=True)
    department_details = DepartmentOnlySerializer(source="department", fields="id,name", read_only=True)
    job_details = JobSerializer(source="job",fields="id,title",read_only=True)

    def validate(self, data):
        s = data["staff"]
        d = data["department"]
        obj = StaffDepartment.objects.filter(staff=s,department=d).first()
        if obj is not None:
            raise serializers.ValidationError("Instance already exist.")

        if "is_primary" in data:
            ip = data["is_primary"]
            if ip == True:
                obj = StaffDepartment.objects.filter(staff=s, is_primary=True).first()
                if obj is not None:
                    raise serializers.ValidationError({"is_primary":"There can only be one primary department."})
        return data

    def create(self, data):
        d = data["department"]
        u = data["staff"]
        res = UserMS(u.email).add_to_group(u.ms_id,d.ms_id,"members")
        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json()})

        return super().create(data,)

    class Meta:
        model = StaffDepartment
        fields = "__all__"


class StaffTagSerializer(DynamicFieldsModelSerializer):    
    staff_details = StaffOnlySerializer(source="staff",fields="id,email,dname,ename,uname,profile_pic,card_pic", read_only=True)
    tag_details = TagOnlySerializer(source="tag",fields="id,name,color", read_only=True)
    

    def validate(self, data):
        s = data["staff"]
        t = data["tag"]

        obj = StaffTag.objects.filter(staff=s,tag=t).first()

        if obj is not None:
            raise serializers.ValidationError("Instance already exists.")


        return data

    class Meta:
        model = StaffTag
        fields = "__all__"
        dept=1


class StaffSerializer(DynamicFieldsModelSerializer):
    departments = StaffDepartmentSerializer(source="staffdepartment_set", fields="id,pos,department_details", many=True,read_only=True)
    tags = StaffTagSerializer(source="stafftag_set",fields="id,pos,tag_details", many=True,read_only=True)
    works = StaffWorkSerializer(source="staffwork_set",fields="id,work_details,role_details", many=True, read_only=True)
    sessions = StaffSessionSerializer(source="staffsession_set",fields="id,session_details", many=True, read_only=True)
    role_details = RoleOnlySerializer(source="role",read_only=True)
    
    _gender_lst = [
        "male",
        "female",
        "non-binary",
        "other"
    ]
    _status_lst = [
            "in progress",
            "unapproved",
            "active",
            "retired",
            "on halt"
        ]

    def validate(self, data):
        role = Staff.objects.get(pk=(self.context.get("r").user.id)).role.shorthand
        if data.get("role"):
            if data.get("role").is_specific:
                raise serializers.ValidationError("Cannot assign a specific role to Staff.")
        
            if role == "ADM":
                if data.get("role").shorthand in ["SDM", "ADM"]:
                    raise serializers.ValidationError("ADM can only give USR role.")

        status = data.get("status")
        if not status_check(status, self._status_lst):
            raise serializers.ValidationError({"status":f"Status '{status}' not allowed. Allowed statuses are {self._status_lst}."})

        if data.get("gender"):
            if data.get("gender") not in self._gender_lst:
                raise serializers.ValidationError({"gender":"Gender must be in "+ str(self._gender_lst)})

        return super().validate(data)


    def create(self, validated_data):

        request = self.context.get("r")
        print(validated_data)
        if not self.context.get("silent"):
            
            start_user_creation_flow(request, validated_data,"staff")

        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, data):

        
        
        password = data.pop("password", None)
        if password:
            instance.set_password(password)
        
        instance = super().update(instance,data)
        instance.save()


        return instance

    class Meta:
        model = Staff
        fields = "__all__"
        extra_kwargs = {
            "password":{"write_only":True},
            "ms_id":{"required":False}
        }
        dept = 1


class DepartmentSerializer(DynamicFieldsModelSerializer):
    staff = StaffDepartmentSerializer(source="staffdepartment_set",fields="id,pos,staff_details",many=True,read_only=True)
    department_details = DepartmentOnlySerializer(source="is_under",fields="id,name,shorthand", read_only=True)

    def create(self, data):
        res = GroupMS.create_group(data)
        if res.status_code not in range(199,300):
            raise serializers.ValidationError({"MS_error":res.json(), "step":"creating group"})
        
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
        model = Department
        fields = "__all__"
        extra_kwargs = {
            "ms_id":{"required":False, "read_only":True},
            "channel_id":{"required":False, "read_only":True}
        }
       
       
class TagSerializer(DynamicFieldsModelSerializer):
    staff = StaffTagSerializer(source="stafftag_set", fields="id,pos,staff_details" ,many=True, read_only=True)

    class Meta:
        model = Tag
        fields = "__all__"
        dept=1

