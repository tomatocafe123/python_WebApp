from datetime import timedelta
from flask import Flask, render_template,request,url_for,redirect,session
import db , string , random
from root_app import root_bp

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

app.register_blueprint(root_bp)


# indexにとぶ
@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg') # Redirect された時のパラメータ受け取り
    if msg == None:# 通常のアクセスの場合
      return render_template('index.html')
    else :
     # register_exe() から redirect された場合
      return render_template('index.html',msg=msg)
  
  
    
@app.route('/', methods=['POST'])
def login_val():
    name = request.form.get("username")
    if name == "root":
      return render_template('root/root_index.html')
    else :
     # register_exe() から redirect された場合
      return render_template('login.html')



#ログイン処理
@app.route('/login', methods=['POST'])
def login():
    mail = request.form.get("mail")
    password = request.form.get('password')
   
    if db.login(mail,password):
      session['user'] = True
      session['email'] = mail
      session.permanent = True # session の有効期限を有効化
      app.permanent_session_lifetime = timedelta(minutes=30) # session の有効期限を 5 分に設定
      return redirect(url_for('toppage'))
    else :
      error = 'ユーザ名またはパスワードが違います。'
     
      input_data = {"mail":mail, 'password':password}
      return render_template('index.html', error=error)


#ログイン後のトップページにとぶ
@app.route('/toppage', methods=['GET'])
def toppage():
  if 'user' in session:
    return render_template('toppage.html') # session があれば mypage.html を表示
  else :
    return redirect(url_for('index')) #session がなければログイン画面にリダイレクト 

#session切れの時にログアウト
@app.route('/logout')
def logout():
 session.pop('user', None) # session の破棄
 return redirect(url_for('index')) # ログイン画面にリダイレクト


#ユーザ登録のページにとぶ
@app.route('/register')
def register_form():
 return render_template('account_register.html')

#ユーザ登録
@app.route('/register_exe', methods=['POST'])
def register_exe():
 user_name = request.form.get('username')
 mail = request.form.get('mail')
 password = request.form.get('password')
 count = db.insert_user(user_name,mail,password)
 if count == 1:
   msg = '登録が完了しました。'
   return redirect(url_for('index', msg=msg))
 else:
  error = '登録に失敗しました。'
  return render_template('account_register.html', error=error)


@app.route('/list')
def list():
  book_list = db.get_all_books()
    # 返すHTMLは templates フォルダ以降のパスを書きます。
  return render_template('book_list.html', books=book_list)


@app.route('/search', methods=['POST'])
def search():
  key= request.form.get('title')
  book_list = db.book_search(key)
    # 返すHTMLは templates フォルダ以降のパスを書きます。
  return render_template('book_list.html', books=book_list)




@app.route('/borrow', methods=['POST'])
def borrow():
 mail = session['email']
 title = request.form.get('title')
 isbn = request.form.get('isbn')
 
 count = db.borrow_info(mail,title,isbn)
 if count == 1:
   msg = '貸出が完了しました。'
   return redirect(url_for('toppage', msg=msg))
 else:
  error = '貸出に失敗しました。'
  return render_template('toppage.html', error=error)



@app.route('/borrow_list' )
def borrow_list():
  mail = session['email']
  borrow_list = db.get_borrow_books(mail)
    # 返すHTMLは templates フォルダ以降のパスを書きます。
  return render_template('borrow_list.html', borrows=borrow_list)


@app.route('/return_book', methods=['POST'])
def return_book():
  isbn= request.form.get('isbn')
  count = db.return_book(isbn)
  if count == 1:
   msg = '返却完了しました。'
   return redirect(url_for('toppage', msg=msg))
  else:
   error = '返却に失敗しました。'
   return render_template('toppage.html', error=error)


#URL
if __name__ == '__main__':
    app.run(debug=True)