import imp
from flask import render_template, request, redirect, url_for, flash
import csv
from registro_ig import app
import os #Es para poder Borrar (delete) y renombrar (rename)
from datetime import date
from registro_ig.models import insert, select_all, select_by, delete_by
from registro_ig.forms import MovementForm

@app.route("/index")
def index():
    registros = select_all()
    return render_template("index.html", pageTitle="Todos los movimientos", data=registros)

@app.route("/new", methods=["GET", "POST"])
def new():
    form = MovementForm() #Se importa el validador
    if request.method == "GET": #Si el método es GET, muestra la página web de añadir datos (/nuevo)
        return render_template("new.html", pageTitle="Añadir movimientos", el_formulario=form, dataForm="")
#El dataForm va la html new.html y sirve para indicar un diccionario vacío para que dejemos el dato correcto en el campo que habíamos escrito
    else:
        #Hacer validación para todos los formularios
        """
        1º Validar el formulario
        Fecha válida y <= hoy
        2º Concepto no sea vacío
        3º Cantidad no sea 0 o vacía
        """
        if form.validate():
            insert([form.date.data.isoformat(),
                    form.description.data,
                    form.quantity.data])
            return redirect("/index")
        else:
            return render_template("new.html", pageTitle="Añadir movimientos", el_formulario=form)
        
        """#ERRORES --- ES MUY IMPORTANTE -- ANOTAR PARA POSTERIORES OCASIONES
        errores = validaFormulario(request.form)
        if not errores: #Viene de models.py (from registro_ing_gast.models import insert(registro))
            insert([request.form['date'],
                    request.form['description'],
                    request.form['quantity']])
            return redirect("/index") #Y lo redirige al documento index si es correcto.
            #Otra forma: return redirect(url_for("index"))
        else:
            return render_template("new.html", pageTitle="Añadir movimientos", msgErrors=errores, dataForm=dict(request.form)) #Si no es correcto, hay que volver a introducir los datos.
            #Viene de new.html -- Líneas 19 a 26 
        """

def validaFormulario(camposFormulario):
    errores = [] #Se crea una lista vacía para ir añadiendo errores
    hoy = date.today().isoformat() #Se convierte en cadena con el formato ISO (YYYY-MM-DD)
    if camposFormulario['date'] > hoy: #Si los datos introducidos en el campo de formulario de fecha son mayores a hoy
        errores.append("La fecha introducida es el futuro, introduce la fecha actual o una anterior")
    
    if camposFormulario['description'] == "": #Si no escribes nada en el campo descripción
        errores.append("Introduce un concepto para la transacción.")
    
    if camposFormulario ['quantity'] == "" or float(camposFormulario['quantity']) == "0.0": #Si está vacío o es cero
        errores.append("Introduce una cantidad positiva o negativa")
    
    return errores

@app.route("/mod", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        """
        1º Consultar en movimientos.txt y recuperar el registro con id al de la petición
        2º Devolver el formulario html con los datos de mi registro
        """
        registro_definitivo = select_by(id) #1º Consultar en movimientos.txt y recuperar el registro con id al de la petición

        if registro_definitivo:
            return render_template("mod.html", registro=registro_definitivo, pageTitle="Actualizar/Modificar") #2º Devolver el formulario html con los datos de mi registro
        else:
            return redirect(url_for("index")) #Si no, llévame a index
    else:
        """
        1º Validar registro de entrada
        2º Si el registro es correcto, lo sustituyo en movimientos.txt. La mejor manera es copiar registro a registro en fichero nuevo y dar el cambiazo
        3º Redirect
        4º Si el registro es incorrecto, la gestión de errores que conocemos
        """
        errores = validaFormulario(request.form) #1º Validar registro de entrada
    
    if not errores:
        update_by(form_to_list(id, request.form)) #Viene de la función form_to_list
        #2º Si el registro es correcto, lo sustituyo en movimientos.txt (con la función que viene de models.py: update_by(id)).
        #La mejor manera es copiar registro a registro en fichero nuevo y dar el cambiazo

        return redirect(url_for("index")) #3º Redirect
    else:
        return render_template("mod.html", pageTitle="Actualizar/Modificar", msgErrors=errores,
            registro=form_to_list(id, request.form)) #Viene de la función form_to_list
            #4º Si el registro es incorrecto, la gestión de errores que conocemos
    

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def remove(id):
    # Para probar que funciona la página: return "Voy a borrar {}".format(id)
    #registro = select_by(id)
    if request.method == "GET":
        registro = select_by(id)
        if registro:
            return render_template("delete.html", pageTitle="Eliminar movimientos", movement=select_by(id))
        else:
            flash(f"No se encuentra el registro {id}.")
            return redirect(url_for("index")) #El registro ya no existe
    else:
        delete_by(id)
        flash("Movimiento borrado correctamente.")
        return redirect(url_for("index")) #Registro borrado correctamente
