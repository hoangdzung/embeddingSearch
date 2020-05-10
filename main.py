from flask import * 
from model import QueryMachine 
from utils import get_embeddings_from_tsv, get_meta_from_tsv
from collections import defaultdict
import json 

app = Flask(__name__)  
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
query_machine = []#QueryMachine()
queryMachines = []

@app.route('/')  
def upload():  
    # return render_template("file_upload_form.html")
    dataFiles = [{
        "id" : "model1",
        "metaFile" : "Choose file",
        "embFile" : "Choose file" 
    }]
    return render_template("demo.html", datasets = dataFiles ,types = ["Empty"],name_dict = [])  

def clean(string):
    return string.replace('"','\\"')
    # to_save = ""
    # for char in string:
    #     if not char.isalpha():
    #         if char != " ":
    #             continue
    #     to_save += char
    # return to_save

@app.route('/success', methods = ['POST'])  
def success(): 
    dataFiles = [] 
    if request.method == 'POST':
        numDatasets = int(request.form['numDatasets'])
        global queryMachines
        queryMachines = []
        name_dict = defaultdict(list)
        for model in range(numDatasets):  
            meta_f = request.files['meta_file_model' + str(model + 1)]
            assert meta_f.filename.endswith('tsv')  
            meta_f.save("temp_" + meta_f.filename)  
            types, names = get_meta_from_tsv("temp_" + meta_f.filename)
            for i in range(types.shape[0]):
                name_dict[types[i]].append(clean(names[i]))
                
            emb_f = request.files['emb_file_model' + str(model + 1)]  
            assert emb_f.filename.endswith('tsv')
            emb_f.save("temp_" + emb_f.filename)  
            embeddings = get_embeddings_from_tsv("temp_" + emb_f.filename)
            query_machine = QueryMachine()
            query_machine.update_data(embeddings, names, types)
            queryMachines.append(query_machine)
            print("qm",len(queryMachines))
            dataFiles.append({
                "id" : "model" + str(model + 1),
                "metaFile" : meta_f.filename[:-4],
                "embFile" : emb_f.filename[:-4]
            })
        print(list(set(types)))
        return render_template("demo.html", datasets = dataFiles, types = list(set(types)), name_dict = name_dict)  

@app.route("/api/search/<src_type>/<src_name>/<target_type>/<k>", methods = ["GET"])
def search(src_type,src_name,target_type,k):
    results = []
    print("queryMachines",len(queryMachines))
    for qMachine in queryMachines:
        results.append(qMachine.search(src_type, src_name, target_type,int(k)))
    return jsonify(results)

if __name__ == '__main__':  
    app.run(debug = True)  