from flask import Flask, render_template, request, redirect, flash, session
from models import init_db, add_operation, get_operations, get_report, delete_item, get_for_edit, update_operation, get_fitered_operations, find_user
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"
init_db()

@app.route("/", methods=['GET', 'POST'])
def index_page():
    session.clear()
    user_login = None
    user_pass = None
    user_data = []
    error_message = None
  
    if request.method == 'POST':
        user_login = request.form.get('user_login')
        user_pass = request.form.get('user_password')
        user_data = find_user(user_login)
        error_message = 'Login or  pass is wrong. Try again'
        if user_data:
            if user_data[2] == user_pass:
                session['user'] = user_login
                return redirect('/list')
            else: 
                error_message
        else:
            error_message

    return render_template(
        'index.html', 
        user_login=user_login, 
        user_pass=user_pass,
        error_message=error_message
        )

@app.route("/add", methods=['GET','POST'])
def add_page():
    if 'user' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        users_names = {"maxat_cell": "Шайдоллин М.К", "ereke_cell": "Токтаров Е.Н."}
        print("POST done")
        print(request.form)
        amount_raw = request.form.get('amount')

        try:
            amount = float(amount_raw)
        except (TypeError, ValueError):
            amount = None

        op_type = request.form.get('op_type')
        description = request.form.get('description')
        if request.form.get('date'):
            date = request.form.get('date')
        else:
            date = datetime.now().date()
        user_from_session = session['user']
        user = users_names[user_from_session]

         
        add_operation(amount, op_type, description, date, user)

    return render_template('add.html')

@app.route('/list', methods=['GET', 'POST'])

def list_page():
    if 'user' not in session:
        return redirect('/')

    operations = get_operations()

    return render_template('list.html', operations=operations)

@app.route('/delete', methods=['POST'])
def delete_operation():

    operation_id = request.form.get('id')
    print(operation_id)
    delete_item(operation_id)
    flash('Запись удалена')
    return redirect('/list')

@app.route('/report', methods=['GET', 'POST'])
def report_page():
    if 'user' not in session:
        return redirect('/')
    
    filter_operations = []
    if request.method == 'POST':
        if request.form.get('date_bef'):
            data_before = request.form.get('date_bef')
        else: 
            data_before = datetime.now().date()

        if request.form.get('date_aft'):
            data_after = request.form.get('date_aft')
        else:
            data_after = datetime.now().date()
           
        filter_operations = get_fitered_operations(data_before, data_after)
    
    sum_operations = dict(get_report())
    if 'expense' in sum_operations:
        cash_expense = sum_operations['expense']
    else:
        cash_expense = 0
    if 'income' in sum_operations:
        cash_income = sum_operations['income']
    else: 
        cash_income = 0
    cash_status = cash_income - cash_expense
    return render_template(
        'report.html', 
        sum_operations=sum_operations, 
        filter_operations=filter_operations,
        cash_status=cash_status,
        cash_expense=cash_expense,
        cash_income=cash_income)

@app.route('/edit', methods=['GET', 'POST'])
def edit_operation():
    if 'user' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        edit_id = request.form.get('id')
        op = get_for_edit(edit_id)
    
    
    return render_template('edit.html', op=op)

@app.route('/update', methods=['GET', 'POST'] )
def update_data():

    users_names = {"maxat_cell": "Шайдоллин М.К", "ereke_cell": "Токтаров Е.Н."}
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        edit_id = request.form.get('id_oper')
                
        amount_raw = request.form.get('amount')
        try:
            amount = float(amount_raw)
        except (TypeError, ValueError):
            amount = None
        op_type = request.form.get('op_type')
        description = request.form.get('description')
        
        if request.form.get('date'):
            date = request.form.get('date')
            
        else:
            date = datetime.now().date()
        
        user_from_session = session['user']
        user = users_names[user_from_session]

        update_operation(edit_id, amount, op_type, description, date, user)
    flash('Запись изменена.')
    return redirect('/list')

if __name__ == '__main__':
    app.run(debug=True)