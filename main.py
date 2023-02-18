import os
import subprocess


# requirements.txtから一括インストール
cmd="pip install -r requirements.txt"
subprocess.run(cmd.split(' '))

cmd="python scraping/manage.py collectstatic --noinput"
subprocess.run(cmd.split(' '))

# CA証明書をDL
# cmd=os.getenv("DOWNLOAD_CA_CERT")
# subprocess.run(cmd.split(' '))

cmd="python scraping/manage.py makemigrations"
subprocess.run(cmd.split(' '))

cmd="python scraping/manage.py migrate"
subprocess.run(cmd.split(' '))

cmd="python scraping/manage.py runserver 0.0.0.0:3000"
subprocess.run(cmd.split(' '))