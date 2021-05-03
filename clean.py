import os
import subprocess

command1 = 'git remove *.jpg'
command2 = "git commit -m 'removed images'"
command3 = 'git push'

os.system(command1)
os.system(command2)
os.system(command3)