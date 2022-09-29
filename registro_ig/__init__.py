from flask import Flask #1º

app = Flask(__name__, instance_relative_config=True) #2º Atributos de python Instance sirve para utilizar la contraseña que viene de config.py
app.config.from_object("config") #Se utiliza la contraseña

from registro_ig.routes import * #3º - De routes, impórtame todo (*)
