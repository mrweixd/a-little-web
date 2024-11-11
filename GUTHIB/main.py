from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'  
SMTP_PORT = 587  
SENDER_EMAIL = 'yourmail@com'  #put your email here
SENDER_PASSWORD = 'yourpassowrd'  #and password


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def send_email(receiver_email, subject, message):
    try:
        # 設置郵件內容
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # 建立 SMTP 連接
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # 啟用TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # 登入郵箱
        server.send_message(msg)  # 發送郵件
        server.quit()  # 關閉連接

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def init_db():
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Users
                 (User_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                 User_Name TEXT UNIQUE, 
                 User_PW TEXT,
                 User_Mail TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Articles
                 (Article_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 Article_Title TEXT,
                 Article_Poster TEXT,
                 Article_Context TEXT,
                 Article_Category TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Comments
                 (Comment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 Poster TEXT,
                 Context TEXT,
                 Article_ID INTEGER,
                 FOREIGN KEY (Article_ID) REFERENCES Articles(Article_ID))''')
    conn.commit()
    conn.close()

init_db()

@app.before_request
def before_request():
    g.username = session.get('username', 'Visitor')
    g.user_id = session.get('user_id', 0)
    g.user_pw = session.get('user_pw', 0)
    g.user_mail = session.get('user_mail', 0)

@app.route('/')
def home():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "Passwords do not match"
            return render_template('register.html', error=error)
        else:
            try:
                conn = sqlite3.connect('webdata.db')
                c = conn.cursor()
                c.execute("INSERT INTO Users (User_Name, User_PW, User_Mail) VALUES (?, ?, ?)", (username, password, email))
                conn.commit()
                conn.close()
                eerror = "Registration successful"
                return render_template('signin.html', eerror=eerror)
            except sqlite3.IntegrityError:
                error = "Username or Email already exists"
                return render_template('register.html', error=error)

    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/web', methods=['GET', 'POST'])
def web():
    if g.username == 'Visitor':
        cerror = "需要登入才能發文"
        return render_template('signin.html', cerror=cerror)
        
    if request.method == 'POST':
        article_title = request.form['main']
        article_poster = session.get('username')
        article_context = request.form['postContent']
        article_category = request.form['selectedCategory']

        conn = sqlite3.connect('webdata.db')
        c = conn.cursor()

        # 將文章插入資料庫
        c.execute("INSERT INTO Articles (Article_Title, Article_Poster, Article_Context, Article_Category) VALUES (?, ?, ?, ?)",
                  (article_title, article_poster, article_context, article_category))
        conn.commit()

        # 獲取發文者的郵箱
        c.execute("SELECT User_Mail FROM Users WHERE User_Name = ?", (article_poster,))
        user_email = c.fetchone()
        if user_email:
            user_email = user_email[0]  # 提取郵件地址

        conn.close()
        
        # 發送郵件通知給發文者
        if user_email:
            subject = "發文成功!"
            message = f"您好，{article_poster},\n\n 您的文章： '{article_title}' 已成功在 '{article_category}'中發布。"
            send_email(user_email, subject, message)
        
        conn.close()
        return redirect(url_for('home'))
    return render_template('web.html')

@app.route('/1')
def article_1():
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '遊戲' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('1.html', articles=articles)

@app.route('/2')
def article_2():
    print("Accessed /2 route")
    try:
        conn = sqlite3.connect('webdata.db')
        c = conn.cursor()
        c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '日常' ORDER BY Article_ID DESC")
        articles = c.fetchall()
        conn.close()
        return render_template('2.html', articles=articles)
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred", 500

@app.route('/3')
def article_3():
    print("Accessed /3 route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '問題' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('3.html', articles=articles)

@app.route('/4')
def article_4():
    print("Accessed /4 route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '感情' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('4.html', articles=articles)

@app.route('/5')
def article_5():
    print("Accessed /5 route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '程式' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('5.html', articles=articles)

@app.route('/6')
def article_6():
    print("Accessed /6 route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '梗圖' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('6.html', articles=articles)

@app.route('/7')
def article_7():
    print("Accessed /7 route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '桐人' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('7.html', articles=articles)

@app.route('/8')
def article_8():
    print("Accessed /8 route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '閒聊' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('8.html', articles=articles)

@app.route('/9')
def article_9():
    print("Accessed /9 route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '你媽' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('9.html', articles=articles)

@app.route('/A')
def article_A():
    print("Accessed /A route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '家庭' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('A.html', articles=articles)

@app.route('/B')
def article_B():
    print("Accessed /B route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '瑟瑟' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('B.html', articles=articles)

@app.route('/C')
def article_C():
    print("Accessed /C route")
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_ID, Article_Title FROM Articles WHERE Article_Category = '其他' ORDER BY Article_ID DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('C.html', articles=articles)

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('webdata.db')
        c = conn.cursor()
        c.execute("SELECT User_Name, User_PW FROM Users WHERE User_Name = ? AND User_PW = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('login_success'))
        else:
            error = "Invalid username or password"
            return render_template('signin.html', error=error)
    return render_template('signin.html')

@app.route('/login_success')
def login_success():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session['username'] = 'Visitor'
    session['user_id'] = 0
    session['user_pw'] = 0
    session['user_mail'] = 0
    return redirect(url_for('home'))

@app.route('/api/comments/<int:article_id>', methods=['GET', 'POST'])
def handle_comments(article_id):
    if request.method == 'GET':
        conn = sqlite3.connect('webdata.db')
        c = conn.cursor()
        c.execute("SELECT Poster, Context FROM Comments WHERE Article_ID = ?", (article_id,))
        comments = c.fetchall()
        conn.close()
        comments_list = [{'poster': comment[0], 'context': comment[1]} for comment in comments]
        return jsonify(comments_list)
    elif request.method == 'POST':
        if 'username' not in session :
            return jsonify({"error": "Not logged in"}), 403

        data = request.json
        poster = session['username']
        context = data.get('context')

        if not context:
            print("No comment context provided")
            return jsonify({"error": "No comment context provided"}), 400

        print(f"Received comment from {poster}: {context}")

        conn = sqlite3.connect('webdata.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Comments (poster, Context, Article_ID) VALUES (?, ?, ?)",
                      (poster, context, article_id))
            conn.commit()
            print("Comment added successfully")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return jsonify({"error": "Database error"}), 500
        finally:
            conn.close()

        return jsonify({"success": True})

@app.route('/article/<int:article_id>')
def show_article_page(article_id):
    conn = sqlite3.connect('webdata.db')
    c = conn.cursor()
    c.execute("SELECT Article_Title, Article_Poster, Article_Context FROM Articles WHERE Article_ID = ?", (article_id,))
    article = c.fetchone()
    conn.close()
    if article:
        return render_template('article.html', title=article[0], poster=article[1], context=article[2], article_id=article_id)
    else:
        return "Article not found", 404

if __name__ == "__main__":
    
	app.run(debug=True, port=5500)
