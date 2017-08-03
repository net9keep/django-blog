from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email import Utils
from email.header import Header
import os


from .models import Post
from .forms import PostForm
# Create your views here.

cc_user = ["tae0code@gmail.com","net9keep@naver.com"]
smtp_server  = "smtp.naver.com"
port = 465
userid = "net9keep"
passwd = "qs13e2rd13w2a"


def send_mail(from_user, to_user, subject, text, attach):
    COMMASPACE = ", "
    msg = MIMEMultipart("alternative")
    msg["From"] = from_user
    msg["To"] = to_user
    msg["Subject"] = Header(s=subject, charset="utf-8")
    msg["Date"] = Utils.formatdate(localtime=1)
    msg.attach(MIMEText(text, "html", _charset="utf-8"))

    if (attach != None):
        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(attach, "rb").read())
        Encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=\"%s\"" % os.path.basename(attach))
        msg.attach(part)

    smtp = smtplib.SMTP(smtp_server, port)
    smtp.login(userid, passwd)
    smtp.sendmail(from_user, msg.as_string())
    smtp.close()


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
            send_mail("net9keep@naver.com", "tae0code@gmail.com", "test", "test")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html',{'form' : form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' : post})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts' : posts})

