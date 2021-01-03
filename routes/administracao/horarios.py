import requests
from flask import Blueprint, render_template, redirect, request, json, session
from routes.main import confirmCredentials

admHorarios = Blueprint('admHorarios', __name__, template_folder='templates')


@admHorarios.route('/admHorarios')
def admHorariosTab():
    returnRedirect = confirmCredentials(1, 1)
    if returnRedirect != "":
        return redirect(returnRedirect)

    session['page'] = "admHorarios"
    return render_template('administracao/horarios/listagem.html')