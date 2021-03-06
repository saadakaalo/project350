from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Comment, Course, UserDetail, LogTable, RoleTable
from .forms import QuestionForm, CommentForm, UserDetailForm

# @login_required
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('add_content/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'add_content/index.html', context)

# @login_required
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'add_content/detail.html', {'question': question})


@login_required
def get_question(request):
    user_detail = UserDetail.objects.get(user=request.user)
    user_group = user_detail.user_group
    user_access = RoleTable.objects.filter(
        user_group=user_group,
        access_name="ADD_QUESTION"
    )
    if not user_access:
        return HttpResponse("Sorry, You cannot add question")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuestionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            question_text = form.cleaned_data['question_text']
            question_name = form.cleaned_data['question_name']
            user = request.user
            course = Course.objects.get(
                course_code=form.cleaned_data['course_code'])
            q = Question(
                question_name=question_name,
                question_text=question_text,
                user=user,
                pub_date=timezone.now(),
                course=course,
            )
            q.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/questions/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = QuestionForm()

    return render(request, 'add_content/add_question.html', {'form': form})


@login_required
def get_user_details(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserDetailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            age = form.cleaned_data['age']
            profession = form.cleaned_data['profession']
            user = request.user
            location = form.cleaned_data['location']
            gender = form.cleaned_data['gender']
            user_detail = UserDetail(
                user=user,
                age=age,
                location=location,
                gender=gender,
                profession=profession,
            )
            user_detail.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/questions/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserDetailForm()

    return render(request, 'add_content/add_user_detail.html', {'form': form})


@login_required
def get_detail_view_with_comment(request, pk):
    question = get_object_or_404(Question, pk=pk)
    comment_list = Comment.objects.filter(question=question)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            comment_text = form.cleaned_data['comment_text']
            user = request.user
            comment = Comment(
                comment_text=comment_text,
                question=question,
                user=user,
                created_date=timezone.now()
            )
            comment.save()

            # q = Question(question_text=question_text,
            #              user=user, pub_date=timezone.now())
            # q.save()
            # comment = form.save(commit=False)
            # comment.post = post
            # comment.save()

            # return redirect('questions:detail', pk=pk)
    #         return HttpResponseRedirect('/questions/')
    else:
        log_table = LogTable(user=request.user,
                             operation="View post " + str(pk),
                             operation_time=timezone.now(),)
        log_table.save()

    new_form = CommentForm()
    return render(request,
                  'add_content/detail.html',
                  {'form': new_form,
                   'question': question,
                   'comment_list': comment_list
                   }
                  )


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'add_content/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        user_detail = UserDetail.objects.get(user=self.request.user)
        user_group = user_detail.user_group
        user_access = RoleTable.objects.filter(
            user_group=user_group,
            access_name="SEE_PENDING_QUESTION"
        )
        if not user_access:
            return Question.objects.filter(status="ACCEPTED").order_by('-pub_date')
        return Question.objects.order_by('-pub_date')


class ProfileView(LoginRequiredMixin, generic.ListView):
    template_name = 'add_content/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(user=self.request.user)


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'add_content/detail.html'
