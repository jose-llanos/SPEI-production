# SPEI-production
Software: Student Prediction Early Intervention

## Instalar docker
#### - sudo apt update
#### - sudo apt install apt-transport-https ca-certificates curl software-properties-common
#### - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add –
#### - sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
#### - sudo apt update
#### - apt-cache policy docker-ce
#### - sudo apt install docker-ce

## Instalar docker compose
#### - sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
#### - sudo chmod +x /usr/local/bin/docker-compose

# Instalar python 3
#### - sudo apt-get update
#### - sudo apt-get install python3.6

## instalar el ambiente virtual (esto es opcional, solo si no se quiere usar toda la maquina, sino solo ambiente virtual)
#### - pip3 install virtualenv
#### - python3 -m venv  nombre_ambiente
#### - source nombre_ambiente/bin/activate

## Instalar las dependencias de la aplicación 
#### - pip3 install -r requirements.txt 

## Instalar el motor de bases de datos PostgreSQL
#### - docker-compose up -d

## Crear tablas de la base de datos 
#### - docker exec -i postgres pg_restore -d crud -U postgres < crud.sql

## Ejecutar la aplicación de Python (ver en local host del navegador)
#### - python3 manage.py runserver 0.0.0.0:80

- Usuario: ??
- contraseña: ??
