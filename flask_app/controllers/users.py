from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, tool # import entire file, rather than class, to avoid circular imports





#Create Users and sets them in session.
@app.route('/')
def create_page():
    return render_template('index.html')

@app.route('/create', methods = ["POST"])
def create_user():
    if user.User.create_user(request.form):
        return redirect('/home')
    return redirect ('/')
#Login Users and sets them in session
@app.route('/login')
def user_login_page():
    return render_template('login.html')

@app.route('/users/login' , methods = ['POST'])
def login():

    if user.User.login(request.form):
        print(session['user_id'])
        return redirect('/home')
    return redirect('/login')

#Home route where dashboard will live.
@app.route('/home')
def index():
    if 'user_id' not in session :
        return redirect('/login')
    else:
        # print(session['first_name'])
        all_fiancial_tools = tool.Tool.get_all_assets_by_user()
        return render_template('home.html', all_fiancial_tools = all_fiancial_tools)

#Create a finacial tool
@app.route('/tool/create' , methods = ["Post"])
def create_tool():
    tool.Tool.store_asset(request.form)
    return redirect('/home')

#LOGOUT/ Clears session. Prototects the rest of the routes
@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/login')

# Update Journal
@app.route('/edit/journal/<id>', methods = ['GET' ,'POST'])
def edit(id):
    if request.method == "POST":
        data = {
        'id' :request.form['id'],
        "name": request.form["name"],
        "trade_date": request.form["trade_date"],
        "asset": request.form["asset"],
        "position": request.form["position"],
        "profitorloss": request.form["profitorloss"]
        }
        tool.Tool.edit_asset(data)
        return redirect('/home')
    elif request.method == "GET":
        asset = tool.Tool.get_asset_by_id(id)

        return render_template('edit.html',asset= asset)

@app.route('/delete/journal/<id>')
def delete_journal(id):
    this_tool = tool.Tool.remove_asset(id)
    return redirect('/home')
