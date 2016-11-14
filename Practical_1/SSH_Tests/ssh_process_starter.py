from paramiko.client import SSHClient
import os

# user inputs #

with open('default_inputs.txt') as f:
    default_inputs = [x.strip('\n') for x in f.readlines()]

pi_ip = raw_input('Please enter your pi ip adress: (Return for previous selection)') or default_inputs[0]
pi_usr = raw_input('Please enter your pi username: ') or default_inputs[1]
pi_pass = raw_input('Please enter your pi password: ') or default_inputs[2]
local_git_repo = raw_input('Please enter your local git repo directory: ') or default_inputs[3]
pi_git_repo = raw_input('Please enter your pi git repo directory: ') or default_inputs[4]
cwd = os.getcwd()

# write new selections to file #

f = open('default_inputs.txt','w')
f.write(pi_ip + '\n')
f.write(pi_usr + '\n')
f.write(pi_pass + '\n')
f.write(local_git_repo + '\n')
f.write(pi_git_repo + '\n')
f.close()

client = SSHClient()
client.load_system_host_keys()

client.connect(pi_ip, pi_usr, pi_pass)
stdin, stdout, stderr = client.exec_command('python ' + pi_git_repo + cwd.replace(local_git_repo,"") + 'motor_position_example.py')