from datetime import timedelta
from flask import Blueprint, render_template,request,url_for,redirect,session
import root_db, string , random

root_bp = Blueprint('root', __name__, url_prefix='/root')
root_bp.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


# indexにとぶ
@root_bp.route('/', methods=['GET'])
def root_index():
    msg = request.args.get('msg') # Redirect された時のパラメータ受け取り
    if msg == None:# 通常のアクセスの場合
      return render_template('root/root_index.html')
    else :
     # register_exe() から redirect された場合
      return render_template('root/root_index.html',msg=msg)

#ログイン処理
@root_bp.route('/', methods=['POST'])
def root_login():
    id = request.form.get("id")
    password = request.form.get('password')
   
    if root_db.login(id,password):
      session['user'] = True
      session.permanent = True # session の有効期限を有効化
      root_bp.permanent_session_lifetime = timedelta(minutes=30) # session の有効期限を 5 分に設定
      return redirect(url_for('root.root_toppage'))
    else :
      error = 'IDまたはパスワードが違います。'
     
      input_data = {"id":id, 'password':password}
      return render_template('root/root_index.html', error=error)


#ログイン後のトップページにとぶ
@root_bp.route('/root_toppage', methods=['GET'])
def root_toppage():
  if 'user' in session:
    return render_template('root/root_toppage.html') # session があれば mypage.html を表示
  else :
    return redirect(url_for('index')) #session がなければログイン画面にリダイレクト 

#session切れの時にログアウト
@root_bp.route('/logout')
def logout():
 session.pop('user', None) # session の破棄
 return redirect(url_for('root.root_index')) # ログイン画面にリダイレクト



#ユーザ登録のページにとぶ
@root_bp.route('/register')

def root_register():  #<< 新規登録url
  
 return render_template('root_register.html')


#ユーザ登録
@root_bp.route('/register_exe', methods=['POST'])
def register_exe():
 id = request.form.get('id')
 password = request.form.get('password')
 count = root_db.insert_user(id,password)
 if count == 1:
   msg = '登録が完了しました。'
   return redirect(url_for('root_index', msg=msg))
 else:
  error = '登録に失敗しました。'
  return render_template('root_register.html', error=error)





#本の登録のページにとぶ
@root_bp.route('/book_register')
def book_register_form():
 return render_template('root/book_register_form.html')

#本の登録
@root_bp.route('/book_register_exe', methods=['POST'])
def book_register_exe():
  title= request.form.get('title')
  publisher= request.form.get('publisher')
  author=request.form.get("author")
  isbn=request.form.get("isbn")
  count = root_db.register_book(title,publisher,author,isbn)
  if count == 1:
   msg = '登録が完了しました。'
   return redirect(url_for('root.root_toppage', msg=msg))
  else:
   error = '登録に失敗しました。'
   return render_template('root.book_register_form.html', error=error)
 
 

@root_bp.route('/book_list')
def book_root_list():
  book_list = root_db.get_all_books()
    # 返すHTMLは templates フォルダ以降のパスを書きます。
  return render_template('root/book_root_list.html', books=book_list)


@root_bp.route('/root_book_search', methods=['POST'])
def root_book_search():
  key= request.form.get('title')
  book_list = root_db.root_book_search(key)
    # 返すHTMLは templates フォルダ以降のパスを書きます。
  return render_template('root/book_root_list.html', books=book_list)


@root_bp.route('/delete_book', methods=['POST'])
def delete_book():
  id= request.form.get('id')
  count = root_db.delete_book(id)
  if count == 1:
   msg = '削除完了しました。'
   return redirect(url_for('root.root_toppage', msg=msg))
  else:
   error = '削除に失敗しました。'
   return render_template('root/root_toppage.html', error=error)
  