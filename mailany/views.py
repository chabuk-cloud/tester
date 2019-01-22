from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
import sendgrid
import os,random
from sendgrid.helpers.mail import *

def index(request):
    context={}
    if(request.method == 'GET'):
        r_otp = request.GET.get('otp')
        sender = Email(request.GET.get('sender'))
        
        r_mail = request.GET.get('reciever')
        reciever = Email(request.GET.get('reciever'))
        subject = request.GET.get('subject')
        content = Content("text/plain", request.GET.get('content'))
        x=True
        
        mail=request.session['mail']
        print(mail,r_mail)
        if(r_mail == None):
            print("none")
            x=True
        else:
            if(r_mail.split("@")[-1] != mail.split("@")[-1]):
                context['status_code'] = 1
                context['mail_end']=mail.split("@")[-1]
                print("wrong mail")
                x=False
        otp=request.session['otp']
        print(otp,r_otp)
        if(str(r_otp) != str(otp)):
            context['status_code'] = 2
            print("wrong otp")
            x=False
            
        if(x):
            try:
                print(sender,r_mail,subject,content)
                sg = sendgrid.SendGridAPIClient(apikey='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')
                print(1)
                mail = Mail(sender, subject, reciever, content)
                print(2,mail.get())
                response = sg.client.mail.send.post(request_body=mail.get())
                print(3)
                print("Status Code = ",response.status_code)
                context['status_code']=int(response.status_code)
            except Exception as e:
                context['status_code']=400
                print(e)
                pass

        #print(sender,reciever,subject,content)
        if(r_mail==None):
            context['status_code']=0
    return render(request,'mailany/index.html',context)

def verify(request):
    context={}
    
    if(request.method == 'GET'):
        otp = random.randint(100000,999999)
        mail =request.GET.get('email')
        request.session['otp']=otp
        request.session['mail']=mail
        reciever = Email(request.GET.get('email'))
        sender = Email("verify@anymail.com")
        subject = 'OTP for verification'
        content = Content("text/plain", "Your OTP is " + str(otp))
        try:
            #print(sender,reciever,subject,content)
            sg = sendgrid.SendGridAPIClient(apikey='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')
            print(1)
            mail = Mail(sender, subject, reciever, content)
            print(2)
            print(mail.get())
            response = sg.client.mail.send.post(request_body=mail.get())
            print(3)
            print("Status Code = ",response.status_code)
            context['status_code']=int(response.status_code)
            return redirect('/mailany/index1')
        except Exception as e:
            context['status_code']=400
            print(e)
            pass        
        
    
    #context['graph'] = div
    return render(request,'mailany/home.html',context)

