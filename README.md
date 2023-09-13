# SPEI-production

SPEI es una herramienta Web que permite realizar intervención temprana a partir de:

* Predicción del desempeño del estudiante en las semanas 3, 5 y 7 de cursos de programación. A partir de características relacionadas con: calificación de los laboratorios, tiempo utilizado en las entregas (días) y número de intentos.
* Intervención preventiva (semanas 3 y 5): Incluye la gestión de tutoría grupal, envío de sugerencias y código fuente de referencia al correo electrónico al estudiantes intervenido.
* Intervención proactiva (semana 7): Incluye el envío y seguimiento de ejercicios de programación por indicador de logro, a los estudiantes intervenidos.


## Descripción técnica

La herramienta SPEI está desarrollada en Django, un framework escrito en el lenguaje de programación Python que utiliza la arquitectura Model-Template-View para integrar la base de datos, la lógica del negocio y la presentación de los datos.  La base de datos es PostgreSQL y soporta transacciones SQL que se ejecutan dentro de un esquema. La lógica del negocio es controlada por el modelo de la aplicación, se encarga de la comunicación bidireccional entre la base de datos y la presentación. La presentación de los datos se muestra en plantillas HTML que renderizan las solicitudes y respuesta generadas por el usuario. 


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

## Crear la base de datos 
#### # docker exec -i postgres createdb spei -U postgres

## Montar el Backup de la base de datos 
#### # docker exec -i postgres pg_restore -d spei -U postgres < SPEI/BD/bk_spei_22-mayo-2023.sql

## Borrar la base de datos 
#### # docker exec -i postgres dropdb spei -U postgres

## Ejecutar la aplicación de Python (ver en local host del navegador)
#### - python3 manage.py runserver 0.0.0.0:80 &

- Usuario: ??
- contraseña: ??
