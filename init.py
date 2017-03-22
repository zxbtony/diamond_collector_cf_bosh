from subprocess import PIPE, STDOUT, Popen
import os
import time

cmd = "cf api %s" % os.environ["CF_TARGET_HOST"]
p = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
time.sleep(5)

cmd = "cf login -u %s -p %s -o %s" % (os.environ["CF_ADMIN_USER"],os.environ["CF_ADMIN_PWD"],os.environ["CF_ORG"])
p = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
time.sleep(5)

cmd = "bosh target %s" % os.environ['BOSH_TARGET_HOST']
usr_pwd = "%s\n%s\n" % (os.environ["BOSH_ADMIN_USER"],os.environ["BOSH_ADMIN_PWD"])
p = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
time.sleep(1)
p.communicate(input=usr_pwd)[0]
time.sleep(5)
