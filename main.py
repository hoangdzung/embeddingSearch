from flask import * 
from model import QueryMachine 
from utils import get_embeddings_from_tsv, get_meta_from_tsv
from collections import defaultdict
import json 

app = Flask(__name__)  
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
query_machine = QueryMachine()

@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        meta_f = request.files['meta_file']
        assert meta_f.filename.endswith('tsv')  
        meta_f.save(meta_f.filename)  
        types, names = get_meta_from_tsv(meta_f.filename)
        name_dict = defaultdict(list)
        for i in range(types.shape[0]):
            name_dict[types[i]].append(names[i])

        emb_f = request.files['emb_file']  
        assert emb_f.filename.endswith('tsv')
        emb_f.save(emb_f.filename)  
        embeddings = get_embeddings_from_tsv(emb_f.filename)

        query_machine.update_data(embeddings, names, types)
        print(list(set(types)))
        return render_template("success.html", meta_name = meta_f.filename, emb_name = emb_f.filename, types = list(set(types)), name_dict = name_dict)  

@app.route("/api/search", methods = ["GET"])
def search():
    src_type = request.args.get('src_type')
    src_name = request.args.get('src_name')
    target_type = request.args.get('target_type')
    print(src_type, src_name, target_type)
    k = int(request.args.get('k', 5))
    results = query_machine.search(src_type, src_name, target_type,k)
    print(results)
    return jsonify(results)

if __name__ == '__main__':  
    app.run(debug = True)  