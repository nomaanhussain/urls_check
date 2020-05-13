import requests, json, threading
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
        if r.status_code == 404:
            urls.append(link)
    in_process = False
    

@app.route("/", methods=['GET'])
def process_all():
    if in_process:
        return jsonify({"message": "Threads are busy."})
    links = []
    with open('links.txt') as f:
        links = [line.rstrip() for line in f]
    thr = threading.Thread(target=process, args=(links,))
    thr.start()
    return jsonify({"message": "Process is started."})


@app.route("/", methods=['POST'])
def process_some():
    if in_process:
        return jsonify({"message": "Threads are busy."})
    if request.method == "POST":
        body = json.loads(request.data)
        links = body['urls']
        thr = threading.Thread(target=process, args=(links,))
        thr.start()
    return jsonify({"message": "Process is started."})


@app.route("/status", methods=['GET'])
def status():
    global urls
    return jsonify({"url": urls})


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