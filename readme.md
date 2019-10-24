# Endpoints de la aplicación en Producción

## Usuarios

| Feature | URL | Method |
| ------- | --- | ------ |
| Crear usuario | `/api/auth/users/` | POST

Requiere los siguientes datos:

```json
{
  "username":"nombreusuario",
  "password":"password",
  "email":"prueba@prueba.com"
}
```
devuelve:

```json
{
  "email": "prueba@prueba.com",
  "username": "nombreusuario",
  "id": 5
}
```

| Feature | URL | Method |
| ------- | --- | ------ |
| Login usuario | `/api/auth/token/login/` | POST

Requiere los siguientes datos:

```json
{
  "username":"nombreusuario",
  "password":"password"
}
```
devuelve:

```json
{
  "auth_token": "7fcfa62771ac2fd7c085c37db2f088528dbc42ee"
}
```

 Feature | URL | Method |
| ------- | --- | ------ |
| Logout usuario | `/api/auth/token/logout/` | POST

Requiere la siguiente cabecera:

```
-H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'
```
No devuelve respuesta

| Feature | URL | Method |
| ------- | --- | ------ |
| Sacar datos de un usuario | `/api/auth/users/me/` | GET

Requiere haber hecho login primero y pasar el token en la cabecera:

```
-H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'
```
devuelve:

```json
{
  "email": "prueba@prueba.com",
  "username": "nombreusuario",
  "id": 5
}
```

| Feature | URL | Method |
| ------- | --- | ------ |
| Articulos | `articulos/` | GET POST

### [Método GET]

- Requiere haber hecho login primero y pasar el token en la cabecera.
- Los artículos que se muestran son sólo los publicados [PUB].
- Los artículos se ordenan por fecha de modificación.

```
-H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'
```
devuelve artículos paginados:

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "titulo": "Articulo 1",
      "texto_introduccion": "Prueba texto"
    },
    {
      "id": 2,
      "titulo": "Articulo 2",
      "texto_introduccion": "Prueba texto"
    },
    {
      "id": 3,
      "titulo": "Articulo 2",
      "texto_introduccion": "Prueba texto"
    }
  ]
}
```
### [Búsqueda de artículos por usuario]

| Feature | URL | Method |
| ------- | --- | ------ |
| Articulos | `articulos/?usuario=id` | GET

Ejemplo:

http://api.elmoribundogarci.com/articulos/?usuario=5

Permite búsquedas por los siguientes parámetros:

```python
fields = {
            'titulo' : ['contains'],
            'usuario' : ['exact'],
            'fecha_creacion' : ['gte', 'lt', 'contains'],
            'estado' : ['exact']
        }
```
No pongo ejemplos porque no creo que vayamos a implementar esto

---

| Feature | URL | Method |
| ------- | --- | ------ |
| Detalle de artículo | `articulos/<id>` | GET POST PATCH PUT DELETE

### [Método GET]

Todos

### [Método POST|PATCH|PUT|DELETE]

Requiere haber hecho login primero y pasar el token en la cabecera. Sólo el usuario creador del artículo y un super usuario podra hacer tareas de edición (POST|PATCH|PUT|DELETE).

El [id] se autoasigna al id del usuario logado incluso si se especifica.

los campos de [fecha_creacion], [fecha_modificacion], [fecha_publicacion] se autoasignan de no enviarlos.

De lo contrario nos devolverá:

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### [Método POST]

Requiere haber hecho login primero y pasar el token en la cabecera:

```
-H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'
```
Requiere envío de datos:

```json
{
  "titulo":"Articulo 2",
  "texto_introduccion":"Prueba texto",
	"contenido":"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
	"estado":"PUB",
	"usuario":5		
}
```
estos datos están basados en el modelo que de momento es asì:

```python
class Article(models.Model):
    BORRADOR = 'DRF'
    PUBLICADO = 'PUB'

    ESTADO = [
        [BORRADOR, 'Borrador'],
        [PUBLICADO, 'Publicado']
    ]

    titulo = models.CharField(max_length=150);
    texto_introduccion = models.TextField(null=True, blank=True)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now())
    estado =  models.CharField(max_length=3, choices=ESTADO, default=BORRADOR)
    usuario = models.ForeignKey(User, related_name='articulos', on_delete=models.CASCADE)
    imagen = models.URLField(default='http://ella.practicalaction.org/wp-content/themes/ella/images/no-photo.png')
    video = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.titulo
```
De momento el usuario no se auto asigna al que tiene el login pero supongo que entre otras arreglare hoy cosas parecidas. Me gustaría dejar el PUT hecho para modificar y el DELETE.


# Importación del proyecto a local con pyCharm

- Hacemos un fetch con git del repositorio
- en pyCharm creamos un interpretador de proyecto en /file/settings/Project:welldone -> Project interpreter (idealmente la versión de python más alta que se tenga en producción estamos con la 3.7.3).

### Instalamos dependencias

Puede que antes de este paso ya habiendo configurado el intérprete haya que cerrar y abrir el proyecto para que nos salga en la línea de comandos (env)

```bash
pip install -r app/requirements.txt
```
### Importante crear un archivo .env en la raiz con las siguientes variables

```
DEBUG=True
SECRET_KEY=laquesea
DATABASE_URL=sqlite:///db.sqlite3
```

# Instalación de Django con PostgreSQL + Gunicorn + Nginx en ubuntu server 18.04 en producción

Lo primero es instalar todas las aplicaciones que vamos a necesitar con el usuario ubuntu (usuario por defecto en aws Amazon).

## Instalación de PostgreSQL, Nginx, y Circus:

```bash
sudo apt update

sudo apt-get install -y postgresql-10 postgresql-contrib-10 postgresql-server-dev-10 nginx git circus make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils python-setuptools
```

## Creamos un usuario para correr la aplicación

No es recomendable levantar aplicaciones con usuarios root. Creamos el usuario y bloqueamos el acceso al servidor por ssh con el mismo. Por último añadimos al grupo de Nginx el usuario creado este grupo suele ser www-data. Para ello en orden ejecutamos los siguientes comandos:

```bash
sudo adduser welldone
sudo passwd -l welldone
sudo adduser www-data welldone
```

## Creamos la base de datos y permitimos al usuario de la aplicación acceder a la base de datos

creamos el usuario de la aplicación desde el usuario de postgres (por defecto en la instalación de PostgresSQL). de la misma forma creamos la base de datos con ese usuario y permitimos acceso al usuario a la base de datos.

```bash
sudo -u postgres createuser welldone
sudo -u postgres createdb welldone -O welldone

```

# Puesta a punto del entorno con nuestro usuario de aplicación

Lo primero cambiamos al usuario donde residirá la aplicación.

```bash
sudo -u welldone -i 
```

## Instalamos pyenv y pyenv-virtualenv

Esto nos permite instalar diferentes versiones de python y crear entornos virtuales. ejecutamos lo siguiente:

```bash
git clone https://github.com/yyuu/pyenv.git ~/.pyenv

git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
```

Actualizamos nuestro .bash_profile para que nos funcione con nuestro usuario

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
```

para que se haga efectivo y podamos usar el comando directamente pyenv necesitaremos relogar

```bash
logout
sudo -u <app_name> -i
```

## Instalamos python con pyenv y creamos el entorno virtual (virtualenv)

Con pyenv instalamos la versión de python deseada (en nuestro caso la 3.7.3) y creamos un entorno virtual con los siguientes comandos.


```bash
pyenv install 3.7.3
pyenv virtualenv 3.7.3 venv
```

se nos crean en la ruta /home/welldone/.pyenv/versions/ las carpetas 3.7.3 y venv. Dependiendo de la costumbre el venv puede ser env pero habrá que llevarse cuidados en configuraciones posteriores.

## Configuramos la aplicación y la importamos

Clonamos la aplicación para ello ejecutamos los siguientes comandos:

```bash
git init
git remote add origin https://github.com/budahs/practica-django.git
git clone https://github.com/budahs/practica-django.git app
```

Creamos una carpeta donde meter logs

```bash
mkdir logs
```

## Cambio de variables de entorno para producciòn

En local tenemos la aplicación pasándole variables de entorno con django-environ y las guardamos en .env en la raiz del proyecto. Por lo tanto tenemos las siguientes variables sin valor o que darán fallo en producción. O bien que hay que cambiar. El archivo es el settings.py en nuestra carpeta principal en nuestro caso main/settings.py

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db()
}
```

Para ello en producción creamos un archivo de configuración desde el cual importamos el archivo settings.py de local y reemplazamos las variables que deben cambiar. Creamos el archivo.

```bash
vim app/main/settings_production.py
```
Añadimos lo siguiente:

```python
import os
from main.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['api.elmoribundogarci.com']

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

ADMINS = ((
	os.environ.get('ADMIN_EMAIL_NAME', ''), 
	os.environ.get('ADMIN_EMAIL_ADDRESS', '')
),)

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': os.environ.get('DB_NAME', ''),
       'USER': os.environ.get('DB_USER', '')
   }
}

STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', "static/"))
STATIC_URL = os.environ.get('STATIC_URL', STATIC_URL)

MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('MEDIA_ROOT', "media/"))
MEDIA_URL = os.environ.get('MEDIA_URL', "/media/")
```

## Instalamos las dependencias y gunicorn en el entorno virtual

- Primero activamos el entorno virtual
- Actualizamos pip (ojo debido a la versión de python esto ha cambiado y he tenido problemas de versiones con lo queen nuestro servidor no ejecutamos pip sino pip3.7)
- Instalamos dependencias
- Y finalmente gunicorn (es servidor WSGI HTTP para Python el equivalente a http-server en node).
- También he tenido que añadir un paquete extra psycopg2-binary porque me daba errores

```bash
pyenv activate env
pip3.7 install --upgrade pip
pip3.7 install -r app/requirements.txt
pip3.7 install gunicorn
pip3.7 install psycopg2-binary
```

## asignamos las variables de producción como variables de entorno

Yo en particular esto no me he metido a hacerlo con django environ por que no tenia claro la base de datos ya que en shell por url no podemos entrar he preferido hacerlo como lo explicaban en el tutorial. Supongo que habría que meterse a hacer binds en la config de postgreSQL y no era el momento.

Así que metemos las variables que solpamos en el app/main/settings_production.

creamos una clave secreta con openssl y la asignamos

```bash
openssl rand -base64 32
export SECRET_KEY=laclavequesalga
```

y asignamos el resto de variables:

```bash
export DB_NAME=welldone
export DB_USER=welldone
export DJANGO_SETTINGS_MODULE=main.settings_production
```

Ojo aquí hay que entender en que en el tutorial se nos dice export DJANGO_SETTINGS_MODULE=<app_name>.settings_production. Pero nosotros hemos configurado en local la carpeta de la aplicación de django como main por el tema de no repetir nombres welldone/welldone. Lo lógico siguiendo los pasos del tuto es que pusieramos:

```bash
export DJANGO_SETTINGS_MODULE=welldone.settings_production
```

Esto me dio algun quebradero de cabeza. Así que es la carpeta principal de la aplcación django que en nuestro caso se llama main.

Finalmete podemos ejecutar los cambios de modelos que tengamos en la base de datos con manage.py. Seguimos en el entorno virtual. Necesitamos entrar ya a la carpeta de nuestra proyecto app.

```bash
python manage.py makemigrations
python manage.py migrate
```

Con esto podríamos levantar un servidor directamente con gunicorn de la siguiente forma.

```bash
gunicorn -b 0.0.0.0:8000 app.wsgi
```
Pero lo que necesitamos es que el servidor corra como un servicio constante por lo que salimos del usuario welldone y procedemos con la configuración de circus.

# Configuración de circus para que ejecute el servidor con gunicorn

primero debemos crear un archivo en /etc/circus/conf.d llamado welldone.ini e introducimos lo siguiente.

```bash
[watcher:welldone]
working_dir = /home/welldone/app
cmd = gunicorn
args = -w 1 -t 180 --pythonpath=. -b 0.0.0.0:8000 main.wsgi
uid = welldone
numprocesses = 1
autostart = true
send_hup = true
stdout_stream.class = FileStream
stdout_stream.filename = /home/welldone/logs/gunicorn.stdout.log
stdout_stream.max_bytes = 10485760
stdout_stream.backup_count = 4
stderr_stream.class = FileStream
stderr_stream.filename = /home/welldone/logs/gunicorn.stderr.log
stderr_stream.max_bytes = 10485760
stderr_stream.backup_count = 4
copy_env = true
virtualenv = /home/welldone/.pyenv/versions/venv/
virtualenv_py_ver = 3.7

[env:welldone]
DJANGO_SETTINGS_MODULE = main.settings_production
SECRET_KEY = LFcsabG1A6/iR+yDVScw5W8Zp5198dJ89fvcL7hmKtM=
DB_NAME = welldone
DB_USER = welldone
```
Ojo aquí al igual que antes ojo con la configuración de DJANGO_SETTINGS_MODULE al igual que en args que por logica del tutorial hubieramos puesto:

```bash
args = -w 1 -t 180 --pythonpath=. -b 0.0.0.0:8000 welldone.wsgi
```
Esto impedía que se levantara el proceso encontrandonos en el archivo de log /home/welldone/logs/gunicorn.stderr.log el siguiente error

```bash
[2019-10-06 22:13:25 +0000] [15445] [ERROR] Exception in worker process
Traceback (most recent call last):
  File "/home/welldone/.pyenv/versions/venv/lib/python3.7/site-packages/gunicorn/arbiter.py", line 583, in spawn_worker
    worker.init_process()
  File "/home/welldone/.pyenv/versions/venv/lib/python3.7/site-packages/gunicorn/workers/base.py", line 129, in init_process
    self.load_wsgi()
  File "/home/welldone/.pyenv/versions/venv/lib/python3.7/site-packages/gunicorn/workers/base.py", line 138, in load_wsgi
    self.wsgi = self.app.wsgi()
  File "/home/welldone/.pyenv/versions/venv/lib/python3.7/site-packages/gunicorn/app/base.py", line 67, in wsgi
    self.callable = self.load()
  File "/home/welldone/.pyenv/versions/venv/lib/python3.7/site-packages/gunicorn/app/wsgiapp.py", line 52, in load
    return self.load_wsgiapp()
  File "/home/welldone/.pyenv/versions/venv/lib/python3.7/site-packages/gunicorn/app/wsgiapp.py", line 41, in load_wsgiapp
    return util.import_app(self.app_uri)
  File "/home/welldone/.pyenv/versions/venv/lib/python3.7/site-packages/gunicorn/util.py", line 350, in import_app
    __import__(module)
ModuleNotFoundError: No module named 'welldone'

```
No me encontraba el módulo. Por eso queda como:

```bash
args = -w 1 -t 180 --pythonpath=. -b 0.0.0.0:8000 main.wsgi
```

Reiniciamos el servicio circus.

```bash
sudo service circusd restart
```
# Configuramos nginx

Creamos los virtual hosts y enlazamos simbólicamente.

```bash
sudo vim /etc/nginx/sites-available/welldone

sudo ln -s /etc/nginx/sites-available/welldone /etc/nginx/sites-enabled/welldone
```
## configuración del host

```bash
server {
        listen 80;
        server_name api.elmoribundogarci.com;

        access_log /home/welldone/logs/nginx-access.log;
        error_log /home/welldone/logs/nginx-error.log;

        root /home/welldone/app/;

        client_max_body_size 10M;

        location /static {
                alias /home/welldone/app/static;
        }

    location /media {
        alias /home/welldone/app/media;
    }

        location / {
                include proxy_params;
                proxy_pass http://0.0.0.0:8000;
        }
}

```
A continuación:

```bash
sudo nginx -t
sudo service nginx restart
```

Por supuesto comprobar que el comando primero da ok antes de ejecutar el segundo.

