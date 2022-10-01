from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_bcrypt import generate_password_hash, check_password_hash
from database import Users


app = Flask(__name__)
app.secret_key = "ccccccccccccccccccccccccccccckkkkkkkkkkkkkkkkkkkk"

@app.route('/',methods=["POST","GET"])
def register():
    if request.method == "POST":
        jina = request.form["x"]
        arafa = request.form["y"]
        siri = request.form["z"]
        encrypted_password = generate_password_hash(siri)
        Users.create(name=jina, email=arafa, password=encrypted_password)
        flash("User registered successfully")
    return render_template("register.html")
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form["y"]
        password = request.form["z"]
        try:
            user = Users.get(Users.email == email)
            encrypted_password = user.password
            if check_password_hash(encrypted_password, password):
                flash("User logged in successfully")
                session["logged_in"] = True
                session["name"] = user.name
                return redirect(url_for("dashboard"))
        except Users.DoesNotExist:
            flash("wrong username or password")
    return render_template("login.html")
@app.route('/dashboard')
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    users = Users.select()
    return render_template("dashboard.html", users=users)
@app.route('/delete/<int:id>')
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    Users.delete().where(Users.id == id).execute()
    flash("user deleted successfully")
    return redirect(url_for("dashboard"))
@app.route('/update/<int:id>',methods=["POST","GET"])
def update(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user = Users.get(Users.id == id)
    if request.method == "POST":
        updatedName = request.form["x"]
        updatedEmail = request.form["y"]
        updatedPassword = request.form["z"]
        encryptedPassword = generate_password_hash(updatedPassword)
        user.name = updatedName
        user.email = updatedEmail
        user.password = encryptedPassword
        user.save()
        flash("User update successfully")
        return redirect(url_for("dashboard"))
    return render_template("update.html", user=user)
@app.route('/logout')
def logout():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    session.pop("logged_in",None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run()
