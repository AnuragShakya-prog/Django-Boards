from django.shortcuts import (render,get_object_or_404,get_list_or_404,redirect)
from django.http import HttpResponse
from board.models import Board,Topic,Post
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .forms import TopicForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db.models import Count
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.urls import reverse_lazy
# Create your views here.


def homepage(request):
    boards=Board.objects.all()

    return render(request,"home.html",{"boards":boards})


def board_topics(request,pk):
    board=get_object_or_404(Board,pk=pk)

    page=request.GET.get('page',1)
    queryset=Topic.objects.filter(board=board).order_by('-last_updated').annotate(replies=Count('posts')-1)
    paginator=Paginator(queryset,4)
    try:
        topics=paginator.page(page)
    except PageNotAnInteger as e:
        topics=paginator.page(paginator.num_pages)
    
    except EmptyPage as ep:
        topics=paginator.page(1)

    start_index=topics.number-4
    start_index=start_index if start_index>0 else 0

    page_range=list(topics.paginator.page_range)[(start_index):(topics.number+4)]


    if not list(topics):
        return render(request,'topics.html',{"not_found":True})
    return render(request,'topics.html',{"board":board,"topics":topics,'page_range':page_range})


@login_required
def new_topic(request,pk):
    board=get_object_or_404(Board,pk=pk)
    if request.method=='POST':
        topic_form=TopicForm(request.POST)

        if topic_form.is_valid():
            topic=topic_form.save(commit=False)
            topic.board=board
            topic.starter=request.user
            
            topic.save()
            
            post=Post.objects.create(
                message=topic_form.cleaned_data['message'],
                created_by=request.user,
                topic=topic
            )

            return redirect('topic_posts',pk=pk,topic_pk=topic.pk)
    else:
        topic_form=TopicForm()

    return render(request,'new_topic.html',{"board":board,'form':topic_form})


@login_required
def topic_posts(request,pk,topics_pk):
    topic=get_object_or_404(Topic,board__pk=pk,pk=topics_pk)
    cur_user=request.user
    if not (cur_user in topic.views.all()):
        topic.views.add(cur_user) 

    return render(request,'topics_post.html',{"topic":topic})

@login_required
def reply_topic(request,pk,topics_pk):
    topic=get_object_or_404(Topic,board__pk=pk,pk=topics_pk)
    
    if request.method=='POST':
        form=PostForm(request.POST)

        if form.is_valid():
            post=Post.objects.create(
                message=form.cleaned_data['message'],
                created_by=request.user,
                topic=topic
            )

            topic.last_updated=timezone.now()
            topic.save()
            return redirect('topic_posts',pk=pk,topics_pk=topics_pk)

    else:
        form=PostForm()


    return render(request,'reply_topic.html',{"topic":topic,'form':form})


@method_decorator(login_required,name='dispatch')
class UpdatePost(UpdateView):
    model=Post
    pk_url_kwarg='post_pk'
    context_object_name='post'
    fields=['message',]
    template_name='edit_post.html'

    def get_queryset(self):
        queryset=super().get_queryset()

        return queryset.filter(created_by=self.request.user)

    def is_valid(self,form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post.updated_at=timezone.now()

        return super().is_valid()


class BoardListView(ListView):
    model=Board
    context_object_name='boards'
    template_name='home.html'
    paginate_by=3


class UserUpdateView(UpdateView):
    model=User
    fields=('first_name','last_name','username','email')
    template_name='my_account.html'
    success_url=reverse_lazy('user_update')

    def get_object(self,**kwargs):
        return self.request.user
