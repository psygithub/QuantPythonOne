import os
import datetime

print('D:\3')
source=[R"D:\3"]
target_dir='D:\\4\\'
print(target_dir)
target=target_dir+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.zip'
zip_command='rar a %s %s'%(target,''.join(source))
print(zip_command)
count=os.system(zip_command)
if count==0:
	print('bakup to'+target+'succees')
else:
	print('backup failed')