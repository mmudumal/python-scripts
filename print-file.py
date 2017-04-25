import os
def print_file(filename):
    with open(filename) as f:
        for line in f.readlines().rstrip('\n'):
            print(line)
os.chdir('/home/mmudumal/python-scripts')
print_file('pblogs_vmsodalqd022')
        
        
