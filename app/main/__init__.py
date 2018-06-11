from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap

from flask import Blueprint

from app.models import Permission

main = Blueprint('main', __name__)

from . import views, errors


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
