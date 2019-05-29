from flask import Blueprint, render_template, request,redirect, session,url_for, g
import functools
from . import db

auth_blueprint= Blueprint('auth_blueprint', __name__,
                      template_folder='templates',url_prefix='/auth')

@auth_blueprint.route("/login", methods=('GET', 'POST'))
def login_router():
    if request.method == "POST":
        user_id = request.form['userid']
        user_password = request.form['password']

        db_conn = db.create_db_connection()
        connected_db_cursor = db_conn.cursor()
        connected_db_cursor.execute("select * from iis_user where userid=%s",user_id)
        user = connected_db_cursor.fetchone()
        connected_db_cursor.close()
        db_conn.close()

        if user is None :
            result_message = "no user with userid"
            return render_template("auth/login.html",result_message = result_message)
        else :
            if user["password"]==user_password :
                import datetime

                db_conn = db.create_db_connection()
                connected_db_cursor = db_conn.cursor()
                connected_db_cursor.execute("UPDATE iis_user SET recent_connection = %s",datetime.datetime.now())
                connected_db_cursor.close()
                db_conn.close()

                session['user_id'] = user["userid"]
                session['user_name'] = user["username"]

                return redirect(url_for("dashboard_blueprint.dashboard_graph_page_router"))

            else :
                result_message = "incorrect PW"
                return render_template("auth/login.html",result_message = result_message)


    elif request.method == "GET":
        if session.get("user_name") is None:
            return render_template("auth/login.html")
        else :
            return redirect(url_for('dashboard_blueprint.dashboard_graph_page_router'))


@auth_blueprint.route('/logout')
def logout_router():
    session.clear()
    return redirect(url_for('auth_blueprint.login_router'))


@auth_blueprint.before_app_request
def load_logged_in_user():
    userid = session.get('user_id')
    if userid is None:
        g.user = None
    else:
        db_conn = db.create_db_connection()
        connected_db_cursor = db_conn.cursor()
        connected_db_cursor.execute("select * from iis_user where userid=%s",userid)
        g.user = connected_db_cursor.fetchone()
        connected_db_cursor.close()
        db_conn.close()

def login_required(view):
    @functools.wraps(view)
    def check_logged_in_and_rout_to_propriate_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth_blueprint.login_router'))
        return view(**kwargs)

    return check_logged_in_and_rout_to_propriate_view