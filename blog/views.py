from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from .models import Post , LikePost , comment , notification
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.
"""def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request , 'blog/home.html' , context)"""
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #By default django is looking for a template at <app>/<template>_<viewtype>.html. In order to change that according to your own choice then you can do that by this line.
    context_object_name = 'posts' #Django does not know the name of the variable which you use in your template for loop over Post. By default django is looking for object(name of variable) in template. To change that according to you then this line will be added. 
    ordering = ['-date_posted'] #Our Post sequence is from older to newer but we want to change that from newer to older. Inorder to do that this line is added.
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #By default django is looking for a template at <app>/<template>_<viewtype>.html. In order to change that according to your own choice then you can do that by this line.
    context_object_name = 'posts' #Django does not know the name of the variable which you use in your template for loop over Post. By default django is looking for object(name of variable) in template. To change that according to you then this line will be added. 
    #Our Post sequence is from older to newer but we want to change that from newer to older. Inorder to do that this line is added.
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User , username=self.kwargs.get('username')) #Get user from the requested url on the bases of username and store it in user
        return Post.objects.filter(author = user).order_by('-date_posted')
        
class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin , CreateView):
    model = Post
    fields = ['title' , 'content']

    def form_valid(self , form): #Overriding this function to save post for specific author. Without this we get an error that author is null.
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
class PostUpdateView(LoginRequiredMixin , UserPassesTestMixin , UpdateView):
    model = Post
    fields = ['title' , 'content']
    template_name = 'blog/update.html'

    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
"""class PostUpdateView(UpdateView): My Own logic
    model = Post
    fields = ['title' , 'content']
    template_name = 'blog/update.html'"""


class PostDeleteView(LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = Post
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
 
def about(request):
    return render(request , 'blog/about.html' , {'title' : 'About'})

@login_required
def like_post(request , pk):
    user = request.user
    post = Post.objects.get(pk = pk)

    like_filter = LikePost.objects.filter(post = post , user = user).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post = post , user = user)
        message = f'{user} like your post {post.title}'
        channel_layer = get_channel_layer()
        async_to_sync (channel_layer.group_send)(
            'notification',{
                'type' : 'sendNotification',
                'message' : message,
                'post_author' : post.author.username
            }
        )
        notification.objects.create(user = post.author , message = message)
    
    if like_filter != None:
        like_filter.delete()

    return redirect('blog-home') 

@login_required
def PostComment(request , pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk = pk)
            comment_obj = comment()
            comment_obj.comment = form.cleaned_data.get('comment')
            comment_obj.user = request.user
            comment_obj.post = post
            comment_obj.save()
            return redirect('post-comment' , pk=pk)
        else:
            return redirect('post-comment' , pk=pk)
    else:
            post = Post.objects.get(pk = pk)
            comments = comment.objects.filter(post = post)
            form = CommentForm()
            context = {
                'form' : form,
                'post' : post,
                'comments' : comments
            }
            return render(request , 'blog/comment.html' , context)
    
"""@login_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data.get('title')
            post.content = form.cleaned_data.get('content')
            post.author = request.user
            post.save()
            return redirect('blog-home')
        else:
            return redirect('blog-post')
    else:
        form = PostForm()
        return render(request , 'blog/post.html' , {'form' : form})"""

"""def permission_testing(request):
    content_type = ContentType.objects.get_for_model(Post)
    post_permission = Permission.objects.filter(content_type=content_type)
    print([perm.codename for perm in post_permission])
    user = User.objects.get(username="ukashahassan449")
    print(user.has_perms(["blog.view_post" , "blog.add_post" , "blog.update_post" , "blog.delete_post"]))
    for perm in post_permission:
        user.user_permissions.add(perm)
    print(user.has_perms(["blog.view_post" , "blog.add_post" , "blog.change_post" , "blog.delete_post"]))

    user = User.objects.get(email="ukashahassan449000@gmail.com")
    print(user.has_perms(["blog.view_post" , "blog.add_post" , "blog.change_post" , "blog.delete_post"]))
    return HttpResponse(f"{request.user}")"""
    
    
def notify(request):

    notifications = notification.objects.filter(user = request.user , is_read=False)
    
    return render(request , 'blog/notifications.html' , {'notifications' : notifications})