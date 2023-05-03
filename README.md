# SPEI-production
Software: Student Prediction Early Intervention

## Instalar docker
#### - sudo apt update
#### - sudo apt install apt-transport-https ca-certificates curl software-properties-common
#### - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
#### - echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
#### - sudo apt update
#### - apt-cache policy docker-ce
#### - sudo apt install docker-ce

## Instalar docker compose
#### - sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
#### - sudo chmod +x /usr/local/bin/docker-compose

# Instalar python 3
#### - sudo apt-get update
#### - sudo apt-get install python3.6
#### - apt install python3-pip

## instalar el ambiente virtual (esto es opcional, solo si no se quiere usar toda la maquina, sino solo ambiente virtual) ESTO NO
#### - pip3 install virtualenv
#### - python3 -m venv  nombre_ambiente
#### - source nombre_ambiente/bin/activate

## Clonar el repositorio
#### - git clone https://github.com/jose-llanos/SPEI-production

## Instalar las dependencias de la aplicación 
#### - pip3 install -r requirements.txt 

## Instalar el motor de bases de datos PostgreSQL
#### - docker-compose up -d

## Crear tablas de la base de datos 
#### - docker exec -i postgres pg_restore -d spei -U root < SPEI/BD/bk_spei_01-mayo-2023.sql

## Ejecutar la aplicación de Python (ver en local host del navegador)
#### - python3 manage.py runserver 0.0.0.0:8000

- Usuario: ??
- contraseña: ??
