import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template)
import utils
import json

# Static Routes

@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")

@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")

@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")

@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

@route('/browse')
def browse():
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=utils.getShowData())

@route('/search')
def search():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

@post('/search')
def search_result():
    query = request.forms.get('q')
    sectionTemplate = "./templates/search_result.tpl"
    return template("./pages/index.html", version=utils.getVersion(),sectionTemplate=sectionTemplate, query=query, results= utils.search(query), sectionData={})

@route('/ajax/show/<show>')
def show(show):
    sectionData = json.loads(utils.getJsonFromFile(show))
    return template("./templates/show.tpl", version=utils.getVersion(), result=sectionData)
    
@route('/ajax/show/<show>/episode/<episode>')
def episode(show, episode): 
    sectionData = json.loads(utils.getJsonFromFile(show))
    for ep in sectionData['_embedded']['episodes']:
        if ep["id"] == int(episode):
            sectionData= ep
            break

    return template("./templates/episode.tpl", version=utils.getVersion(), result=sectionData)
    

if __name__ == "__main__":
    run(host='localhost', port=os.environ.get('PORT', 5000), reloader=True, debug=True)
