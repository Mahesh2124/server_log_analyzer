# import paramiko
# import os
# import gzip
# host = '192.168.17.126'
# port = 22
# username = ''
# password = ''

# source_directory = '/var/log/nginx/access.log-20231018'
# local_file_path = '/Users/kuchetti.mahesh/Desktop/myproject/access1.log'
# if os.path.exists(local_file_path):
#     os.remove(local_file_path)
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# try:
#     ssh.connect(host, port, username, password)
#     sftp = ssh.open_sftp()

#     stdin, stdout, stderr = ssh.exec_command(f"sudo -S ls {source_directory}| grep access.log*")
#     stdin.write(f"{password}\n")
#     stdin.flush()
    
#     output = stdout.read().decode('utf-8')
#     file_paths = output.split()
#     print(file_paths)
#     with open(local_file_path, 'ab') as local_file:  # Open in append binary mode
#         for file_path in file_paths:
#             if file_path.endswith('.gz'):
#                 print(1)
#                 stdin, stdout, stderr = ssh.exec_command(f"sudo -S zcat {file_path}")
#                 stdin.write(f"{password}\n")
#                 stdin.flush()
#                 # print(stdout.read.decode())                
#                 # with gzip.open(file_path, 'rb') as gz_file:
#                 #     data = gz_file.read()
#                 # with open(local_file_path, 'ab') as output_file:
#                 #     local_file_path.write(data)
#             else:
#                 stdin, stdout, stderr = ssh.exec_command(f"sudo -S cat {file_path}")
#                 stdin.write(f"{password}\n")
#                 stdin.flush()
#                 binary_content = stdout.read()
#                 local_file.write(binary_content)

#     sftp.close()
#     ssh.close()

# except Exception as e:
#     print(f"An error occurred: {str(e)}")



# import paramiko
# import gzip
# import os 
# host = '192.168.17.176'
# port = 22
# username = ''
# password = ''

# source_directory = '/var/log/nginx/access.log-20231018'
# local_file_path = '/Users/kuchetti.mahesh/Desktop/myproject/access1.log'
# if os.path.exists(local_file_path):
#     os.remove(local_file_path)
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# try:
#     ssh.connect(host, port, username, password)
#     sftp = ssh.open_sftp()

#     stdin, stdout, stderr = ssh.exec_command(f"sudo -S ls {source_directory}")
#     stdin.write(f"{password}\n")
#     stdin.flush()
#     print(stderr.read())

#     output = stdout.read().decode('utf-8')
#     file_paths = output.split()
#     print(file_paths)
#     with open(local_file_path, 'ab') as local_file:
#         print(1)
#         for file_path in file_paths:
#             stdin, stdout, stderr = ssh.exec_command(f"sudo -S cat {file_path}")
#             stdin.write(f"{password}\n")
#             stdin.flush()
#             print(2)
#             if file_path.endswith(".gz"):
#                 # Read and decompress .gz files
#                 compressed_data = stdout.read()
#                 with gzip.GzipFile(fileobj=gzip.io.BytesIO(compressed_data)) as decompressed:
#                     binary_content = decompressed.read()
                
#             else:
#                 # Read normal files
#                 binary_content = stdout.read()
#             local_file.write(binary_content)

#     sftp.close()
#     ssh.close()

# except Exception as e:
#     print(f"An error occurred: {str(e)}")


import paramiko
import gzip
import os

host = '192.168.17.126'
port = 22
username = ''
password = ''
server=input("enter your server: ")
source_directory = '/var/log/httpd/'
local_file_path = '/Users/kuchetti.mahesh/Desktop/myproject/access1.log'
if os.path.exists(local_file_path):
    os.remove(local_file_path)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, port, username, password)
    sftp = ssh.open_sftp()
    # command = f"find /path/to/folder -type f -name 'access.log-*' ! -name '*.gz' -exec grep 'access.log*' {{}} \\;"
    # stdin, stdout, stderr = ssh.exec_command(f"sudo -S {command}")
    if (server=='nginx'):
        source_directory = '/var/log/nginx/'
        stdin, stdout, stderr = ssh.exec_command(f"sudo -S ls {source_directory} | grep access.log-*")
    elif (server == 'httpd'):
        source_directory = '/var/log/httpd/'
        stdin, stdout, stderr = ssh.exec_command(f"sudo -S ls {source_directory} | grep access_log-*")

    stdin.write(f"{password}\n")
    stdin.flush()
    print(stderr.read().decode())

    output = stdout.read().decode('utf-8')
    print(output)
    file_paths = output.split()
    # file_paths = ['/var/log/nginx/access.log-20231019','/var/log/nginx/access.log-20231106','/var/log/nginx/access.log']
    # for file_path in file_paths:
    #     if file_path.endswith(".gz"):
    #         file_paths.remove(file_path)
    print(file_paths)
    with open(local_file_path, 'ab') as local_file: 
        print(1)
        for file_path in file_paths:
            print(2)
            # command = f"find /path/to/folder -type f -name 'access.log-*' ! -name '*.gz' -exec grep 'access.log*' {{}} \\;"
            # stdin, stdout, stderr = ssh.exec_command(f"sudo -S {command}")
            # if file_path.endswith(".gz"):
            #     print(3)
            #     with gzip.GzipFile(fileobj=gzip.io.BytesIO(binary_content)) as f:
            #         binary_content = f.read()
            #         print(4)

            # local_file.write(binary_content)    
                       
            stdin, stdout, stderr = ssh.exec_command(f"sudo -S cat {source_directory}/{file_path}")
            stdin.write(f"{password}\n")
            stdin.flush()
            binary_content = stdout.read()

            # Check if the file is compressed (.gz) and decompress if necessary
            if file_path.endswith(".gz"):
                print(3)
                with gzip.open(gzip.io.BytesIO(binary_content), 'rb') as f:
                    binary_content = f.read()

            local_file.write(binary_content)

    sftp.close()
    ssh.close()

except Exception as e:
    print(f"An error occurred: {str(e)}")
