from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('login',LoginView.as_view(),name="login"),
    path('user/login',UserLoginView.as_view(),name="user-login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('user/logout',UserLogoutView.as_view(),name="user-logout"),
    path('manager',ManagerDashboardView.as_view(),name="manager-index"),
    path('manager/otheraccounts',ManagerOtherAccountListView.as_view(),name="manager-otheraccount"),
    path('manager/otheraccounts/add',ManagerOtherAccountCreateView.as_view(),name="manager-otheraccount-add"),
    path('manager/account/add',ManagerAccountAddView.as_view(),name="manager-account-add"),
    path('manager/account/<int:pk>',ManagerAccountDetailView.as_view(),name="manager-account-view"),
    path('manager/account/<int:pk>/edit',ManagerAccountEditView.as_view(),name="manager-account-edit"),
    path('manager/staffs',ManagerStaffListView.as_view(),name="manager-staff-list"),
    path('manager/staffs/add',ManagerStaffCreateView.as_view(),name="manager-staff-add"),
    path('manager/branches',ManagerBranchListView.as_view(),name="manager-branch-list"),
    path('manager/branches/add',ManagerBranchCreateView.as_view(),name="manager-branch-add"),
    path('manager/<int:id>/notice',ManagerNotificationCreateView.as_view(),name="manager-notice-add"),
    path('manager/feedbacks',ManagerFeedbackListView.as_view(),name="manager-feedbacks"),

    #user
    path('user',UserIndexView.as_view(),name = "user-index"),
    path('user/account',UserAccountProfileView.as_view(),name = "user-account"),
    path('user/transfer',UserFundTransferView.as_view(),name = "user-transfer"),
    path('user/notifications',UserNotificationListView.as_view(),name = "user-notification"),
    path('user/feedback',UserFeedbackView.as_view(),name = "user-feedback"),
    path('user/statement',UserStatementView.as_view(),name = "user-statement"),

    #cashier
    path('cashier',CashierIndexView.as_view(),name="cashier-index"),
]
