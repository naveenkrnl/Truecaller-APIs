from django.contrib.auth import get_user_model
from django.db.models import Q
User=get_user_model()

# rest_framework
from rest_framework import permissions, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

# relative import of serializer
from .serializers import UserModelSerializer, PersonalContactsSerializer

# importing Model
from data.models import PersonalContacts

# Search View Handler API ENDPOINT
class DataListSearchAPIView(APIView):
    def get(self,request,*args, **kwargs):
        if 'p' in request.GET:
            search_phone_number = request.GET['p']
            qs = User.objects.filter(phone_number__iexact=search_phone_number)
            if qs.count()==1:
                serializer = UserModelSerializer(qs, many=True)
                return Response(serializer.data)
            else:
                qs = PersonalContacts.objects.filter(phone_number__iexact=search_phone_number)
                print(qs)
                if qs.count() > 0:
                    serializer = PersonalContactsSerializer(qs, many=True)
                    data={
                        "message":"Number is not registered",
                        "data":serializer.data
                    }
                    return Response(data)
        if 'name' in request.GET:
            search_name = request.GET['name']
            user_qs = User.objects.filter(
                Q(name__startswith=search_name)|
                Q(name__icontains = search_name)
            ).distinct()
            p_qs = PersonalContacts.objects.filter(
                Q(name__startswith=search_name)|
                Q(name__icontains = search_name)
            ).distinct()
            serializer1 = UserModelSerializer(user_qs,many=True)
            serializer2 = PersonalContactsSerializer(p_qs, many=True)
            data={
                'registered_users':serializer1.data,
                'personal_contacts':serializer2.data
            }
            return Response(data)
        return Response({"data":"Search something by name (?name=)  or phone_number (?p=)"},status=200)

# detail view of User model
class UserDetailAPIView(APIView):

    def get(self,request,pk,*args,**kwargs):
        qs=User.objects.get(id=pk)
        serializer = UserModelSerializer(qs)

        # to display email or not
        # user is already registered
        # now check whether searching user is in this user's contact list
        check_qs = PersonalContacts.objects.filter(
            Q(user=qs) &
            Q(phone_number__icontains=request.user.phone_number)
        )
        if check_qs.count()>0:
            data={
                "data":serializer.data,
                "email":qs.email
            }
        else:
            data=serializer.data
        return Response(data)

    def post(self,request,pk,*args,**kwargs):
        q=User.objects.get(id=pk)
        q.spam_count+=1
        q.save()
        serializer = UserModelSerializer(q)
        data={
            "data":serializer.data,
            "message":"{} marked as spam.".format(q.name)
        }
        return Response(data,status=200)


# detail view of Personal contacts model
class PersonalContactsDetailAPIView(APIView):

    def get(self,request,pk,*args,**kwargs):
        qs=PersonalContacts.objects.get(id=pk)
        serializer = PersonalContactsSerializer(qs)
        return Response(serializer.data)

    def post(self,request,pk,*args,**kwargs):
        q=PersonalContacts.objects.get(id=pk)
        q.spam_count+=1
        q.save()
        serializer = PersonalContactsSerializer(q)
        data={
            "data":serializer.data,
            "message":"{} marked as spam.".format(q.name)
        }
        return Response(data,status=200)
