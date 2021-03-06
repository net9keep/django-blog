from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

import smtplib
from email.mime.text import MIMEText


from .models import Post
from .forms import PostForm
# Create your views here.





def send_mail():
    senderAddr = "tae0code@gmail.com"

    recipientAddr = "tae0code@gmail.com"

    text = "smpt test"

    msg = MIMEText(text, _charset="utf8")

    msg['Subject'] = "smtp test"

    msg['From'] = senderAddr

    msg['to'] = recipientAddr

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    s.login(str(senderAddr), "1325213a")

    s.sendmail(senderAddr, recipientAddr, msg.as_string())

    s.quit()


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            send_mail()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html',{'form' : form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' : post})

def post_list(request):
    send_mail()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts' : posts})

