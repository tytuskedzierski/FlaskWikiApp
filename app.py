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

mainColor = '#ababab'

@app.route('/')
def mainRoute():
    try:
        connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
        cursor = connection.cursor()
        sql_query = 'SELECT id_stamp, searchPhrases, lang FROM wiki ORDER BY id_stamp DESC LIMIT 80'
        cursor.execute(sql_query)
        previousSearch = cursor.fetchall()
        connection.close()
        return render_template('main.html', previous_search = previousSearch,
                                            defaultLang = defaultLanguage,
                                            app_address = appAddress,
                                            main_color = mainColor)
    except:
        return render_template('error.html', error_message = 'db connection error / sql error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)


@app.route('/Add/<string:lang>/<string:searchPhrase>/')
def wikiDbInsert(searchPhrase, lang):
    try:
        connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
        cursor = connection.cursor()
        insert_query = '''INSERT INTO wiki (searchPhrases, lang) values('%s','%s')''' %(searchPhrase, lang)
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
    except:
        return render_template('error.html', error_message = 'db connection error / sql error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)
    return("Record inserted")

@app.route('/Delete/<int:id>/')
def wikiDbDelete(id):
    try:
        connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
        cursor = connection.cursor()
        delete_query = '''DELETE FROM wiki WHERE id_stamp =' ''' + str(id) + ''' ';'''
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
    except:
        return render_template('error.html', error_message = 'db connection error / sql error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)
    return("Record deleted")

@app.route('/Update/<int:id>/<string:lang>/<string:searchPhrase>')
def wikiDbUpdate(id, searchPhrase, lang):
    try:
        connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
        cursor = connection.cursor()
        update_query = '''UPDATE wiki SET lang = ''' +'\'' + str(lang) +'\'' ''' ,searchPhrases = '''  +'\'' + str(searchPhrase) +'\'' + ''' WHERE id_stamp =' ''' + str(id) + ''' ';'''
        cursor.execute(update_query)
        connection.commit()
        connection.close()
    except:
        return render_template('error.html', error_message = 'db connection error / sql error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)
    return("Record updated")

@app.route('/Table/')
def wikiTable():
    try:
        connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
        cursor = connection.cursor()
        sql_query = 'SELECT id_stamp, searchPhrases, lang FROM wiki ORDER BY id_stamp DESC'
        cursor.execute(sql_query)
        previousSearch = cursor.fetchall()
        connection.close()
    except:
        return render_template('error.html', error_message = 'db connection error / sql error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)
    
    return render_template('table.html', defaultLang = defaultLanguage,
                                                  previous_search = previousSearch,
                                                  app_address = appAddress,
                                                  main_color = mainColor)

@app.route('/Search/<string:lang>/<string:searchPhrase>')
def wikiSearch(searchPhrase, lang):
    try:
        connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
        cursor = connection.cursor()
        sql_query = 'SELECT id_stamp, searchPhrases, lang FROM wiki WHERE lang =' +'\'' + lang  +'\'' + ' ORDER BY id_stamp DESC LIMIT 100'
        cursor.execute(sql_query)
        previousSearch = cursor.fetchall()
        connection.close()
    except:
        return render_template('error.html', error_message = 'db connection error / sql error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)
    try:
        wikipedia.set_lang(lang)
        return render_template('wikiSearch.html', searchlist = wikipedia.search(searchPhrase),
                                                  inLang=lang,
                                                  search_phrase = searchPhrase,
                                                  defaultLang = defaultLanguage,
                                                  previous_search = previousSearch,
                                                  app_address = appAddress,
                                                  main_color = mainColor)
    except:
        return render_template('error.html', error_message = 'wikipedia connection error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)

@app.route('/Show/<string:lang>/<string:searchPhrase>')
def wikiShow(searchPhrase, lang):
    try:
        wikipedia.set_lang(lang)
        page = wikipedia.page(searchPhrase)
        try:
            connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
            cursor = connection.cursor()
            insert_query = '''INSERT INTO wiki (searchPhrases, lang) values('%s','%s')''' %(page.title, lang)
            cursor.execute(insert_query)
            connection.commit()
            connection.close()
        except:
            return render_template('error.html', error_message = 'db connection error / sql error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)
        
        return render_template('wikiShow.html',  pageTitle = page.title,
                                                 pageContent = page.content,
                                                 pageSummary = page.summary,
                                                 inLang=lang,
                                                 defaultLang = defaultLanguage,
                                                 searchlist = wikipedia.search(searchPhrase),
                                                 app_address = appAddress,
                                                 main_color = mainColor)
    except:
        return render_template('error.html', error_message = 'wikipedia connection error / query error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)

@app.errorhandler(404)
def invalid_route(e):
    try:
        connection = pymysql.connect(dbAddress, dbUser, dbPass, dbName)
        cursor = connection.cursor()
        sql_query = 'SELECT id_stamp, searchPhrases, lang FROM wiki ORDER BY id_stamp DESC LIMIT 80'
        cursor.execute(sql_query)
        previousSearch = cursor.fetchall()
        connection.close()
        return render_template('main.html', previous_search = previousSearch,
                                             defaultLang = defaultLanguage,
                                             app_address = appAddress,
                                             main_color = mainColor)
    except:
        return render_template('error.html', error_message = 'db connection error / sql error',
                                                  app_address = appAddress,
                                                  main_color = mainColor)


if __name__ == "__main__":
    app.run(debug=True)