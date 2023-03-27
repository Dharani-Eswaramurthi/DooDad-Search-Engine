from flask import Flask, request, jsonify, render_template
from search import search
from storage import DBStorage
import html
from filter import Filter
from storage import DBStorage

app = Flask(__name__)

with open('templates/template.html', 'r') as f:
    search_template = f.read()

with open('templates/rendered_template.html','r') as h:
    ren_search_template=h.read()

with open('templates/result.html', 'r') as g:
    result_template = g.read()

 

def show_search_form():
        return search_template

def run_search(query):
    results = search(query)
    fi = Filter(results)
    results= fi.filter()
    rendered = ren_search_template
    results["snippet"] = results["snippet"].apply(lambda x: html.escape(x))
    for index, row in results.iterrows():
        rendered += result_template.format(**row)
    return rendered


@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form.get("query")
        return run_search(query)
    else:
        return show_search_form()

    


