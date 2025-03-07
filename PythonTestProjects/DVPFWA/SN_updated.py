##########################3
# Encryption algorithms should be used with secure mode and padding scheme

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Example for a symmetric cipher: AES
aes = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())  # Noncompliant

# Example for a asymmetric cipher: RSA
ciphertext = public_key.encrypt(
  message,
  padding.PKCS1v15() # Noncompliant
)

plaintext = private_key.decrypt(
  ciphertext,
  padding.PKCS1v15() # Noncompliant
)

##################
# Dynamic code execution should not be vulnerable to injection attacks
from flask import request

@app.route('/')
def index():
    module = request.args.get("module")
    exec("import urllib%s as urllib" % module) # Noncompliant
	
	
#################
# HTTP request redirections should not be open to forging attacks

from flask import request, redirect

@app.route('move')
def move():
    url = request.args["next"]
    return redirect(url) # Noncompliant

from django.http import HttpResponseRedirect

def move(request):
    url = request.GET.get("next", "/")
    return HttpResponseRedirect(url) # Noncompliant
	

#######################
# Deserialization should not be vulnerable to injection attacks

from flask import request
import pickle
import yaml

@app.route('/pickle')
def pickle_loads():
    file = request.files['pickle']
    pickle.load(file) # Noncompliant; Never use pickle module to deserialize user inputs

@app.route('/yaml')
def yaml_load():
    data = request.GET.get("data")
    yaml.load(data, Loader=yaml.Loader) # Noncompliant; Avoid using yaml.load with unsafe yaml.Loader
	
	
############################
# Cryptographic key generation should be based on strong parameters

from cryptography.hazmat.primitives.asymmetric import rsa, ec, dsa

dsa.generate_private_key(key_size=1024, backend=backend) # Noncompliant
ec.generate_private_key(curve=ec.SECT163R2, backend=backend)  # Noncompliant

#############################
# Database queries should not be vulnerable to injection attacks

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from database.users import User

@app.route('hello')
def hello():
    id = request.args.get("id")
    stmt = text("SELECT * FROM users where id=%s" % id) # Query is constructed based on user inputs
    query = SQLAlchemy().session.query(User).from_statement(stmt) # Noncompliant
    user = query.one()
    return "Hello %s" % user.username
	
from django.http import HttpResponse
from django.db import connection

def hello(request):
    id = request.GET.get("id", "")
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM auth_user WHERE id=%s" % id) # Noncompliant; Query is constructed based on user inputs
    row = cursor.fetchone()
    return HttpResponse("Hello %s" % row[0])
	
	
###################################
# Databases should be password-protected
	
from mysql.connector import connection

connection.MySQLConnection(host='localhost', user='guardrails', password='')  # Noncompliant

####################################
# XPath expressions should not be vulnerable to injection attacks
from flask import request
import xml.etree.ElementTree as ET

tree = ET.parse('users.xml')
root = tree.getroot()

@app.route('/user')
def user_location():
    username = request.args['username']
    query = "./users/user/[@name='"+username+"']/location"
    elmts = root.findall(query) # Noncompliant
    return 'Location %s' % list(elmts)
	
	
###################################
# I/O function calls should not be vulnerable to path injection attacks
from flask import request, send_file

@app.route('/download')
def download():
    file = request.args['file']
    return send_file("static/%s" % file, as_attachment=True) # Noncompliant
	
###################################
# LDAP queries should not be vulnerable to injection attacks

from flask import request
import ldap

@app.route("/user")
def user():
    dn =  request.args['dn']
    username =  request.args['username']

    search_filter = "(&(objectClass=*)(uid="+username+"))"
    ldap_connection = ldap.initialize("ldap://127.0.0.1:389")
    user = ldap_connection.search_s(dn, ldap.SCOPE_SUBTREE, search_filter) # Noncompliant
    return user[0]
	
	
######################################
# OS commands should not be vulnerable to command injection attacks

from flask import request
import os

@app.route('/ping')
def ping():
    address = request.args.get("address")
    cmd = "ping -c 1 %s" % address
    os.popen(cmd) # Noncompliant
	
from flask import request
import subprocess

@app.route('/ping')
def ping():
    address = request.args.get("address")
    cmd = "ping -c 1 %s" % address
    subprocess.Popen(cmd, shell=True) # Noncompliant; using shell=true is unsafe
	

#########################################
# HTTP response headers should not be vulnerable to injection attacks

from flask import Response, request
from werkzeug.datastructures import Headers

@app.route('/route')
def route():
    content_type = request.args["Content-Type"]
    response = Response()
    headers = Headers()
    headers.add("Content-Type", content_type) # Noncompliant
    response.headers = headers
    return response	
