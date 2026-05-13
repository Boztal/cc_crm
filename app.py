from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime

from models import db, User, Operation

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://cc_db_8cge_user:DpY8FYuG7qSgvBo7Ec6LKe4iv2wGD76r@dpg-d81knj3rjlhs73fub82g-a.singapore-postgres.render.com/cc_db_8cge"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secret123"

db.init_app(app)

# ---------------- CREATE TABLES ----------------
with app.app_context():
    db.create_all()

    # if not User.query.filter_by(username="maxat_cell").first():
    #     db.session.add(User(username="maxat_cell", password="29Maxata83"))
    #
    # if not User.query.filter_by(username="ereke_cell").first():
    #     db.session.add(User(username="ereke_cell", password="07Ereke84"))
    #
    db.session.commit()

# ---------------- AUTH ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    session.clear()
    error = None

    if request.method == "POST":
        username = request.form.get("user_login")
        password = request.form.get("user_password")

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["user"] = user.username
            return redirect("/list")
        else:
            error = "Wrong login or password"

    return render_template("index.html", error_message=error)


# ---------------- ADD OPERATION ----------------
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/")
    user_name = {"maxat_cell": "Шайдоллин М.К.", "ereke_cell": "Токтаров Е.Н."}
    operation_type = {"income": "Приход", "ereke_cell": "expense"}
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        op_type = request.form.get("op_type")
        description = request.form.get("description")
        date = request.form.get("date") or str(datetime.now().date())
        user = user_name[session["user"]]

        op = Operation(
            amount=amount,
            op_type=op_type,
            description=description,
            date=date,
            user=user
        )

        db.session.add(op)
        db.session.commit()

        flash("Operation added")

    return render_template("add.html")


# ---------------- LIST ----------------
@app.route("/list")
def list_page():
    if "user" not in session:
        return redirect("/")

    operations = Operation.query.all()
    return render_template("list.html", operations=operations)


# ---------------- DELETE ----------------
@app.route("/delete", methods=["POST"])
def delete():
    if "user" not in session:
        return redirect("/")
    
    op_id = request.form.get("id")

    op = Operation.query.get(op_id)
    if op:
        db.session.delete(op)
        db.session.commit()

    flash("Deleted")
    return redirect("/list")

#------------------ EDIT -----------------
@app.route("/edit", methods=["GET","POST"])
def edit_opr():
    if "user" not in session:
        return redirect("/")
    
    op_id = request.form.get("id")
    op = Operation.query.get(op_id)
    
    return render_template("/edit.html", op=op)

#-----------------UPDATE------------------
# ----------------- UPDATE ------------------
@app.route("/update", methods=["GET", "POST"])
def update_row():

    if "user" not in session:
        return redirect("/")
    user_name = {"maxat_cell": "Шайдоллин М.К.", "ereke_cell": "Токтаров Е.Н."}
    op = Operation.query.get_or_404(request.form.get("id_oper"))

    op.amount = float(request.form.get("amount"))
    op.op_type = request.form.get("op_type")
    op.description = request.form.get("description")
    op.date = request.form.get("date") or str(datetime.now().date())
    op.user = user_name[session["user"]]

    db.session.commit()

    flash("Operation changed")

    return redirect("/list")
# ---------------- REPORT ----------------
@app.route("/report", methods=["GET", "POST"])
def report():
    if "user" not in session:
        return redirect("/")

    operations = []
    income = 0
    expense = 0

    if request.method == "POST":
        d1 = request.form.get("date_bef")
        d2 = request.form.get("date_aft")

        operations = Operation.query.filter(
            Operation.date.between(d1, d2)
        ).all()

        

    all_ops = Operation.query.all()
   

    for op in all_ops:
        if op.op_type == "income":
            income += op.amount
        elif op.op_type == "expense":
            expense += op.amount

    return render_template(
        "report.html",
        operations=operations,
        cash_income=income,
        cash_expense=expense,
        cash_status=income - expense
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)