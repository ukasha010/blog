from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)#auto_now(update date every time post updated) , auto_now_add(we cannot update date) , timezone(we can change date if we want to)
    author = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail' , kwargs = {'pk': self.pk})
    
class LikePost(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Liked {self.post.title}"

class comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    
    def __str__(self):
        return f"comment by {self.user.username}" 
    
    
class notification(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user} notification'
