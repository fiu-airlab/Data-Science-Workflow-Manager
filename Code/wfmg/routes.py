from flask import render_template
from . import server


@server.route('/')
def home_page():
    return render_template('home.html', name="user")


@server.route('/models')
def models_page():
    return render_template('models.html', name="user")


@server.route('/results')
def results_page():
    return render_template('results.html', name="user")


@server.route('/data')
def data_page():
    return render_template('data.html', name="user")


@server.route('/contact')
def contact_page():
    return render_template('contact.html', name="user")
