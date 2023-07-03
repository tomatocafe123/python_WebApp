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

#ログイン処理
@app.route('/', methods=['POST'])
def login():
    mail = request.form.get("mail")
    password = request.form.get('password')
   
    if db.login(mail,password):
      session['user'] = True
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

#URL
if __name__ == '__main__':
    app.run(debug=True)