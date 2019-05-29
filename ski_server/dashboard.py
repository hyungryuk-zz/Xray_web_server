from flask import Blueprint, render_template, request,redirect, session,url_for, g
from . import db
from . import auth

dashboard_blueprint= Blueprint('dashboard_blueprint', __name__,
                   template_folder='templates',url_prefix='/dashboard')


@dashboard_blueprint.route("/graph")
@auth.login_required
def dashboard_graph_page_router():
    return render_template("dashboard/graph.html")

@dashboard_blueprint.route("/statistics")
@auth.login_required
def dashboard_statistic_page_router():
    return render_template("dashboard/statistics.html")

@dashboard_blueprint.route("/classification_result")
@auth.login_required
def dashboard_classification_result_page_router():
    return render_template("dashboard/classification_result.html")
