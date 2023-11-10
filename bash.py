# import subprocess

# # Define the Bash command as a string
# bash_command = 'awk -F\'"\' \'{print $2}\'</Users/kuchetti.mahesh/Desktop/myproject/log_project/access.log'

# # Use subprocess to run the Bash command
# result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# # Check the result and print the output
# if result.returncode == 0:
#     print("Command executed successfully. Output:")
#     print(result.stdout)
# else:
#     print("Command failed. Error output:")
#     print(result.stderr)



# import subprocess

# # Define the Bash command as a list of strings to avoid issues with double quotes
# bash_command = ['awk', '-F"', '{print $2}']

# # Create a subprocess and communicate with it
# result = subprocess.Popen(bash_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
# input_data = '127.0.0.1 - - [18/Oct/2023:05:58:51 -0400] "GET / HTTP/1.1" 200 17 "-" "curl/7.29.0"'
# output, _ = result.communicate(input_data)

# # Check the result and print the output
# if result.returncode == 0:
#     print("Command executed successfully. Output:")
#     print(output)
# else:
#     print("Command failed.")

# -------------------
# import subprocess

# # Specify the input and output file paths
# input_file = '/Users/kuchetti.mahesh/Desktop/myproject/log_project/access.log'  # Replace with your input file path
# output_file = 'output.txt'  # Replace with your output file path

# # Define the Bash command as a list of strings
# bash_command = ['awk', '-F"', '{print $2}']

# # Create a subprocess and communicate with it, providing input from the input file
# with open(input_file, 'r') as f:
#     input_data = f.read()
# result = subprocess.Popen(bash_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
# output, _ = result.communicate(input_data)
# # if result.returncode == 0:
# #     print("Command executed successfully. Output:")
# #     print(output)
# # Check the result and write the output to the output file
# if result.returncode == 0:
#     print("Command executed successfully. Writing output to", output_file)
#     with open(output_file, 'w') as f:
#         f.write(output)
# else:
#     print("Command failed.")

    # --------------------------
# import subprocess

# # Define the Bash command as a list of strings
# bash_command = ['awk', '-F"', '{print $1, $2}']

# # Specify the path to the input and output files
# input_file = '/Users/kuchetti.mahesh/Desktop/myproject/log_project/access.log'  # Replace with the path to your input file
# output_file = 'your_output_file.txt'  # Replace with the path to your output file

# try:
#     # Open and read the input file
#     with open(input_file, 'r') as file:
#         input_data = file.read()
# except FileNotFoundError:
#     print(f"Input file '{input_file}' not found.")
#     exit(1)

# # Create a subprocess and communicate with it
# result = subprocess.Popen(bash_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
# output, _ = result.communicate(input_data)

# # Check the result and write the output to the output file
# if result.returncode == 0:
#     print("Command executed successfully. Output:")
#     print(output)
#     ip_address, text_in_quotes = output.strip().split(" ", 1)
#     print("IP Address:", ip_address)
#     print("Text in Double Quotes:", text_in_quotes)
    
#     # Write the output to the output file
#     with open(output_file, 'w') as output_file:
#         output_file.write(output)
#     print(f"Output written to '{output_file}'")
# else:
#     print("Command failed.")




# ------------------
# import subprocess

# # Specify the input and output file paths
# input_file = '/Users/kuchetti.mahesh/Desktop/myproject/log_project/access.log'  # Replace with your input file path
# output_file = 'output.txt'  # Replace with your output file path

# # Define the Bash command as a list of strings
# bash_command = ['awk', '-F"', '{print $2}']

# # Create a subprocess and communicate with it, providing input from the input file
# with open(input_file, 'r') as f:
#     input_data = f.read()
# result = subprocess.Popen(bash_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
# output, _ = result.communicate(input_data)

# # Check the result and write the output to the output file
# if result.returncode == 0:
#     print("Command executed successfully. Writing output to", output_file)
#     with open(output_file, 'w') as f:
#         f.write(output)
# else:
#     print("Command failed.")

# --------------
# import subprocess

# # Define the path to your Bash script
# bash_script = '/Users/kuchetti.mahesh/Desktop/myproject/hello.sh'  # Replace with the actual path to your Bash script

# # Use subprocess to run the Bash script
# result = subprocess.run(['bash', bash_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# # Check the result and print the output
# if result.returncode == 0:
#     print("Bash script executed successfully. Output:")
#     # print(result.stdout)
# else:
#     print("Bash script execution failed. Error output:")
    # print(result.stderr)

import subprocess

# Define the path to your Bash script
script_path = '/Users/kuchetti.mahesh/Desktop/myproject/hello.sh'

try:
    # Run the Bash script
    subprocess.run(['bash', script_path], check=True)
    print("Bash script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
