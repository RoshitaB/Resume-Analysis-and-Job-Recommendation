from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
import numpy as np
# from keras.models import load_model
from predict.Jobs import jobs
from predict.classify import resume_test

# from keras.preprocessing import image

# Create your views here.


top15=None

def Filter(request):
    profession=request.GET['input']
    filtered_from15=top15[top15["Profession"]==profession]
    unique = list(top15['Profession'].unique())
    return render(request,'crop_index.html',{"top15":filtered_from15,"unique":unique})


def display(request):
    unique = list(top15['Profession'].unique())
    return render(request,'crop_index.html',{"top15":top15,"unique":unique}) 



def index(request):
    context={'a':1}
    return render(request,'crop_index.html',context)

img_height, img_width=224,224

def predictImage(request):
    print (request)
    print (request.POST.dict())
    
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    testimage='.'+filePathName
    professions,data = resume_test(testimage)
    global top15
    top15 = jobs(professions,data)
    unique = list(top15['Profession'].unique())
    context={'filePathName':filePathName,"top15":top15,"unique":unique}
    
    print(top15)
    print(unique)
    return redirect("display")
    # return render(request,'crop_index.html',context) 



