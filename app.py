from flask import Flask, render_template
import wikipedia

app = Flask(__name__)

@app.route('/')
def mainRoute():
    return render_template('error.html')

@app.route('/Search/<string:lang>/<string:searchPhrase>')
def wikiSearch(searchPhrase, lang):
    wikipedia.set_lang(lang)
    return render_template('wikiSearch.html', searchlist = wikipedia.search(searchPhrase),
                                              inLang=lang,
                                              search_phrase = searchPhrase)

@app.route('/Show/<string:lang>/<string:searchPhrase>')
def wikiShow(searchPhrase, lang):
    wikipedia.set_lang(lang)
    page = wikipedia.page(searchPhrase)
    
    return render_template('wikiShow.html',  pageTitle = page.title,
                                             pageContent = page.content,
                                             pageSummary = page.summary)

@app.errorhandler(404)
def invalid_route(e):
    return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True)