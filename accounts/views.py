from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser, Company
from accounts.permissions import IsAdminOrCreateOnly, IsCompanyOwner, IsCompanyEmployee, \
    IsProfileOwnerOrAdmin
from accounts.serializers import UserSerializer, CompanySerializer, UpdateWorkerSerializer


class AdminUserCreation(ModelViewSet):
    """
    View for company owner registration
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrCreateOnly, )


class CompanyView(ModelViewSet):
    """
    Allow GET/PUT/POST/DELETE methods for company management for owner
    """
    serializer_class = CompanySerializer
    permission_classes_by_action = {'create': [IsCompanyOwner],
                                    'update': [IsCompanyOwner],
                                    'destroy': [IsCompanyOwner],
                                    'retrieve': [IsCompanyOwner],
                                    'partial_update': [IsCompanyOwner],
                                    'list': [IsCompanyEmployee]}

    def get_queryset(self):
        """ Get only """
        current_user = self.request.user

        if current_user is None:
            queryset = None
        else:
            queryset = Company.objects.filter(name=current_user.user_company.name)

        return queryset

    def get_permissions(self):
        try:
            """ return permission_classes depending on `action` """
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            """ action is not set return default permission_classes """
            return [permission() for permission in self.permission_classes]


class WorkersViewSet(ModelViewSet):
    """ Create, get list of company workers"""
    serializer_class = UserSerializer
    permission_classes = (IsCompanyOwner, )
    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        current_user = self.request.user
        current_user_company = Company.objects.get(owner=current_user)

        if current_user is None or current_user_company is None:
            queryset = None
        else:
            queryset = CustomUser.objects.filter(user_company=current_user_company)

        return queryset


class UpdateProfileView(UpdateAPIView):
    """ Update company workers"""
    queryset = CustomUser.objects.all()
    serializer_class = UpdateWorkerSerializer
    permission_classes = (IsProfileOwnerOrAdmin, )





