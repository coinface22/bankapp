from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('',TemplateView.as_view(template_name = "home/index.html"), name="index"),
    path('banking',TemplateView.as_view(template_name = "home/banking.html"), name="banking"),
    path('loans',TemplateView.as_view(template_name = "home/loans.html"), name="loans"),
    path('services',TemplateView.as_view(template_name = "home/services.html"), name="services"),
    path('why-vacu',TemplateView.as_view(template_name = "home/why-vacu.html"), name="why-vacu"),
    path('learn',TemplateView.as_view(template_name = "home/learn.html"), name="learn"),
    path('for-business',TemplateView.as_view(template_name = "home/for-business.html"), name="for-business"),
    path('become-a-member',TemplateView.as_view(template_name = "home/become-a-member.html"), name="become-a-member"),
    path('careers',TemplateView.as_view(template_name = "home/careers.html"), name="careers"),
    path('faqs',TemplateView.as_view(template_name = "home/faqs.html"), name="faqs"),
    path('contact-us',TemplateView.as_view(template_name = "home/contact-us.html"), name="contact-us"),
    path('accessibility',TemplateView.as_view(template_name = "home/accessibility.html"), name="accessibility"),


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
    path('cashier/transfer',CashierTransferView.as_view(),name="cashier-transfer"),
]
