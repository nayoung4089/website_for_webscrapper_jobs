from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("JobScrapper")

db = {}
# 한번 크롤링한 후엔 여기다가 저장해서, 똑같은 거 다음 검색 때는 로딩시간 단축

@app.route("/")
# 내 원래 웹사이트 https://flaskpy.un19991217.repl.co에 / 붙여주면 거기로 이동할 수 있거든!! 그래서 이동시켜주려고 / 추가한 것
def home():
  return render_template('home.html')

@app.route("/report")
def report():
  word = request.args.get('word')
  # 우리가 입력한 값이 word로 지칭된다고 했는데, 그 값을 가져오라고 명령하는 것
  if word:
    #word 값이 존재하면
    word = word.lower()   # 대문자로 입력해도 소문자로 출력하라는 코드
    fromDB = db.get(word)
    # db에 이미 저장된 단어가 있는가? 확인해주기 위해서 if else 작성
    if fromDB:
      #formDB가 존재하면 = db에 저장된 단어를 검색했다면
      jobs = fromDB  # 그냥 그거 보여주세요 (웹사이트 크롤링 안 해도 됨)
    else:  
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
    # 메인 페이지(home)으로 오라는 명령
  return render_template("report.html", searchingBy=word, resultNumber=len(jobs), jobs =jobs)
  # word = 이름, len(jobs) = 직업개수, jobs에 대한 모든 정보를 report.html에 넘겨주겠다는 말

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
      # word가 존재하지 않으면 에러를 발생 --> except로 인해 메인 페이지로 이동
    word = word.lower()
    jobs = db.get(word)
    # db에서 자료를 가져온다 
    if not jobs:
      raise Exception()
      # jobs가 없으면 에러 발생
    save_to_file(jobs)
    # csv 파일에 저장된 것으 불러오기
    return send_file("jobs.csv")
    # csv 파일 이름이 jobs.csv/ send_file은 flask 내장함수

  except:
    return redirect("/")  
    # word를 입력하지 않았으면 메인 페이지로 다시 오게 만든다
# try 해서 오류가 뜨면 except가 된다


@app.route("/<username>")
def contact(username):
  return f"Hello, {username} What are you doing?"

app.run(host="0.0.0.0")