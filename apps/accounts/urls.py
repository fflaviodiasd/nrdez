from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
# router.register(r'users', CustomUserViewSet, basename='users')


urlpatterns = [
    path(r'accounts/', include((router.urls, 'accounts'))),
    path(r'accounts/register/',RegisterNewUser.as_view({'post':'create'}), name='register_user'),
    path(r'accounts/token/', TokenObtainPairViewCustom.as_view(), name='token_obtain_pair'),
    path(r'accounts/token/refresh/', TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path(r'accounts/password_recovery/', EmailRecoveryPassword.as_view(), name='email_password_reset'),
    path(r'accounts/password_recovery/confirm/', ConfirmRecoveryPassword.as_view(), name='email_password_reset_confirm'),
    path(r'accounts/password_recovery/employee/', RecoveryPasswordEmployeeView.as_view(), name='password_recovery_employee'),
    path(r'accounts/logout/', BlacklistRefreshView.as_view(), name="logout"),
    path(r'accounts/<int:id>/complete/', AccountsCompleteViewSet.as_view({'patch':'update'}), name='accounts_complete'),
    path(r'accounts/<int:id>/training/', EmployeeTrainingViewSet.as_view({'get':'list'}),name='accounts_training'),
    path(r'accounts/<int:id>/certificate/',AccountsCertificateListViewSet.as_view({'get':'list'}),name='accounts_certificate_list'),
    path(r'accounts/<int:pk>/provider/',RetrieveProviderUserProfile.as_view({'get':'retrieve'}),name='accounts_provider_retrieve'),
    path(r'cards/', CardInfoView.as_view(), name='card-info')
]