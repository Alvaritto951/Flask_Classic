from flask import render_template, request, redirect, url_for
import csv
from registro_ig import app
import os #Es para poder Borrar (delete) y renombrar (rename)

from registro_ig.models import select_all 

@app.route("/index")
def index():
    registros = select_all()
    return render_template("index.html", pageTitle="Todos los movimientos", data=registros)

