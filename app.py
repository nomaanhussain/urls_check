import requests, json, threading, xlrd
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

urls = []
in_process = False

def process(links):
    global urls
    global in_process
    in_process = True
    urls = []
    for link in links: 
        r = requests.get(link)
        print(r.status_code)
        if r.status_code == 404:
            urls.append(link)
    in_process = False

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route("/run", methods=['POST'])
def process_all():
    # global in_process
    # if in_process:
    #     return jsonify({"message": "Threads are busy."})
    f = request.files['file'] 
  
    # loc = ("path of file")
    links = [] 
    data = pd.read_excel(f)
    for index, row in data.iterrows(): 
        links.append(row["Target URL"])
    process(links)
        # print(sheet.cell_value(i, 1)) 
    # with open('links.txt') as f:
    #     links = [line.rstrip() for line in f]
    # thr = threading.Thread(target=process, args=(links,))
    # thr.start()
    # print(in_process)
    return jsonify({"message": urls})

@app.route("/urls", methods=['GET'])
def get_urls():
    with open('links.txt') as f:
        links = [line.rstrip() for line in f]
    return jsonify(links)


@app.route("/404", methods=['GET'])
def status():
    global urls
    global in_process
    if in_process:
        return jsonify({"message": "In Process"})
    else:
        return jsonify(urls)

@app.route("/add_links", methods=['POST'])
def add_entries():
    if request.method == "POST":
        body = json.loads(request.data)
        links = body['urls']
        file_object = open('links.txt', 'a')
        for link in links:
            file_object.write(link)
            file_object.write("\n")
        file_object.close()
    return jsonify({"message": "Entries has been inserted."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)