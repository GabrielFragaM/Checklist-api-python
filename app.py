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


@app.route('/api/check/get_data/', methods=['GET', 'POST'])
def get_data_checklists():
    dict_json = {}
    list_checklists = []
    list_verificacoes = []
    list_accounts = []
    list_perguntas = []
    list_checklists_verificacoes = []
    list_nao_aplicavel = []
    list_conformes = []
    list_nao_conformes = []
    list_nao_aplicavel_details = []
    list_conformes_details = []
    list_nao_conformes_details = []
    list_nao_aplicavel_details_checklist = []
    list_conformes_details_checklist = []
    list_nao_conformes_details_checklist = []
    accounts = db.collection('accounts').get()

    for account in accounts:
        list_accounts.append({'account_id': account.id})

    sum = 0
    for account in list_accounts:
        dict_json['db_firebase'] = list_accounts

        #####ESTRUTURANDO TODAS AS VERIFICACOES DOS OS USUARIOS####################
        verificacoes_total = db.collection('accounts').document(account['account_id']).collection('verificacoes').get()
        for v in verificacoes_total:
            conformes_verificacao = db.collection('accounts').document(account['account_id']).collection(
                'verificacoes').document(v.id).collection('conformes').get()
            for c in conformes_verificacao:
                list_conformes_details.append(
                    {'uid_conforme': c.id, 'pergunta': c.get('pergunta'), 'images': c.get('images'),
                     'situacao': c.get('situacao'), 'comentario': c.get('comentario')})

            nao_conformes_verificacao = db.collection('accounts').document(account['account_id']).collection(
                'verificacoes').document(v.id).collection('nao_conformes').get()
            for nc in nao_conformes_verificacao:
                list_nao_conformes_details.append(
                    {'uid_conforme': nc.id, 'pergunta': nc.get('pergunta'), 'images': nc.get('images'),
                     'comentario': c.get('comentario'), 'situacao': c.get('situacao'), })

            nao_aplicavel_verificacao = db.collection('accounts').document(account['account_id']).collection(
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
                                      'nao_conformes': list_nao_conformes_details, 'conformes': list_conformes_details,
                                      })

        #####ESTRUTURANDO OS DADOS DOS CONFORMES TOTAL NAO CONFORMES NAO APLICAVEL TOTAIS DA CONTA####################
        conformes = db.collection('accounts').document(account['account_id']).collection('conformes').get()
        nao_conformes = db.collection('accounts').document(account['account_id']).collection('nao_conformes').get()
        nao_aplicavel = db.collection('accounts').document(account['account_id']).collection('nao_aplicavel').get()
        for nc in nao_conformes:
            list_nao_conformes.append(nc.id)
        for na in nao_aplicavel:
            list_nao_aplicavel.append(na.id)
        for c in conformes:
            list_conformes.append(c.id)

        #####ESTRUTURANDO OS DADOS DA CHECKLIST####################
        checklists_accounts = db.collection('accounts').document(account['account_id']).collection('checklists').get()
        for checklist in checklists_accounts:
            checklists_perguntas = db.collection('accounts').document(account['account_id']).collection(
                'checklists').document(checklist.id).collection('perguntas').get()
            checklists_verificacoes = db.collection('accounts').document(account['account_id']).collection(
                'checklists').document(checklist.id).collection('verificacoes').get()
            for vc in checklists_verificacoes:
                conformes_verificacao = db.collection('accounts').document(account['account_id']).collection(
                    'verificacoes').document(vc.id).collection('conformes').get()
                for c in conformes_verificacao:
                    list_conformes_details_checklist.append(
                        {'uid_conforme': c.id, 'situacao': c.get('situacao'), 'pergunta': c.get('pergunta'),
                         'images': c.get('images'), 'comentario': c.get('comentario')})

                nao_conformes_verificacao = db.collection('accounts').document(account['account_id']).collection(
                    'verificacoes').document(vc.id).collection('nao_conformes').get()
                for nc in nao_conformes_verificacao:
                    list_nao_conformes_details_checklist.append(
                        {'uid_conforme': nc.id, 'situacao': nc.get('situacao'), 'pergunta': nc.get('pergunta'),
                         'images': nc.get('images'), 'comentario': nc.get('comentario')})

                nao_aplicavel_verificacao = db.collection('accounts').document(account['account_id']).collection(
                    'verificacoes').document(vc.id).collection('nao_aplicavel').get()
                for na in nao_aplicavel_verificacao:
                    list_nao_aplicavel_details_checklist.append(
                        {'uid_conforme': na.id, 'situacao': na.get('situacao'), 'pergunta': na.get('pergunta'),
                         'images': na.get('images'), 'comentario': na.get('comentario')})

                list_checklists_verificacoes.append({'aplicado_por': vc.get('aplicado_por'), 'cargo': vc.get('cargo'),
                                                     'data_checklist': vc.get('data_checklist'),
                                                     'name_checklist': vc.get('name_checklist'),
                                                     'total_c': vc.get('total_c'), 'total_nc': vc.get('total_nc'),
                                                     'total_na': vc.get('total_na'),
                                                     'uid_checklist': vc.get('uid_checklist'),
                                                     'uid_verfication': vc.get('uid_verfication'),
                                                     'nao_aplicavel': list_nao_aplicavel_details_checklist,
                                                     'nao_conformes': list_nao_conformes_details_checklist,
                                                     'conformes': list_conformes_details_checklist,
                                                     })

            for pergunta_details in checklists_perguntas:
                pergunta = db.collection('accounts').document(account['account_id']).collection('checklists').document(
                    checklist.id).collection('perguntas').document(pergunta_details.id).get()
                list_perguntas.append({'pergunta': pergunta.get('pergunta'), 'observacao': pergunta.get('observacao'),
                                       'images': pergunta.get('images')})
            list_checklists.append({'checklist_id': checklist.id, 'CategoriasID': checklist.get('CategoriasID'),
                                    'title': checklist.get('title')
                                       , 'observacao': checklist.get('observacao'),
                                    'deleted_categoria': checklist.get('deleted_categoria'),
                                    'descricao': checklist.get('descricao'),
                                    'pergunta': list_perguntas, 'verificacoes': list_checklists_verificacoes
                                    })

        #####ADICIONANDO OS TODOS OS DADOS DO BANCO FIREBASE EM JSON####################
        dict_json['db_firebase'][sum]['checklists'] = list_checklists
        dict_json['db_firebase'][sum]['conformes'] = list_conformes
        dict_json['db_firebase'][sum]['nao_aplicavel'] = list_nao_aplicavel
        dict_json['db_firebase'][sum]['nao_conformes'] = list_nao_conformes
        dict_json['db_firebase'][sum]['verificacoes'] = list_verificacoes

        list_checklists = []
        list_perguntas = []
        list_verificacoes = []
        list_nao_conformes = []
        list_conformes = []
        list_nao_aplicavel = []
        list_conformes_details = []
        list_nao_aplicavel_details = []
        list_nao_conformes_details = []
        list_checklists_verificacoes = []

        sum = sum + 1

    return jsonify(dict_json)

####METODO PARA PEGAR TODAS AS CHECKLISTS DO USUARIO DO FIREBASE############
@app.route('/api/checklists/get_data/', methods=['GET', 'POST'])
def get_all_checklists():
    Account_Checklists = str(request.args['Account'])
    
    dict_checklists = {}
    list_checklists = []
    #####ESTRUTURANDO OS DADOS DA CHECKLIST####################
    Checklists = db.collection('accounts').document(Account_Checklists).collection('checklists').get()

    try:
        for c in Checklists:
            perguntas_Checklists = db.collection('accounts').document(Account_Checklists).collection('checklists').document(c.id).collection('perguntas').get()

            dict_checklists = {'uid_checklist': c.id, 'CategoriasID': c.get('CategoriasID'), 
            'deleted_categoria': c.get('deleted_categoria'), 'descricao': c.get('descricao'), 
            'observacao': c.get('observacao'), 'title': c.get('title'), 'itens': len(perguntas_Checklists),}
            list_checklists.append(dict_checklists)
        json_list = json.dumps(list_checklists)
        return json_list
    except Exception as e:
        return 'Erro. Não foi possível acessar as checklists dessa conta.\nMais detalhes: ' + str(e)

####METODO PARA PEGAR UMA CHECKLIST DO USUARIO DO FIREBASE############
@app.route('/api/checklists/get_data/checklist/', methods=['GET', 'POST'])
def get_checklist():
    Account_Checklist = str(request.args['Account'])
    Account_Checklist = Account_Checklist.split('-')

    User_id = Account_Checklist[0]
    checklist = Account_Checklist[1]
    list_perguntas = []
    
    #####ESTRUTURANDO OS DADOS DA CHECKLIST####################
    Checklist_Firebase = db.collection('accounts').document(User_id).collection('checklists').document(checklist).get()
    perguntas_Checklists = db.collection('accounts').document(User_id).collection('checklists').document(checklist).collection('perguntas').get()

    try:
        for p in perguntas_Checklists:
            details_perguntas = db.collection('accounts').document(User_id).collection('checklists').document(Checklist_Firebase.id).collection('perguntas').document(p.id).get()
            list_perguntas.append({'uid_pergunta': details_perguntas.get('pergunta'),
                'observacao': details_perguntas.get('observacao'),'images': details_perguntas.get('images'),
            })
        dict_checklists = {'uid_checklist': Checklist_Firebase.id, 'CategoriasID': Checklist_Firebase.get('CategoriasID'), 
        'deleted_categoria': Checklist_Firebase.get('deleted_categoria'), 'descricao': Checklist_Firebase.get('descricao'), 
        'observacao': Checklist_Firebase.get('observacao'), 'title': Checklist_Firebase.get('title'), 'itens': len(perguntas_Checklists), 'perguntas': list_perguntas}
        
        return dict_checklists
    except Exception as e:
        return 'Erro. Não foi possível acessar as checklists dessa conta.\nMais detalhes: ' + str(e)

####METODO PARA LOGAR UM USUARIO DO FIREBASE############
@app.route('/api/accounts/get_data/', methods=['GET', 'POST'])
def get_data_accounts():
    Account = str(request.args['Account'])
    Account = Account.split('-')

    email = Account[0]
    password = Account[1]
    try:
        user = auth.get_user_by_email(email)
        account = db.collection('accounts').document(user.uid).get()
        if (account.get('password') == password):
            dict_account_auth = {'Id': user.uid, 'Email': email, 'UserName': account.get('name')}
            return dict_account_auth
        else:
            return 'Usuário ou senha incorretos.'
    except:
        return 'Usuário ou senha incorretos.'


if __name__ == '__main__':
    app.run(debug=True)
