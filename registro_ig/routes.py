from flask import render_template, request, redirect, url_for
import csv
from registro_ig import app
import os #Es para poder Borrar (delete) y renombrar (rename)

@app.route("/index")
def index():
    return "Servidor funcionando"
