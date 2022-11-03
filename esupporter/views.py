from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, DeleteView, View
from django.contrib.auth.views import LoginView, LogoutView
from esupporter.forms import LoginForm, SignUpForm, CompanyCreateForm, ESCreateForm, QuestionCreateForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from esupporter.models import Company, Question, ES, User
from django.contrib.messages.views import SuccessMessageMixin

# 自分の登録した会社でなければ戻す
class CompanyPermission(UserPassesTestMixin):
    def test_func(self):
        company = Company.objects.get(id=self.kwargs['pk'])
        return company.user_id == self.request.user.id
    def handle_no_permission(self):
        return redirect("company_list")

# 自分の登録したESでなければ戻す
class ESPermission(UserPassesTestMixin):
    def test_func(self):
        es = ES.objects.get(id=self.kwargs['pk'])
        return es.user_id == self.request.user.id
    def handle_no_permission(self):
        return redirect("company_list")
        


# Create your views here.
class IndexView(TemplateView): 
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Login(LoginView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('mypage')


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'user/logout_done.html'


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "user/signup.html" 
    success_url = reverse_lazy('mypage')

# マイページ
class Mypage(LoginRequiredMixin, TemplateView):
    template_name = "mypage/mypage.html"

# 提出したESを会社ごとに一覧表示
class CompanyListView(LoginRequiredMixin, ListView):
    template_name = 'es_management/company_list.html'
    model = Company
    def get_queryset(self, **kwargs):
        query_set = Company.objects.filter(user_id=self.request.user.id)
        return query_set

# 会社登録ページ
class CompanyCreateFormView(LoginRequiredMixin, CreateView):
    template_name = 'es_management/create_company.html'
    model = Company
    form_class = CompanyCreateForm
    success_url = reverse_lazy('es_list')
    success_message = "会社が登録されました！"
    def get_success_url(self):
        return reverse('es_list',kwargs={'pk': self.object.id})
    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_id = self.request.user.id
        post.save()
        return super().form_valid(form)

# 会社削除機能
class CompanyDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "es_management/delete_company.html"
    model = Company
    success_url = reverse_lazy("company_list")
    success_message = "会社情報が削除されました！"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ESs'] = ES.objects.filter(company_id=self.kwargs['pk'])
        context["ES_number"] = len(context['ESs'])
        return context


# 会社のES表示
class ESListView(LoginRequiredMixin, CompanyPermission, TemplateView):
    template_name = 'es_management/es_list.html'
    model = ES
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.filter(id=self.kwargs['pk'])
        if len(companies) == 1:
            context["company"] = companies[0]
        context["ESs"] = ES.objects.filter(company_id=self.kwargs['pk'])
        return context
        

# ES登録ページ
class ESCreateFormView(LoginRequiredMixin, CompanyPermission, SuccessMessageMixin, CreateView):
    template_name = 'es_management/create_es.html'
    model = ES
    form_class = ESCreateForm
    success_message = "質問と回答が登録されました！"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_id"] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('es_list',kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_id = self.request.user.id
        post.company_id = self.kwargs['pk']
        post.save()
        
        return super().form_valid(form)


# ES削除機能
class ESDeleteView(LoginRequiredMixin, ESPermission, SuccessMessageMixin, DeleteView):
    template_name = "es_management/delete_es.html"
    model = ES
    success_message = "質問と回答が削除されました！"
    def get_success_url(self):
        return reverse('es_list',kwargs={'pk': self.object.company_id})


# ES編集機能
class ESUpdateView(LoginRequiredMixin, ESPermission, SuccessMessageMixin,UpdateView):
    template_name = "es_management/update_es.html"
    model = ES
    fields = ['question', 'answer']
    success_message = "質問と回答が編集されました！"
    def get_success_url(self):
        return reverse('es_list',kwargs={'pk': self.object.company_id})


# 要約に使用した文章リスト表示
class QuestionListView(LoginRequiredMixin, ListView):
    template_name = 'AI_summary/question_list.html'
    model = Question
    def get_queryset(self, **kwargs):
        query_set = Question.objects.filter(user_id=self.request.user.id)
        return query_set


# Question登録ページ
class QuestionCreateFormView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'AI_summary/create_question.html'
    model = Question
    form_class = QuestionCreateForm
    success_message = "質問と回答が登録されました"

    def get_success_url(self):
        return reverse('question_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_id = self.request.user.id
        post.save()
        return super().form_valid(form)

class QuestionDetail(LoginRequiredMixin, DetailView):
    #Companyテーブル連携
    model = Question
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "question_detail"
    #テンプレートファイル連携
    template_name = "AI_summary/question_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = Question.objects.filter(id=self.kwargs['pk'])
        print(question[0])
        context["answer_length"] = len(question[0].answer)
        return context

# 質問編集機能
class QuestionUpdateView(LoginRequiredMixin, SuccessMessageMixin,UpdateView):
    model = Question
    template_name = 'AI_summary/update_question.html'
    fields = ['question', 'answer']
    success_message = "質問と回答が編集されました！"
    def get_success_url(self):
        return reverse('question_list')

