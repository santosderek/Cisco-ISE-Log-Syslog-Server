from flask import render_template, url_for, redirect, request
from app import website, LOGGER
from .csv_parser import step_codes
from .ise import *
import requests
from requests.auth import HTTPBasicAuth
import logging
import os
import re
import json

""" Base url """
base_url = 'https://10.122.109.116:9060'
current_user = ''
admin_login = False


@website.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@website.route('/', methods=['GET', 'POST'])
@website.route('/home/', methods=['GET', 'POST'])
def index():
    """ Home page """

    account, priv = credentials_check()
    if not account:
        return redirect("/login/")
    global step_codes
    global current_user
    global admin_login

    if request.method == 'POST':
        if request.form['submit'] == 'macAddressSearchButton':
            # LOGGER.debug("hit")
            """search = re.findall(r'\w{2}[-:.]?\w{2}[-:.]?\w{2}[-:.]?\w{2}[-:.]?\w{2}[-:.]?\w{2}',
                                request.form['macAddressField'])"""

            ip_list = re.findall('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',
                                 request.form['macAddressField'])

            LOGGER.debug(str(ip_list))
            ##################### Get all logs #####################
            with open('./app/static/logs/ciscosys.log', 'r') as current_file:
                data = current_file.read()[:-2]
                #LOGGER.debug("LOG: " + str(data))

            # Load it into a json file
            json_data = json.loads('[' + data + ']')

            """ Create a device group """
            device_group = None

            if device_group == None:
                print ("Works")

            device_group = Device_Group()
            for pos, log in enumerate(json_data):
                #LOGGER.debug("Position: " + str(pos))
                #LOGGER.debug("LOG: " + str(log))

                """ If theres a log """
                if log and 'Device IP Address' in log:
                    for ip in ip_list:
                        """ If theres an ip that matches from the user """
                        if log['Device IP Address'] == ip:
                            """ Add that log to the results """
                            log['severity_of_log'] = 'none'
                            for key, value in log.items():
                                split_key = key.split('_')
                                if split_key[0] == 'Step' and split_key[1] in step_codes:
                                    if step_codes[split_key[1]][3].lower()  == 'error' or step_codes[split_key[1]][3].lower()[:4] == 'warn':
                                        log['severity_of_log'] = 'error'
                            device_group.add_log(log)
            #######################################################

            LOGGER.debug(current_user + " : " + str(admin_login))
            LOGGER.debug(device_group.list_of_devices)
            return render_template('log_page.html',
                                   title='logs',
                                   device_group=device_group,
                                   current_user=current_user,
                                   admin_login=admin_login,
                                   step_codes=step_codes)

        elif request.form['submit'] == 'admin':
            return redirect("/admin/")

        elif request.form['submit'] == 'logoutButton':
            current_user = ''
            admin_login = False

            # return render_template('login_page.html', title='login',failed_login="none", user_already_exists="none")
            return redirect("/login/")

    elif request.method == 'GET':
        return render_template('index.html', title='Home', current_user=current_user, admin_login=admin_login)
        # return render_template('index.html', title='Home',current_user="joe@email.com")


@website.route('/admin/', methods=['GET', 'POST'])
def admin_page():
    account, priv = credentials_check()
    if not priv:
        return redirect("/login/")
    user_list = get_user_data()
    global current_user
    global admin_login
    if request.method == 'POST':
        if request.form['submit'] == 'logoutButton':
            current_user = ''
            admin_login = False
            return redirect("/login/")
        elif request.form['submit'] == 'changeUserSettings':

            user_delete_request = request.form.getlist('deleteUser')
            LOGGER.debug(str(user_delete_request))
            for user in user_list:
                user_priv_settings = request.form.getlist(
                    'radioName' + user['email'])
                LOGGER.debug("priv: " + str(user_priv_settings))
                for new_priv in user_priv_settings:
                    edit_cred_result = edit_credentials(
                        user['email'], int(new_priv[5:]))
                    LOGGER.debug(str(edit_cred_result))

            for user_to_be_deleted in user_delete_request:
                deleted_user_result = delete_user(user_to_be_deleted[11:])
                LOGGER.debug(str(deleted_user_result))

             #     user_priv_settings = request.form.getlist('radioName'+user['email'])
             #     for new_priv in user_priv_settings
             #     edit_credentials

            # return render_template('admin.html', title='admin', current_user=current_user, user_list=user_list)
            # return redirect("/home/")
            return redirect("/admin/")

        else:
            return render_template('admin.html', title='admin', current_user=current_user, user_list=user_list)
    elif request.method == 'GET':
        return render_template('admin.html', title='admin', current_user=current_user, user_list=user_list)


@website.route('/new_user/', methods=['GET', 'POST'])
def new_user_page():
    global current_user
    priv, admin = credentials_check()
    account = check_email_exists(current_user)
    LOGGER.debug("new page: " + str(account) + " : " + str(priv))
    if not account or priv:
        return redirect("/login/")

    if request.method == 'POST':
        current_user = ''
        return redirect("/login/")
    else:
        return render_template('new_user.html', title='new_user', current_user=current_user)


@website.route('/settings/', methods=['GET', 'POST'])
def settings_page():
    global current_user
    account = check_email_exists(current_user)

    if not account:
        return redirect("/login/")
    global admin_login

    if request.method == 'POST':
        if request.form['submit'] == 'logoutButton':
            current_user = ''
            admin_login = False
            return redirect("/login/")

        elif request.form['submit'] == 'admin':
            return redirect("/admin/")

        elif request.form['submit'] == 'changePasswordButton':
            found, current_pwd = getPassword(current_user)
            old_Password = request.form['oldPassword']
            new_password = request.form['newPassword']
            if found and current_pwd == old_Password:
                successful_new_password = change_password(
                    current_user, new_password)
                if successful_new_password:
                    return render_template('settings.html', title='settings', current_user=current_user, failed_change="none", successful_change="block", admin_login=admin_login)
                else:
                    return render_template('settings.html', title='settings', current_user=current_user, failed_change="block", successful_change="none", admin_login=admin_login)
            else:
                return render_template('settings.html', title='settings', current_user=current_user, failed_change="block", successful_change="none", admin_login=admin_login)
    else:
        return render_template('settings.html', title='settings', current_user=current_user, failed_change="none", successful_change="none", admin_login=admin_login)


@website.route('/login/', methods=['GET', 'POST'])
def login_page():
    global current_user
    global admin_login
    account, priv = credentials_check()
    existing_account = check_email_exists(current_user)

    if account:
        return redirect("/home/")
    elif existing_account:
        return redirect("/new_user/")

    if request.method == 'POST':
        if request.form['submit'] == 'loginButton':
            email = request.form['email']
            password = request.form['password']

            account_check = check_login(email=email, password=password)
            current_user = email
            priv_check, admin_login = check_privledge(email=email)

            if account_check and priv_check:
                return redirect("/home/")
            elif account_check:
                return redirect("/new_user/")
            else:
                return render_template('login_page.html', title='login', failed_login="block", user_already_exists="none")

        elif request.form['submit'] == 'admin':
            return redirect("/admin/")

        elif request.form['submit'] == 'createAccountButton':
            email = request.form['newEmail']
            password = request.form['newPassword']
            new_user = add_user(email=email, password=password)
            current_user = email
            if new_user:
                return redirect("/new_user/")
            else:
                return render_template('login_page.html', title='login', failed_login="none", user_already_exists="block")

    elif request.method == 'GET':
        return render_template('login_page.html', title='login', failed_login="none", user_already_exists="none")


def getPassword(email):
    users_json = "./app/static/config.json"
    with open(users_json, 'r') as f:
        userdata = json.load(f)
        for accounts in userdata:
            if email == accounts['email']:
                return True, accounts['password']
    return False, ""


def credentials_check():
    global admin_login
    global current_user
    if admin_login:
        return True, True
    else:
        account, priv = check_privledge(current_user)
        LOGGER.debug("cred check: " + str(account) + " : " + str(priv))
        return account, priv


def check_privledge(email):
    users_json = "./app/static/config.json"
    with open(users_json, 'r') as f:
        userdata = json.load(f)
        for accounts in userdata:
            if email == accounts['email'] and int(accounts['privledge']) > 0:
                if int(accounts['privledge']) >= 2:
                    return True, True
                else:
                    return True, False
    return False, False


def change_password(email, password):
    users_json = "./app/static/config.json"
    with open(users_json, 'r+') as f:
        userdata = json.load(f)
        for accounts in userdata:
            if email == accounts['email']:
                accounts['password'] = password
                f.seek(0)
                json.dump(userdata, f, indent=4)
                return True
    return False


def check_email_exists(email):
    users_json = "./app/static/config.json"
    with open(users_json, 'r') as f:
        userdata = json.load(f)
        for accounts in userdata:
            if email == accounts['email']:
                return True
    return False


def check_login(email, password):
    users_json = "./app/static/config.json"
    with open(users_json, 'r') as f:
        userdata = json.load(f)
        for accounts in userdata:
            if email == accounts['email'] and password == accounts['password']:
                return True
    return False


def add_user(email, password):
    LOGGER.debug("entered adding user")
    users_json = "./app/static/config.json"
    with open(users_json, 'r+') as f:
        userdata = json.load(f)

        for accounts in userdata:
            if email == accounts['email']:
                return False

        new_user = {}
        new_user['email'] = email
        new_user['password'] = password
        new_user['privledge'] = 0
        userdata.append(new_user)
        f.seek(0)
        json.dump(userdata, f, indent=4)
    return True


def edit_credentials(email, priv):
    LOGGER.debug("entered edit user")
    users_json = "./app/static/config.json"
    with open(users_json, 'r+') as f:
        userdata = json.load(f)

        for n, accounts in enumerate(userdata):
            if email == accounts['email']:
                userdata[n]['privledge'] = priv
                f.seek(0)
                json.dump(userdata, f, indent=4)
                return True
    return False


def delete_user(email):
    LOGGER.debug("entered delete user")
    users_json = "./app/static/config.json"
    with open(users_json, 'r+') as f:
        userdata = json.load(f)

        for accounts in userdata:
            if email == accounts['email']:
                userdata.remove(accounts)
                LOGGER.debug(str(userdata))
                f.truncate(0)
                f.seek(0)
                json.dump(userdata, f, indent=4)
                return True
    return False


def get_user_data():
    users_json = "./app/static/config.json"
    with open(users_json, 'r+') as f:
        userdata = json.load(f)
        return userdata

# #def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         login_user(user)
#
#         flask.flash('Logged in successfully.')
#
#         next = flask.request.args.get('next')
#         # is_safe_url should check if the url is safe for redirects.
#         # See http://flask.pocoo.org/snippets/62/ for an example.
#         if not is_safe_url(next):
#             return flask.abort(400)
#
#         return flask.redirect(next or flask.url_for('index'))
#     return flask.render_template('login.html', form=form)
