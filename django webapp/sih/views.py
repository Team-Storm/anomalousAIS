from django.shortcuts import render,redirect
from django.http import HttpResponse
from sih.forms import DataForm
from sih.models import Data
from bayesian import BA_main
import os
from django.conf import settings

# Create your views here.
def hello(request):
   text = """<h1>welcome to my app !</h1>"""
   return HttpResponse(text)

def SaveData(request):
   saved = 0
   #print(request.method)
   if request.method == "POST":
      #Get the posted form
      MyDataForm = DataForm(request.POST, request.FILES)
      print("andar")
      if MyDataForm.is_valid():
         #print("valid")
         data = Data()
         data.name = MyDataForm.cleaned_data["name"]
         data.file = MyDataForm.cleaned_data["file"]
         data.save()
         saved = 1
   else:
      MyDataForm = Dataform()
	
   return redirect('/train/'+str(saved),locals())
   #return render(request, 'saved.html', locals())
   
def train(request,saved):
	last_data=Data.objects.all()
	last_data[len(last_data)-1].file.open(mode="rb")
	filepath=last_data[len(last_data)-1].file.path
	BA_main.bayesianmain(filepath=filepath,K=5)
	saved=True
	vesseldata={}
	#print os.getcwd()
	#print settings.BASE_DIR
	with open("AIS_Sailfish_top1500_scores.txt",'r') as f:
		for line in f:
			vesseldata[line.split(" ")[0]]=line.split(" ")[1]
	return render(request,'show.html',locals())
	