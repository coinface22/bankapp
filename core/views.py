from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Deposit,Withdraw,User,Transfer,Branch,Account,Feedback,Notification,BlockedTransfer, OtherAccount
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import login, logout
from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView
from .forms import LoginForm, AccountAddForm
from django.db.models import Q
from django.contrib import messages
# Create your views here.


class ManagerRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.usertype == "manager"

class CashierRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.usertype == "cashier"

class UserRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.usertype == "user"

class LoginView(FormView):
    form_class = LoginForm
    template_name = "admin-login.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

    def form_valid(self, form):
        user = form.get_user()
        if user.usertype == "manager":
            self.success_url = "manager"
        elif user.usertype == "cashier":
            self.success_url = "cashier"
        else:
            self.success_url = "user"
        login(self.request,user)
        return super().form_valid(form)
class UserLoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

    def form_valid(self, form):
        user = form.get_user()
        if user.usertype == "manager":
            self.success_url = "/manager"
        elif user.usertype == "cashier":
            self.success_url = "/cashier"
        else:
            self.success_url = "/user"
        login(self.request,user)
        return super().form_valid(form)

def index(request):
    return redirect(reverse("user-login"))
class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logout SuccessFul")
        return redirect(reverse("login"))
class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logout SuccessFul")
        return redirect(reverse("user-login"))

class ManagerDashboardView(ManagerRequiredMixin,ListView):
    model = Account
    template_name = "manager/index.html"

    def get_queryset(self):
        return Account.objects.all().order_by("-date_created")
    def post(self,request,*args,**kwargs):
        acc_id = request.POST.get("acc_id")
        password = request.POST.get("password")
        user = User.objects.get(id = self.request.user.id)
        if not user.check_password(password):
            messages.error(self.request,"Password is Incorrect")
            return redirect(reverse("manager-index"))
        account = Account.objects.filter(id = acc_id)
        if not account.exists():
            messages.error(self.request,"Account Does not exist")
            return redirect(reverse("manager-index"))
        account = account.first()
        account.user.delete()
        messages.success(request,"Account Deleted Successfully")
        return redirect(reverse("manager-index"))

class ManagerAccountDetailView(ManagerRequiredMixin,DetailView):
    model = Account
    template_name = "manager/account-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context['object']
        if BlockedTransfer.objects.filter(account = obj).exists():
            blocked = True
        else:
            blocked = False
        context['blocked'] = blocked
        return context
    def post(self,request,*args,**kwargs):
        id = kwargs['pk']
        account = get_object_or_404(Account, pk = id)
        message = request.POST.get("message")
        action = request.POST.get("action")
        if action == "block":
            BlockedTransfer.objects.create(account = account,message = message)
            messages.success(request,"Account Transfer Blocked Successfully")
        else:
            if BlockedTransfer.objects.filter(account = account).exists():
                blockedtf = BlockedTransfer.objects.filter(account = account).first()
                blockedtf.delete()
                messages.success(request,"Account Transfer Unblocked Successfully")
        return redirect(reverse("manager-account-view",kwargs={'pk':id}))

class ManagerAccountAddView(ManagerRequiredMixin,FormView):
    form_class = AccountAddForm
    template_name = "manager/account-add.html"
    success_url = reverse_lazy("manager-index")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['branches'] = Branch.objects.all().order_by("name")
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = User.objects.create(email = email, password = password)
        obj = form.save(commit = False)
        obj.user = user
        obj.save()
        messages.success(self.request,"Account Created Successfully")
        return super().form_valid(form)

class ManagerStaffListView(ManagerRequiredMixin, ListView):
    model = User
    template_name = "manager/staff-list.html"

    def get_queryset(self):
        return User.objects.filter(Q(usertype = "manager")| Q(usertype = "cashier")).exclude(id = self.request.user.id)
    def post(self,request,*args,**kwargs):
        acc_id = request.POST.get("acc_id")
        print(acc_id)
        password = request.POST.get("password")
        user = User.objects.get(id = self.request.user.id)
        if not user.check_password(password):
            messages.error(self.request,"Password is Incorrect")
            return redirect(reverse("manager-staff-list"))
        account = User.objects.filter(id = int(acc_id))
        if not account.exists():
            messages.error(self.request,"Staff Does not exist")
            return redirect(reverse("manager-staff-list"))
        account = account.first()
        account.delete()
        messages.success(request,"Staff Deleted Successfully")
        return redirect(reverse("manager-staff-list"))

class ManagerStaffCreateView(ManagerRequiredMixin,View):
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        usertype = "cashier"

        User.objects.create(email = email,password = password, usertype = usertype)
        messages.success(request,str(usertype.capitalize())+" Staff Created")
        return redirect(reverse("manager-staff-list"))

class ManagerBranchListView(ManagerRequiredMixin, ListView):
    model = Branch
    template_name = "manager/branch-list.html"

    def get_queryset(self):
        return Branch.objects.all()
    def post(self,request,*args,**kwargs):
        branch_id = request.POST.get("branch_id")

        password = request.POST.get("password")
        user = User.objects.get(id = self.request.user.id)
        if not user.check_password(password):
            messages.error(self.request,"Password is Incorrect")
            return redirect(reverse("manager-branch-list"))
        account = Branch.objects.filter(id = int(branch_id))
        if not account.exists():
            messages.error(self.request,"Branch Does not exist")
            return redirect(reverse("manager-branch-list"))
        account = account.first()
        account.delete()
        messages.success(request,"Branch Deleted Successfully")
        return redirect(reverse("manager-branch-list"))

class ManagerBranchCreateView(ManagerRequiredMixin,View):
    def post(self,request):
        name = request.POST['name']
        number = request.POST['number']
        

        Branch.objects.create(name = name,number = number)
        messages.success(request,"Branch Created Successfully")
        return redirect(reverse("manager-branch-list"))

class ManagerOtherAccountListView(ManagerRequiredMixin, ListView):
    model = OtherAccount
    template_name = "manager/other-account-list.html"

    def get_queryset(self):
        return OtherAccount.objects.all().order_by("-date_created")
    def post(self,request,*args,**kwargs):
        account_id = request.POST.get("acc_id")

        password = request.POST.get("password")
        user = User.objects.get(id = self.request.user.id)
        if not user.check_password(password):
            messages.error(self.request,"Password is Incorrect")
            return redirect(reverse("manager-otheraccount"))
        account = OtherAccount.objects.filter(id = int(account_id))
        if not account.exists():
            messages.error(self.request,"Account Does not exist")
            return redirect(reverse("manager-otheraccount"))
        account = account.first()
        account.delete()
        messages.success(request,"Account Deleted Successfully")
        return redirect(reverse("manager-otheraccount"))

class ManagerOtherAccountCreateView(ManagerRequiredMixin,CreateView):
    model = OtherAccount
    fields = "__all__"
    template_name = "manager/other-account-list.html"
    success_url = reverse_lazy("manager-otheraccount")
    


class ManagerNotificationCreateView(ManagerRequiredMixin,View):
    def get(self,request,id):
        user =  get_object_or_404(User, id = id)
        return render(request,"manager/send-notice.html",{"user":user})
    def post(self,request,id):
        message = request.POST['message']
        user = get_object_or_404(User, id = id)
        Notification.objects.create(user = user, message = message, fromm = request.user)
        messages.success(request,"Notification Sent.")
        return redirect(reverse("manager-index"))

class ManagerFeedbackListView(ManagerRequiredMixin,ListView):
    model = Feedback
    template_name = "manager/feedback.html"
    def get_queryset(self):
        return Feedback.objects.all().order_by("-date_created")
    def post(self,request,*args,**kwargs):
        feedback_id = request.POST.get("feedback_id")
        print(feedback_id)
        password = request.POST.get("password")
        user = User.objects.get(id = self.request.user.id)
        if not user.check_password(password):
            messages.error(self.request,"Password is Incorrect")
            return redirect(reverse("manager-feedbacks"))
        feedback = Feedback.objects.filter(id = feedback_id)
        if not feedback.exists():
            messages.error(self.request,"Feedback Does not exist")
            return redirect(reverse("manager-feedbacks"))
        feedback = feedback.first()
        feedback.delete()
        messages.success(request,"Feedback Deleted Successfully")
        return redirect(reverse("manager-feedbacks"))
class UserIndexView(UserRequiredMixin,View):
    def get(self,request):
        user = request.user
        notification = Notification.objects.filter(user = user).order_by("-date_sent").first()
        return render(request,"user/index.html",{'notification':notification})

class UserAccountProfileView(UserRequiredMixin,View):
    def get(self,request):
        user = request.user
        account = get_object_or_404(Account, user = user)
        return render(request,"user/profile.html",{'user':user,'account':account})

class UserFundTransferView(UserRequiredMixin,View):
    def get(self,request):
        user = request.user
        transfers = Transfer.objects.filter(sent_from = request.user.account).order_by("-date_created")
        acc_number = request.GET.get("acc_no")
        if acc_number:
            account = Account.objects.filter(account_number = acc_number).exclude(user = user)
            if account.exists():
                account = account.first()
                
            else:
                account = OtherAccount.objects.filter(account_number = acc_number)
                if account.exists():
                    account = account.first()
                else:
                    messages.error(request,"Account number is Invalid")
        else:
            account = None
        return render(request,"user/transfer.html",{'account':account,'transfers':transfers})
    def post(self, request):
        account_id = request.POST.get("account_id")
        transfers = Transfer.objects.filter(sent_from = request.user.account).order_by("-date_created")
        useraccount = Account.objects.get(user = request.user)
        amount = request.POST.get("amount")
        try:
            account = Account.objects.get(id = account_id)
           
            blockedtf = BlockedTransfer.objects.filter(account = useraccount)
            if blockedtf.exists():
                blockedtf = blockedtf.first()
                messages.error(request,"Funds transfer blocked -- "+blockedtf.message)
                return render(request,"user/transfer.html",{'account':account,'transfers':transfers})
            if int(amount) > int(useraccount.balance):
                messages.error()
                return render(request,"user/transfer.html",{'account':account,'transfers':transfers})
            
            useraccount.balance = str(int(useraccount.balance) - int(amount))
            account.balance = str(int(account.balance) + int(amount))
            Transfer.objects.create(sent_from = request.user.account, sent_to = account, amount = int(amount))
            account.save()
            useraccount.save()
        except Exception:
            account = OtherAccount.objects.get(id = account_id)
            useraccount.balance = str(int(useraccount.balance) - int(amount))
            account.balance = str(int(account.balance) + int(amount))
            account.save()
            useraccount.save()
        messages.success(request,"Transfer Successful")
        return redirect(reverse("user-transfer"))

class UserNotificationListView(UserRequiredMixin,ListView):
    model = Notification
    template_name = "user/notification.html"

    def get_queryset(self):
        return Notification.objects.filter(user =  self.request.user).order_by("-date_sent")

class UserFeedbackView(UserRequiredMixin,CreateView):
    model = Feedback
    template_name = "user/feedback.html"
    fields = ['message']
    success_url = reverse_lazy("user-feedback")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request,"Feedback Successful")
        return super().form_valid(form)

from itertools import chain
class UserStatementView(UserRequiredMixin,ListView):
    template_name = "user/statement.html"

    def get_queryset(self):
        withdraw_list = Withdraw.objects.filter(account = self.request.user.account)
        deposit_list = Deposit.objects.filter(account = self.request.user.account)
        transfer_list = Transfer.objects.filter(Q(sent_from = self.request.user.account)|Q(sent_to = self.request.user.account))
        result_list = list(sorted(chain(withdraw_list,deposit_list, transfer_list),key=lambda instance: instance.date_created, reverse=True))
        return result_list

class CashierIndexView(CashierRequiredMixin,View):
    def get(self,request):
        acc_no = request.GET.get("acc_no")
        account = None
        if acc_no:
            account = Account.objects.filter(account_number = acc_no)
            if account.exists():
                account = account.first()
            else:
                messages.error(request,"Account Does not Exist")
                
        return render(request,"cashier/index.html",{'account':account})
    def post(self,request):
        acc_no = request.POST.get('acc_no')
        transaction_type = request.POST.get("transaction_type")
        description = request.POST.get("description")
        amount = request.POST.get("amount")
        account = None
        if acc_no:
            account = Account.objects.filter(account_number = acc_no)
            if account.exists():
                account = account.first()
            else:
                messages.error(request,"Account Does not Exist")
                return redirect(reverse("cashier-index"))
        else:
            messages.error(request,"Account Number not specified")
            return redirect(reverse("cashier-index"))
        if transaction_type == "deposit":
            Deposit.objects.create(account = account,amount = int(amount), description = description, status = "success")
            account.balance = account.balance + int(amount)
            account.save()
            messages.success(request,"Deposit Successful")
        elif transaction_type == "withdraw":
            if account.balance >= int(amount):
                Withdraw.objects.create(account = account,amount = int(amount), description = description, status = "success")
                account.balance = account.balance - int(amount)
                account.save()
                messages.success(request,"Withdrawal Successful")
            else:
                messages.error(request,"Insufficient fund")
                return redirect(reverse("cashier-index"))
        else:
            messages.error(request,"Unknown Transaction Type")
            return redirect(reverse("cashier-index"))
        
        return redirect(reverse("cashier-index"))