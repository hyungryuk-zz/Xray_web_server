from flask import Blueprint, render_template, request,redirect, session,url_for, g
import functools
from . import db
import enum


class Login_result_message(enum.IntEnum):
    PASSWORD_INVALID = 0
    NO_USER_FOUND= 1
    LOGIN_SUCCESS = 2

auth_blueprint= Blueprint('auth_blueprint', __name__,
                      template_folder='templates',url_prefix='/auth')

@auth_blueprint.route("/login", methods=('GET', 'POST'))
def login_router():
    if request.method == "POST":
        input_user_id = request.form['userid']
        input_user_password = request.form['password']
        login_result = user_login(input_user_id,input_user_password)

        if login_result==Login_result_message.LOGIN_SUCCESS:
            return redirect(url_for("dashboard_blueprint.dashboard_graph_page_router"))
        elif login_result==Login_result_message.NO_USER_FOUND:
            return render_template("auth/login.html",result_message = "no user with userid")
        else:
            return render_template("auth/login.html",result_message = "incorrect PW")

    elif request.method == "GET":
        if session.get("user_name") is None:
            return render_template("auth/login.html")
        else :
            return redirect(url_for('dashboard_blueprint.dashboard_graph_page_router'))

def user_login(input_user_id,input_password):
    user = get_user_from_db(input_user_id)
    if user is None :
        return Login_result_message.NO_USER_FOUND
    elif user["password"] != input_password:
        return Login_result_message.PASSWORD_INVALID
    else:
        update_user_connect_time_in_db(user["userid"])
        add_user_to_session(user)
        return Login_result_message.LOGIN_SUCCESS

def get_user_from_db(user_id):
    return db.DB().run_query_with_one_return("select * from iis_user where userid=%s",user_id)

def update_user_connect_time_in_db(user_id):
    import datetime
    db.DB().run_query_with_no_return("UPDATE iis_user SET recent_connection = %s WHERE userid = %s",[datetime.datetime.now(),user_id])

def add_user_to_session(user):
    session['user_id'] = user["userid"]
    session['user_name'] = user["username"]

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
        g.user = db.DB().run_query_with_one_return("select * from iis_user where userid=%s",userid)

def login_required(view):
    @functools.wraps(view)
    def check_logged_in_and_rout_to_propriate_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth_blueprint.login_router'))
        return view(**kwargs)

    return check_logged_in_and_rout_to_propriate_view