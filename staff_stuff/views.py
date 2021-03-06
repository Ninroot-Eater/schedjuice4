
from schedjuice4.generic_views import GeneralDetails, GeneralList
from rest_framework.permissions import IsAuthenticated
from .models import Department, Job, Staff, Tag, StaffTag, StaffDepartment
from .serializers import (
                        DepartmentSerializer, StaffSerializer,
                        StaffTagSerializer, TagSerializer,
                        StaffDepartmentSerializer, JobSerializer)

from role_stuff.permissions import RegistrationPhase,IsADMOrReadOnly, IsOwnerOrReadOnly, StatusCheck


# Create your views here.


class StaffList(GeneralList):
    
    model = Staff
    serializer = StaffSerializer
    related_fields = [
        "staffsession_set__session",
        "staffsession_set__role",
        "stafftag_set","staffdepartment_set__job",
        "user_permissions","groups", "role",
        "staffwork_set__work",
        "staffwork_set__role",
        "stafftag_set__tag"

    ]
    permission_classes = [IsAuthenticated,RegistrationPhase, IsADMOrReadOnly]
    

class StaffDetails(GeneralDetails):
    
    model = Staff
    serializer = StaffSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]


class StaffSearch(GeneralList):
    model = Staff
    serializer = StaffSerializer
    permission_classes = [IsAuthenticated, IsADMOrReadOnly]
    related_fields = [
        "staffsession_set__session",
        "staffsession_set__role",
        "stafftag_set","staffdepartment_set__job",
        "user_permissions","groups", "role",
        "staffwork_set__work",
        "staffwork_set__role",
        "stafftag_set__tag"
    ]


    def get(self, request, **kwargs):
        return super().search(request, **kwargs)



class DepartmentList(GeneralList):
    model = Department
    serializer = DepartmentSerializer
    related_fields = [
        "staffdepartment_set__staff",
        "staffdepartment_set__job"
    ]
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]

class DepartmentDetails(GeneralDetails):
    model = Department
    serializer = DepartmentSerializer
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]



class TagList(GeneralList):
    model = Tag
    serializer = TagSerializer
    related_fields = ["stafftag_set__staff"]
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]

class TagDetails(GeneralDetails):
    model = Tag
    serializer = TagSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]



class JobList(GeneralList):
    model = Job
    serializer = JobSerializer
    permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]

class JobDetails(GeneralDetails):
    model = Job
    serializer = JobSerializer
    permission_classes = [IsAuthenticated, StatusCheck, IsADMOrReadOnly]



class StaffTagList(GeneralList):
    model = StaffTag
    serializer = StaffTagSerializer
    related_fields = ["staff","tag"]
    permission_classes = [IsAuthenticated,StatusCheck, IsADMOrReadOnly]

class StaffTagDetails(GeneralDetails):
    model = StaffTag
    serializer = StaffTagSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]



class StaffDepartmentList(GeneralList):
    model = StaffDepartment
    serializer = StaffDepartmentSerializer
    related_fields = ["staff","department","job"]
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]

class StaffDepartmentDetails(GeneralDetails):
    model = StaffDepartment
    serializer = StaffDepartmentSerializer
    permission_classes = [IsAuthenticated, StatusCheck,IsADMOrReadOnly]
