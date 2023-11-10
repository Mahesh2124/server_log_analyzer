import re
import os
import paramiko
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UnwantedHit,Successful_url
from django.db import transaction
from .forms import ServerLoginForm
import subprocess
import gzip



def analyze_log(request):
    log_file = '/Users/kuchetti.mahesh/Desktop/myproject/access.log'
    log_pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>[^"]+)" (?P<status>\d+)'
    with open(log_file, 'r') as log_file:
        for line in log_file:
            match = re.search(log_pattern, line)
            if match:
                ip = match.group('ip')
                url = match.group('url')
                status_code = match.group('status')
                hit=1
                if int(status_code) < 400:
                    existed_ip = Successful_url.objects.filter(IP_ADDRESS=ip,URL=url).exists()
                    if not existed_ip:
                        Successful_url.objects.create(IP_ADDRESS=ip,URL=url)

                else:
                    ip_exists = UnwantedHit.objects.filter(ip_address=ip,url=url).exists()
                    if ip_exists:
                        instance = UnwantedHit.objects.filter(ip_address=ip,url=url).first()
                        instance.count=instance.count+1
                        instance.save()
                    else:
                        UnwantedHit.objects.create(ip_address=ip, url=url,status_code=status_code,count=hit)  
    entries = UnwantedHit.objects.all()
    success_log= Successful_url.objects.all()

    return render(request, 'display_data.html', {'entries': entries, 'success_log':success_log})     #return render(request,'analysis_done.html')



def server_login_view(request):     
    if request.method == 'POST':
        form = ServerLoginForm(request.POST)
        if form.is_valid():
            return redirect('form_render')
    else:
        form = ServerLoginForm()
    return render(request, 'server_login.html', {'form': form})


def form_render(request):
    # print("hello")
    file_paths=[]
    local_file_path = '/Users/kuchetti.mahesh/Desktop/myproject/access.log'
    if os.path.exists(local_file_path):
        os.remove(local_file_path)
    if request.method == 'POST':
        print("the data",request.POST)
        form = ServerLoginForm(request.POST)
        # print(1)
        if form.is_valid():
            # print(2)
            ip = form.cleaned_data.get('ip_address')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            port=form.cleaned_data.get('port')
            server=form.cleaned_data.get('server')

            print(ip,username,password,port,server)

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                print(1)
                ssh.connect(ip, port, username, password)
                print(2)
                sftp = ssh.open_sftp()
                if (server == 'nginx'):
                    file = '/var/log/nginx/'
                    stdin, stdout, stderr = ssh.exec_command(f"sudo -S ls {file} | grep access.log-*")
                    stdin.write(f"{password}\n")
                    stdin.flush()
                    output = stdout.read().decode('utf-8')
                    print(stderr.read().decode())
                    file_paths = output.split()
                    print(file_paths)
                elif(server=='httpd') :
                    print(3)
                    file='/var/log/httpd/'
                    stdin, stdout, stderr = ssh.exec_command(f"sudo -S ls {file} | grep access_log-*")
                    stdin.write(f"{password}\n")
                    stdin.flush()
                    output = stdout.read().decode('utf-8')
                    print(stderr.read().decode())
                    file_paths = output.split()
                    print(file_paths)
                    if len(file_paths)==0:
                        return HttpResponse("Please choose apache because server is running on UBUNTU")
                else:
                    file='/var/log/apache2/'
                    print(4)
                    stdin, stdout, stderr = ssh.exec_command(f"sudo -S ls {file} | grep access.log-*")
                    stdin.write(f"{password}\n")
                    stdin.flush()
                    output = stdout.read().decode('utf-8')
                    print(stderr.read().decode())
                    file_paths = output.split()
                    print(file_paths)
                    if len(file_paths)==0:
                        return HttpResponse("Please choose HTTPD because server is running on CENTOS")
                
                with open(local_file_path, 'ab') as local_file: 
                    for file_path in file_paths:
                        stdin, stdout, stderr = ssh.exec_command(f"sudo -S cat {file}/{file_path}")
                        stdin.write(f"{password}\n")
                        stdin.flush()
                        binary_content = stdout.read()                
                        if file_path.endswith(".gz"):
                            with gzip.open(gzip.io.BytesIO(binary_content), 'rb') as f:
                                binary_content = f.read()
                        local_file.write(binary_content)
                sftp.close()
                ssh.close()
            except paramiko.ssh_exception.SSHException as e:
                print(f"SSH error: {str(e)}")
                return HttpResponse("SSH connection timeout. Please check the server availability and credentials.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return HttpResponse("WRONG CREDENTIALS")
        else:
            return HttpResponse("WRONG CREDENTIALS")
    return redirect('analyze_log')  
    
    

