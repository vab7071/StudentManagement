from flask import *
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    user="root",
    password="Vaibhav@123",
    database="university",
    unix_socket="/tmp/mysql.sock"
)

mycursor = mydb.cursor()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add():

    sid = request.form['student_id']
    sname = request.form['student_name']
    email = request.form['email']
    mobile = request.form['mobile']
    course = request.form['course']
    branch = request.form['branch']
    year = request.form['year']

    sql = """
    INSERT INTO students
    VALUES(%s,%s,%s,%s,%s,%s,%s)
    """

    val = (sid,sname,email,mobile,course,branch,year)

    mycursor.execute(sql,val)
    mydb.commit()

    return redirect('/view')

@app.route('/view')
def view():

    mycursor.execute("SELECT * FROM students")
    data = mycursor.fetchall()

    return render_template("view.html",
                           students=data)
@app.route('/edit/<int:id>')
def edit(id):

    mycursor.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (id,)
    )

    student = mycursor.fetchone()

    return render_template(
        "edit.html",
        student=student
    )
@app.route('/update', methods=['POST'])
def update():

    sid = request.form['student_id']
    name = request.form['student_name']
    email = request.form['email']
    mobile = request.form['mobile']
    course = request.form['course']
    branch = request.form['branch']
    year = request.form['year']

    sql = """
    UPDATE students
    SET student_name=%s,
        email=%s,
        mobile=%s,
        course=%s,
        branch=%s,
        year_of_study=%s
    WHERE student_id=%s
    """

    values = (
        name,
        email,
        mobile,
        course,
        branch,
        year,
        sid
    )

    mycursor.execute(sql, values)
    mydb.commit()

    return redirect('/view')

@app.route('/delete/<int:id>')
def delete(id):

    mycursor.execute(
        "DELETE FROM students WHERE student_id=%s",
        (id,)
    )

    mydb.commit()

    return redirect('/view')

if __name__ == "__main__":
    app.run(debug=True, port=5001)