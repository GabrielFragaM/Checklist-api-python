from flask.json import jsonify
import requests
import json
import time
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore, storage, initialize_app
from flask import Flask, request
import json

app = Flask(__name__)
cred = credentials.Certificate('checklist_firebase.json')
initialize_app(cred, {'storageBucket': 'gererador-qr-code.appspot.com'})
db = firestore.client()

#################CRUD API#################################


####METODO EDITAR CHECKLIST############
@app.route('/api/checklists/edit_data/checklist/', methods=['PUT'])
def edit_checklist():
    try:
        json_data_edit_checklist = request.json
        User_id = json_data_edit_checklist['user_id']
        checklist = json_data_edit_checklist['uid_checklist']
    

        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('checklists').document(checklist).update(json_data_edit_checklist)
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('categorias').document(cat.id).collection('checklists').document(checklist).update(json_data_edit_checklist)
        except:
            pass
        response = jsonify({'message':'Editado com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível editar a checklist.' + str(e)})
        return response, 500

####METODO DELETAR CHECKLIST############
@app.route('/api/checklists/delete_data/checklist/', methods=['GET'])
def detele_checklist():
    try:
        json_data_delete_checklist = str(request.args['Account'])
        json_data_delete_checklist = json_data_delete_checklist.split('/')
        User_id = json_data_delete_checklist[0]
        checklist = json_data_delete_checklist[1]
    
        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('checklists').document(checklist).delete()
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('categorias').document(cat.id).collection('checklists').document(checklist).delete()
        except:
            pass
        response = jsonify({'message':'Checklist deletada com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível deletar a checklist. Mais detalhes: ' + str(e)})
        return response, 500

####METODO DELETAR VERIFICACAO############
@app.route('/api/verificacoes/delete_data/verificacao/', methods=['GET'])
def detele_verificacao():
    try:
        json_data_delete_verificacao = str(request.args['Account'])
        json_data_delete_verificacao = json_data_delete_verificacao.split('/')
        User_id = json_data_delete_verificacao[0]
        verificacao = json_data_delete_verificacao[1]
    
        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).delete()
        try:
            checklits_data = db.collection('accounts').document(User_id).collection('checklists').get()
            for c in checklits_data:
                db.collection('accounts').document(User_id).collection('checklists').document(c.id).collection('verificacoes').document(verificacao).delete()
        except:
            pass
        response = jsonify({'message':'Verificação deletada com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível deletar a Verificação. Mais detalhes: ' + str(e)})
        return response, 500

####METODO CRIAR CHECKLIST############
@app.route('/api/checklists/create_data/checklist/', methods=['POST'])
def create_checklist():
    try:
        json_data_edit_checklist = request.json
        User_id = json_data_edit_checklist['user_id']
        descricao = json_data_edit_checklist['descricao']
        observacao = json_data_edit_checklist['observacao']
        title = json_data_edit_checklist['title']

        dict_checklist = {'descricao': descricao, 'observacao': observacao, 'title': title,
        'CategoriasID': 'NaN', 'deleted_categoria': True, 'icon': 'https://firebasestorage.googleapis.com/v0/b/connect-my-health-24512.appspot.com/o/edit_viagem.png?alt=media&token=d4c2ecde-9e3c-446b-89f0-d8d5d605e1f6'
        }

        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('checklists').add(dict_checklist)
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('checklists').add(dict_checklist)
        except:
            pass
        response = jsonify({'message':'Checklist criada com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível criar uma checklist. Mais detalhes: ' + str(e)})
        return response, 500
############################################################

####METODO EDITAR PERGUNTAS############
@app.route('/api/perguntas/edit_data/pergunta/', methods=['PUT'])
def edit_pergunta():
    try:
        json_data_edit_pergunta = request.json
        User_id = json_data_edit_pergunta['user_id']
        pergunta = json_data_edit_pergunta['uid_pergunta']
        checklist = json_data_edit_pergunta['uid_checklist']

        #####EDITANDO OS DADOS DA CHECKLIST####################
        db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').document(pergunta).update(json_data_edit_pergunta)
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('categorias').document(cat.id).collection('checklists').document(checklist).collection('perguntas').document(pergunta).update(json_data_edit_pergunta)
        except:
            pass
        response = jsonify({'message':'Editado com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível editar o item.' + str(e)})
        return response, 500

####METODO CRIAR PERGUNTAS############
@app.route('/api/perguntas/create_data/pergunta/', methods=['POST'])
def create_pergunta():
    try:
        json_data_edit_checklist = request.json
        User_id = json_data_edit_checklist['user_id']
        checklist = json_data_edit_checklist['uid_checklist']
        images = json_data_edit_checklist['images']
        observacao = json_data_edit_checklist['observacao']
        pergunta = json_data_edit_checklist['pergunta']

        dict_pergunta = {'images': images, 'observacao': observacao, 'pergunta': pergunta,
        }

        db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').add(dict_pergunta)
        try:
            categorias_data = db.collection('accounts').document(User_id).collection('categorias').get()
            if(len(categorias_data) != 0):
                for cat in categorias_data:
                    db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').add(dict_pergunta)
        except:
            pass
        response = jsonify({'message':'Item criado com sucesso.'})
        return response, 200
    except Exception as e:
        response = jsonify({'message':'Não foi possível criar um novo Item. Mais detalhes: ' + str(e)})
        return response, 500
################ACESSAR DADOS DO FIREBASE####################

#####METODO PARA PEGAR TODAS AS INFO DO PAINEL############
@app.route('/api/painel/get_data/', methods=['GET'])
def get_dashbord():
    Account_Verificacoes = str(request.args['Account'])
    try:
        verificacoes = db.collection('accounts').document(Account_Verificacoes).collection('verificacoes').get()
        for v in verificacoes:
            itens = v.get('total_c') + v.get('total_nc') + v.get('total_na')
        conformes = db.collection('accounts').document(Account_Verificacoes).collection('conformes').get()
        nao_conformes = db.collection('accounts').document(Account_Verificacoes).collection('nao_conformes').get()
        nao_aplicavel = db.collection('accounts').document(Account_Verificacoes).collection('nao_aplicavel').get()
        planos_de_acao = db.collection('accounts').document(Account_Verificacoes).collection('planos_de_acao').get()
        
        dict_painel = {'conformes': len(conformes) / itens* 100, 'nao_conformes': len(nao_conformes) / itens * 100, 'planos_de_acao': len(planos_de_acao) / itens * 100, 'nao_aplicavel': len(nao_aplicavel) / itens * 100}
       
        return dict_painel

    except Exception as e:
        return 'Erro. Não foi possível acessar o painel dessa conta.\nMais detalhes: ' + str(e)

#####METODO PARA PEGAR TODAS AS VERIFICACOES############
@app.route('/api/verificacoes/get_data/', methods=['GET'])
def get_all_verificacoes():
    Account_Verificacoes = str(request.args['Account'])
    list_verificacoes = []
    list_nao_aplicavel_details = []
    list_conformes_details = []
    list_nao_conformes_details = []
    list_verificacoes = []
    #####ESTRUTURANDO TODAS AS VERIFICACOES DOS OS USUARIOS####################
    try:
        verificacoes_total = db.collection('accounts').document(Account_Verificacoes).collection('verificacoes').get()
        for v in verificacoes_total:
            conformes_verificacao = db.collection('accounts').document(Account_Verificacoes).collection(
                'verificacoes').document(v.id).collection('conformes').get()
            for c in conformes_verificacao:
                list_conformes_details.append(
                    {'uid_conforme': c.id, 'pergunta': c.get('pergunta'), 'images': c.get('images'),
                        'situacao': c.get('situacao'), 'comentario': c.get('comentario')})

            nao_conformes_verificacao = db.collection('accounts').document(Account_Verificacoes).collection(
                'verificacoes').document(v.id).collection('nao_conformes').get()
            for nc in nao_conformes_verificacao:
                list_nao_conformes_details.append(
                    {'uid_conforme': nc.id, 'pergunta': nc.get('pergunta'), 'images': nc.get('images'),
                        'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

            nao_aplicavel_verificacao = db.collection('accounts').document(Account_Verificacoes).collection(
                'verificacoes').document(v.id).collection('nao_aplicavel').get()
            for na in nao_aplicavel_verificacao:
                list_nao_aplicavel_details.append(
                    {'uid_conforme': na.id, 'pergunta': na.get('pergunta'), 'images': na.get('images'),
                        'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

            list_verificacoes.append({'aplicado_por': v.get('aplicado_por'), 'cargo': v.get('cargo'),
                                        'data_checklist': v.get('data_checklist'),
                                        'name_checklist': v.get('name_checklist'), 'total_c': v.get('total_c'),
                                        'total_nc': v.get('total_nc'), 'total_na': v.get('total_na'),
                                        'uid_checklist': v.get('uid_checklist'),
                                        'uid_verfication': v.get('uid_verfication'),
                                        'nao_aplicavel': list_nao_aplicavel_details,
                                        'pdf': v.get('pdf'),
                                        'nao_conformes': list_nao_conformes_details, 'conformes': list_conformes_details,
                                        })

        json_list = json.dumps(list_verificacoes)
        return json_list

    except Exception as e:
        return 'Erro. Não foi possível acessar as checklists dessa conta.\nMais detalhes: ' + str(e)

####METODO PARA PEGAR UMA VERIFICACAO############
@app.route('/api/verificacoes/get_data/verificacao/', methods=['GET'])
def get_verificacao():
    Account_Verificacoe = str(request.args['Account'])
    Account_Checklist = Account_Verificacoes = str(request.args['Account']).split('/')
    User_id = Account_Checklist[0]
    verificacao = Account_Checklist[1]
    dict_verificacao = {}
    list_nao_aplicavel_details = []
    list_conformes_details = []
    list_nao_conformes_details = []
    list_verificacoes = []
    #####ESTRUTURANDO TODAS AS VERIFICACOES DOS OS USUARIOS####################
    try:
        verificacoe_details = db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).get()
 
        conformes_verificacao = db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).collection('conformes').get()
        for c in conformes_verificacao:
            list_conformes_details.append(
                {'uid_conforme': c.id, 'pergunta': c.get('pergunta'), 'images': c.get('images'),
                    'situacao': c.get('situacao'), 'comentario': c.get('comentario')})

        nao_conformes_verificacao = db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).collection('nao_conformes').get()
        for nc in nao_conformes_verificacao:
            list_nao_conformes_details.append(
                {'uid_conforme': nc.id, 'pergunta': nc.get('pergunta'), 'images': nc.get('images'),
                    'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

        nao_aplicavel_verificacao = db.collection('accounts').document(User_id).collection('verificacoes').document(verificacao).collection('nao_aplicavel').get()
        for na in nao_aplicavel_verificacao:
            list_nao_aplicavel_details.append(
                {'uid_conforme': na.id, 'pergunta': na.get('pergunta'), 'images': na.get('images'),
                    'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

        dict_verificacao = {'aplicado_por': verificacoe_details.get('aplicado_por'), 'cargo': verificacoe_details.get('cargo'),
                                    'data_checklist': verificacoe_details.get('data_checklist'),
                                    'name_checklist': verificacoe_details.get('name_checklist'), 
                                    'total_c': verificacoe_details.get('total_c'),
                                    'total_nc': verificacoe_details.get('total_nc'), 
                                    'total_na': verificacoe_details.get('total_na'),
                                    'uid_checklist': verificacoe_details.get('uid_checklist'),
                                    'uid_verfication': verificacoe_details.get('uid_verfication'),
                                    'pdf': verificacoe_details.get('pdf'),
                                    'nao_aplicavel': list_nao_aplicavel_details,
                                    'nao_conformes': list_nao_conformes_details, 
                                    'conformes': list_conformes_details,
                                    }

        return dict_verificacao

    except Exception as e:
        return 'Erro. Não foi possível acessar as checklists dessa conta.\nMais detalhes: ' + str(e)

####METODO PARA PEGAR TODAS AS CHECKLISTS############
@app.route('/api/checklists/get_data/', methods=['GET'])
def get_all_checklists():
    Account_Checklists = str(request.args['Account'])
    dict_checklists = {}
    list_checklists = []
    list_perguntas = []
    #####ESTRUTURANDO OS DADOS DA CHECKLIST####################
    Checklists = db.collection('accounts').document(Account_Checklists).collection('checklists').get()
    try:
        for c in Checklists:
            perguntas_Checklists = db.collection('accounts').document(Account_Checklists).collection('checklists').document(c.id).collection('perguntas').get()
            for p in perguntas_Checklists:
                details_perguntas = db.collection('accounts').document(Account_Checklists).collection('checklists').document(c.id).collection('perguntas').document(p.id).get()
                list_perguntas.append({'uid_pergunta': p.id,'pergunta': details_perguntas.get('pergunta'),
                    'observacao': details_perguntas.get('observacao'),'images': details_perguntas.get('images'),
                })
            dict_checklists = {'uid_checklist': c.id, 'CategoriasID': c.get('CategoriasID'), 
            'deleted_categoria': c.get('deleted_categoria'), 'descricao': c.get('descricao'), 
            'observacao': c.get('observacao'), 'title': c.get('title'), 'itens': len(perguntas_Checklists),'perguntas': list_perguntas,}
            list_checklists.append(dict_checklists)
            list_perguntas = []
        json_list = json.dumps(list_checklists)
        return json_list
    except Exception as e:
        return 'Erro. Não foi possível acessar as checklists dessa conta.\nMais detalhes: ' + str(e)

####METODO PARA PEGAR UMA CHECKLIST############
@app.route('/api/checklists/get_data/checklist/', methods=['GET'])
def get_checklist():
    Account_Checklist = str(request.args['Account'])
    Account_Checklist = Account_Checklist.split('/')
    list_perguntas = []
    User_id = Account_Checklist[0]
    checklist = Account_Checklist[1]
    
    #####ESTRUTURANDO OS DADOS DA CHECKLIST####################
    Checklist_Firebase = db.collection('accounts').document(User_id).collection('checklists').document(checklist).get()
    perguntas_Checklists = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').get()
    try:
        for p in perguntas_Checklists:
            details_perguntas = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').document(p.id).get()
            list_perguntas.append({'uid_pergunta': p.id,'pergunta': details_perguntas.get('pergunta'),
                'observacao': details_perguntas.get('observacao'),'images': details_perguntas.get('images'),
            })
        dict_checklists = {'uid_checklist': Checklist_Firebase.id, 'CategoriasID': Checklist_Firebase.get('CategoriasID'), 
        'deleted_categoria': Checklist_Firebase.get('deleted_categoria'), 'descricao': Checklist_Firebase.get('descricao'), 
        'observacao': Checklist_Firebase.get('observacao'), 'title': Checklist_Firebase.get('title'), 'itens': len(perguntas_Checklists), 'perguntas': list_perguntas,}
        return dict_checklists
    except Exception as e:
        return 'Erro. Não foi possível acessar as checklists dessa conta.\nMais detalhes: ' + str(e)

####METODO PARA PEGAR UMA PERGUNTA DE UMA CHECKLIST############
@app.route('/api/checklists/get_data/perguntas/get/', methods=['GET'])
def get_pergunta():
    Account_Checklist = str(request.args['Account'])
    Account_Checklist = Account_Checklist.split('/')
    User_id = Account_Checklist[0]
    checklist = Account_Checklist[1]
    pergunta = Account_Checklist[2]
    dict_pergunta = {}

    pergunta = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').document(pergunta).get()
    try:
        dict_pergunta = {'uid_pergunta': pergunta.id,'pergunta': pergunta.get('pergunta'),
                'observacao': pergunta.get('observacao'),'images': pergunta.get('images'),
            }
        return dict_pergunta
    except Exception as e:
        return 'Erro. Não foi possível acessar as perguntas dessa Checklist.\nMais detalhes: ' + str(e)

####METODO PARA PEGAR TODAS PERGUNTAS DE UMA CHECKLIST############
@app.route('/api/checklists/get_data/perguntas/', methods=['GET'])
def get_all_perguntas():
    Account_Checklist = str(request.args['Account'])
    Account_Checklist = Account_Checklist.split('/')
    User_id = Account_Checklist[0]
    checklist = Account_Checklist[1]
    list_perguntas = []

    perguntas_Checklists = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').get()
    try:
        for p in perguntas_Checklists:
            details_perguntas = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').document(p.id).get()
            list_perguntas.append({'uid_pergunta': p.id,'pergunta': details_perguntas.get('pergunta'),
                'observacao': details_perguntas.get('observacao'),'images': details_perguntas.get('images'),
            })
        json_list = json.dumps(list_perguntas)
        return json_list
    except Exception as e:
        return 'Erro. Não foi possível acessar as perguntas dessa Checklist.\nMais detalhes: ' + str(e)

####METODO PARA LOGAR UM USUARIO DO FIREBASE############
@app.route('/api/accounts/get_data/', methods=['GET'])
def get_data_accounts():
    Account = str(request.args['Account'])
    Account = Account.split('/')

    email = Account[0]
    password = Account[1]
    try:
        user = auth.get_user_by_email(email)
        account = db.collection('accounts').document(user.uid).get()
        if (account.get('password') == password):
            dict_account_auth = {'Id': user.uid, 'Email': email, 'UserName': account.get('name')}
            response = jsonify(dict_account_auth)
            return response, 200
        else:
            response = jsonify({'message':'Usuário ou senha incorretos.'})
            return response, 401
    except:
        response = jsonify({'message':'Usuário ou senha incorretos.'})
        return response, 401


if __name__ == '__main__':
    app.run(debug=True)
