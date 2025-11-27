from django.shortcuts import render, redirect
from django.http import HttpResponse
from random import randint


def test_view(request):
    return HttpResponse(f"This is a test view.{randint(1,1000)}")



def html_view(request):
    return render(request,"base.html")

