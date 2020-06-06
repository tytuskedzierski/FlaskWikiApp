from flask import Flask, render_template
import wikipedia
import pymysql

app = Flask(__name__)

defaultLanguage = 'pl'
appAddress = 'http://localhost:5000'
dbAddress = 'localhost'
dbUser = 'root'
dbPass = '112233654'
dbName = 'crypto'

@app.route('/')
def mainRoute():
    connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
    cursor = connection.cursor()
    sql_query = 'SELECT id_stamp, searchPhrases, lang FROM wiki ORDER BY id_stamp DESC LIMIT 80'
    cursor.execute(sql_query)
    previousSearch = cursor.fetchall()
    connection.close()
    return render_template('error.html', previous_search = previousSearch,
                                         defaultLang = defaultLanguage,
                                         app_adress = appAddress)

@app.route('/Search/<string:lang>/<string:searchPhrase>')
def wikiSearch(searchPhrase, lang):
    connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
    cursor = connection.cursor()
    sql_query = 'SELECT id_stamp, searchPhrases, lang FROM wiki WHERE lang =' +'\'' + lang  +'\'' + ' ORDER BY id_stamp DESC LIMIT 100'
    cursor.execute(sql_query)
    previousSearch = cursor.fetchall()
    connection.close()
    wikipedia.set_lang(lang)
    return render_template('wikiSearch.html', searchlist = wikipedia.search(searchPhrase),
                                              inLang=lang,
                                              search_phrase = searchPhrase,
                                              defaultLang = defaultLanguage,
                                              previous_search = previousSearch,
                                              app_adress = appAddress)

@app.route('/Show/<string:lang>/<string:searchPhrase>')
def wikiShow(searchPhrase, lang):
    wikipedia.set_lang(lang)
    page = wikipedia.page(searchPhrase)
    connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
    cursor = connection.cursor()
    insert_query = '''INSERT INTO wiki (searchPhrases, lang) values('%s','%s')''' %(searchPhrase, lang)
    cursor.execute(insert_query)
    connection.commit()
    connection.close()
    return render_template('wikiShow.html',  pageTitle = page.title,
                                             pageContent = page.content,
                                             pageSummary = page.summary,
                                             inLang=lang,
                                             defaultLang = defaultLanguage,
                                             app_adress = appAddress)

@app.errorhandler(404)
def invalid_route(e):
    connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
    cursor = connection.cursor()
    sql_query = 'SELECT id_stamp, searchPhrases, lang FROM wiki ORDER BY id_stamp DESC LIMIT 80'
    cursor.execute(sql_query)
    previousSearch = cursor.fetchall()
    connection.close()
    return render_template('error.html', previous_search = previousSearch,
                                         defaultLang = defaultLanguage,
                                         app_adress = appAddress)


if __name__ == "__main__":
    app.run(debug=True)