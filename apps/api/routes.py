# -*- encoding: utf-8 -*-

from apps.api import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/test')
@login_required
def test():

    return render_template('api/test.html')
