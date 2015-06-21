from app import (app,db,auth)
from app.models import User
from flask import (request, abort, jsonify, url_for, g)
from flask_login import (login_user, logout_user, current_user, login_required)
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
@app.route('/api/users',methods=["POST"])
def api_register():
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        username = None
        password = None
    if username is None or password is None:
        return jsonify({
            "status": "error",
            "error": "Missing arguments",
            "message": "Not username or password sent"
        })
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            "status": "error",
            "error": "Existing user",
            "message": "User already exists, username is already taken"
        })
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {'username': user.username,
         "status":"success",
         "id":user.id}),\
           201,\
           {'Location': url_for('get_user', id = user.id, _external=True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({
            "status":"error",
            "error":"User not found",
            "message":"This id doesn't have a user assigned"
        })
    return jsonify({'username': user.username,"status": "success"})
@app.route('/api/login', methods=["POST"])
def api_login_user():
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        username = None
        password = None
    if username is None or password is None:
        return jsonify({
            "status": "error",
            "error": "Missing arguments",
            "message": "Not username or password sent"
        })
    try:
        user = User.query.filter_by(username=username).first()
        if isinstance(user,type(None)):
            return jsonify({
                "status":"error",
                "error":"user doesn't exists"
            })
        if user.verify_password(password):
            login_user(user)
            return jsonify({
                "status":"success",
                "username":user.username,
                "id":user.id
            })
        else:
            return jsonify({
                "status":"error",
                "error":"wrong password"
            })
    except Exception as e:
        return jsonify({
            "status":"error",
            "error":unicode(e)
        })
@app.route('/api/logout')
@login_required
def api_logout_user():
    logout_user()
    return jsonify({
        "status":"success",
    })

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
@app.route("/api/deny")
def deny():
    g.user = None
    abort(401)