import subprocess

output = subprocess.check_output(('arp', '-a'))
print(output.decode('ascii'))

