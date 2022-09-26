from flask import Flask #1º

app = Flask(__name__) #2º Atributos de python

from registro_ig.routes import * #3º - De routes, impórtame todo (*)
