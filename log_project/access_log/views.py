import re
import os
import paramiko
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Successful_url,Client_errors,Server_errors,Redirection
from django.db import transaction
from .forms import ServerLoginForm,Server,DateForm
import subprocess
import gzip,tarfile,zipfile,shutil
from django.views import View
from datetime import datetime
from io import BytesIO

def data_to_database(status_code,ip,url,timestamp,hit):
    if int(status_code) <300:
        existed_ip = Successful_url.objects.filter(IP_ADDRESS=ip,URL=url).exists()
        if not existed_ip:
            Successful_url.objects.create(IP_ADDRESS=ip,URL=url)
    elif int(status_code)>=300 and int(status_code)<400:
        ip_exists = Redirection.objects.filter(ip_address=ip,url=url).exists()
        if ip_exists:
            instance = Redirection.objects.filter(ip_address=ip,url=url).first()
            instance.count=instance.count+1
            instance.save()
        else:
            Redirection.objects.create(ip_address=ip, url=url,status_code=status_code,count=hit,timestamp=timestamp)                   
    elif int(status_code)>=400 and int(status_code)<500:
        ip_exists = Client_errors.objects.filter(ip_address=ip,url=url).exists()
        if ip_exists:
            instance = Client_errors.objects.filter(ip_address=ip,url=url).first()
            instance.count=instance.count+1
            instance.save()
        else:
            Client_errors.objects.create(ip_address=ip, url=url,status_code=status_code,count=hit,timestamp=timestamp)
    elif int(status_code)>=500 and int(status_code)<600 :
        ip_exists = Server_errors.objects.filter(ip_address=ip,url=url).exists()
        if ip_exists:
            instance = Server_errors.objects.filter(ip_address=ip,url=url).first()
            instance.count=instance.count+1
            instance.save()
        else:
            Server_errors.objects.create(ip_address=ip, url=url,status_code=status_code,count=hit,timestamp=timestamp)

def analyze_log(request):
    log_file = '/Users/kuchetti.mahesh/Desktop/jenkins/myproject/log_project/access.log'
    log_pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>[^"]+)" (?P<status>\d+)'
    with open(log_file, 'r') as log_file:
        for line in log_file:
            match = re.search(log_pattern, line)
            if match:
                ip = match.group('ip')
                url = match.group('url')
                timestamp=match.group('timestamp')
                time=timestamp.split(' ')
                timestamp = time[0]
                status_code = match.group('status')
                hit=1
                data_to_database(status_code,ip,url,timestamp,hit)
    client400 = Client_errors.objects.all()
    server500 = Server_errors.objects.all()
    success_log= Successful_url.objects.all()
    redirection300=Redirection.objects.all()
    date_form=DateForm()
    return render(request, 'display_data.html', {'client400': client400, 'success_log':success_log,'server500':server500,'redirection300':redirection300,'date_form':date_form})  

def server_login_view(request):     
    if request.method == 'POST':
        form = ServerLoginForm(request.POST)
        if form.is_valid():
            return redirect('server_details')
    else:
        form = ServerLoginForm()
    return render(request, 'server_login.html', {'form': form})

def form_render(request):
    file_paths=[]
    local_file_path = '/Users/kuchetti.mahesh/Desktop/jenkins/myproject/log_project/access.log'
    with open(local_file_path,'w') as f:
        pass
    vm_details = request.session.get('vm_details', {})
    ip = vm_details.get('ip', '')
    username = vm_details.get('username', '')
    password = vm_details.get('password', '')
    port = vm_details.get('port', '')
    if request.method == 'POST':
        form = Server(request.POST)
        if form.is_valid():
            my_checkbox_value = form.cleaned_data['my_checkbox']
            server=form.cleaned_data.get('server_name')
            server=server.lower()
            print(server,my_checkbox_value)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            paths={'nginx':'/var/log/nginx','httpd':'/var/log/httpd','lshttpd':'/usr/local/lsws/logs','apache':'/var/log/apache2'}
            paths_keys=list(paths.keys())
            if server in paths_keys:
                try:
                    print(ip,port,username,password,server)
                    ssh.connect(ip, port, username, password)
                    sftp = ssh.open_sftp()
                    file = paths[server]
                    stdin, stdout, stderr = ssh.exec_command(f"sudo -S ls {file} | grep access.*")
                    stdin.write(f"{password}\n")
                    stdin.flush()
                    output = stdout.read().decode()
                    print(stderr.read().decode())
                    file_paths = output.split()
                    print(file_paths)
                    with open(local_file_path, 'ab') as local_file:
                        for file_path in file_paths:
                            stdin, stdout, stderr = ssh.exec_command(f"sudo -S cat {file}/{file_path}")
                            stdin.write(f"{password}\n")
                            stdin.flush()
                            binary_content = stdout.read() 
                            if file_path.endswith(".gz"):
                                with gzip.open(gzip.io.BytesIO(binary_content), 'rb') as f:
                                    binary_content = f.read()
                            elif file_path.endswith('.zip'):
                                with zipfile.ZipFile(io.BytesIO(binary_content),'r') as zip_data:
                                    files=zipfile.namelist()
                                    if files:
                                        binary_content = zip_data.read(files[0])
                            elif file_path.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz")):
                                with tarfile.open(fileobj=BytesIO(binary_content), mode='r:*') as tar_data:
                                    files = tar_data.getnames()
                                    if files:
                                        binary_content = tar_data.extractfile(files[0]).read()
                            local_file.write(binary_content)
                    sftp.close()
                    ssh.close()
                    request.session['log_path'] = paths[server]
                except paramiko.ssh_exception.SSHException as e:
                    print(f"SSH error: {str(e)}")
                    return HttpResponse("SSH connection timeout. Please check the server availability and credentials.")
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    return HttpResponse("WRONG CREDENTIALS")
            else:
                return HttpResponse("WRONG CREDENTIALS")   
    return redirect('analyze_log')

def server_details(request):
    data=[]
    if request.method == 'POST':
        form = ServerLoginForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data.get('ip_address')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            port=form.cleaned_data.get('port')
            server=form.cleaned_data.get('server')
            vm_details={'ip':ip,'username':username,'password':password,'port':port}
            request.session['vm_details'] = vm_details
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip, port, username, password)
                sftp = ssh.open_sftp()
                stdin, stdout, stderr = ssh.exec_command(f"sudo -S systemctl list-units --all  | grep -oE 'nginx.service|httpd.service|lshttpd.service|apache2.service|caddy.service|jetty.service|jigsaw.service'")
                stdin.write(f"{password}\n")
                stdin.flush()
                data = stdout.read().decode('utf-8')
                data=data.split('\n')
                print(data)
                sftp.close()
                ssh.close()
            except paramiko.ssh_exception.SSHException as e:
                print(f"SSH error: {str(e)}")
                return HttpResponse("SSH connection timeout. Please check the server availability and credentials.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return HttpResponse("WRONG CREDENTIALS")
        else:
            return HttpResponse("Check your Credentials")
    form = Server()
    date_form=DateForm()
    return render(request,'server_details.html',{'data':data,'form':form,'date_form':date_form})

class EraseDataView(View):
    def get(self, request, *args, **kwargs):
     
        Redirection.objects.all().delete()
        Server_errors.objects.all().delete()
        Client_errors.objects.all().delete()
        Successful_url.objects.all().delete()
        return render(request,'display_data.html')

def date_logs(request):
    if request.method == 'POST':
        form=DateForm(request.POST)
        if form.is_valid():
            from_date_str= str(form.cleaned_data.get('from_date'))
            to_date_str= str(form.cleaned_data.get('to_date'))
            from_date=datetime.strptime(from_date_str,'%Y-%m-%d')
            to_date=datetime.strptime(to_date_str,'%Y-%m-%d')
            from_date=from_date.strftime('%d/%b/%Y')
            to_date=to_date.strftime('%d/%b/%Y')
            from_date=datetime.strptime(from_date,'%d/%b/%Y')
            to_date=datetime.strptime(to_date,'%d/%b/%Y')
            date_format = "%d/%b/%Y"
            local_file_path='/Users/kuchetti.mahesh/Desktop/jenkins/myproject/log_project/access.log'
            log_path='/Users/kuchetti.mahesh/Desktop/jenkins/myproject/access1.log'
            log_pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>[^"]+)" (?P<status>\d+)'
            if from_date > to_date:
                return HttpResponse("Please check your DATES")
            with open(local_file_path, 'r') as log_file:
                with open(log_path,'w') as log:
                    for line in log_file:
                        match = re.search(log_pattern, line)
                        if match:
                            timestamp=match.group('timestamp')
                            time_list=timestamp.split(':')
                            log_time=time_list[0]
                            date3  = datetime.strptime(log_time, date_format)
                            if (date3 >= from_date and date3 <= to_date):
                                log.write(line)
            
        else:
            return HttpResponse("Plase enter the correct DATE format")
        with open(log_path,'r') as f:
                access_content=f.readlines()
    return render(request,'time_logs.html',{'access_content':access_content})


