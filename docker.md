# Docker

docker run --name katplan_2432 -p 2432:80 -it mitch122/katplan:latest

docker run  --name katplan_2432 -p 2432:80 -it \  
     -e DJANGO_SUPERUSER_USERNAME=admin \  
     -e DJANGO_SUPERUSER_PASSWORD=michi1996 \  
     -e DJANGO_SUPERUSER_EMAIL=office@michael-web.at \  
     mitch122/katplan:1.0

# TODO

-> Fehlermeldung beim Start von Container:  
  /usr/bin/env: ‘bash\r’: No such file or directory


# URL
https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application#h-building-and-running-the-container

