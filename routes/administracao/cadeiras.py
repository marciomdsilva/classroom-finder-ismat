import requests
from flask import Blueprint, render_template, redirect, request, json, session
from routes.main import confirmCredentials

admCadeiras = Blueprint('admCadeiras', __name__, template_folder='templates')


@admCadeiras.route('/admCadeiras', methods=['POST', 'GET'])
def admCadeirasTab():
    returnRedirect = confirmCredentials(1, 1)
    if returnRedirect != "":
        return redirect(returnRedirect)
    data = {}

    url = "http://127.0.0.1:5000//cursos_"
    headers = {
        'Authorization': 'Bearer ' + session['access_token'],
    }
    r = requests.request("GET", url, headers=headers, data={})


    url = "http://127.0.0.1:5000//cadeiras_"
    if request.method == 'POST':
        url = "http://127.0.0.1:5000//cadeiras_?search=" + request.form.get("search")+"&curso=" + request.form.get("curso")
        data["search"] = request.form.get("search")
        data["curso"] = request.form.get("curso")

    headers = {
        'Authorization': 'Bearer ' + session['access_token'],
    }
    r1 = requests.request("GET", url, headers=headers, data={})

    if r.status_code == 200 and r1.status_code == 200:
        data["cursos"] = r.json()["cursos"]
        data["cadeiras"] = r1.json()["cadeiras"]
        session['page'] = "admCadeiras"
        return render_template('administracao/cadeiras/listagem.html', data=data)
    else:
        return redirect("/")
