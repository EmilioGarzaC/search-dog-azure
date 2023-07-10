import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

# > FUNCIONES

def search(palabra, path_diccionario, path_documentos):
    #Indica al usuario escribir la palabra a buscar
    #palabra = input("Escribe la palabra a buscar: ")
    #La palabra se cambia a minúsculas en caso de que no sea así
    palabra = palabra.lower()
    results = []
    df_diccionario = pd.read_csv(path_diccionario, sep=';', names=["TOKEN", "REPETICIONES", "UBICACION"])
    if palabra in df_diccionario["TOKEN"].values:
        dict_index = df_diccionario[df_diccionario['TOKEN'] == palabra].index
        row_start = df_diccionario.iloc[dict_index]
        row_end = df_diccionario.iloc[dict_index+1]
        p_index_start = row_start['UBICACION'].values[0]
        p_index_end = row_end['UBICACION'].values[0]
        df_documentos = pd.read_csv(path_documentos)
        for i in range(p_index_start, p_index_end):
            doc_row = df_documentos.loc[df_documentos['ID'] == i]
            doc_name = doc_row["DOCUMENTO"].values[0]
            results.append(doc_name)
        print("RESULTADOS DE BUSQUEDA")
        print(results)
        
        return {
            'documentos': results,
            'p_start': p_index_start,
            'p_end': p_index_end,
        }
    else:
        print(f"{palabra} no existe en el diccionario")
        return False
    
    
# > FLASK ROUTES

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/hello', methods=['POST'])
def hello():

    name = request.form.get('name')
    if name is None:
        data = request.json
        name = data.get('name')
    searchResults = search(
        palabra=name, 
        path_diccionario='output-files/diccionario.txt', 
        path_documentos='output-files/index_documents.txt'
    )

    if name:
        print('Request for search page received with token=%s' % name)
        return render_template('hello.html', name = name, searchResults = searchResults)
    else:
        print('Request for search page received with no token or blank token -- redirecting')
        return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == '__main__':
   app.run()
