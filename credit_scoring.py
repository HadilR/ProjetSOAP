from spyne import Application, rpc, ServiceBase, Unicode, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json

class CreditScoringService(ServiceBase):

    @rpc(Unicode, _returns=Float)
    def calculate_credit_score(ctx, client_info_file):
        calculate_score(client_info_file, 'credit_data.json')
        return 0.0

def calculate_score(client_info_file, client_data_file):
    credit_data = load_credit_data(client_data_file)  # Charger les données de crédit
    client_info = load_info_file(client_info_file)

    for client_id, client_data in credit_data.items():
        if 'requests' in client_data and 'delays' in client_data and 'bankruptcies' in client_data:
            credit_score = 0.5 * client_data['requests'] - 0.2 * client_data['delays'] + 0.3 * client_data['bankruptcies']
            if client_id in client_info:
                client_info[client_id]["credit_score"] = credit_score
                
    save_credit_data(client_info_file, client_info)

def load_info_file(client_info_file):
    try:
        with open(client_info_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        # Gérer l'erreur de fichier non trouvé
        return {}

def load_credit_data(client_data_file):
    try:
        with open(client_data_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        # Gérer l'erreur de fichier non trouvé
        return {}
    
def save_credit_data(client_info_file, data):
    with open(client_info_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)


# Crée une application Spyne pour le service de scoring de crédit
credit_scoring_application = Application([CreditScoringService],
                                         'spyne.examples.credit_scoring.soap',
                                         in_protocol=Soap11(validator='lxml'),
                                         out_protocol=Soap11())

# Crée une application WSGI pour servir le service de scoring de crédit
credit_scoring_wsgi_application = WsgiApplication(credit_scoring_application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    credit_scoring_server = make_server('127.0.0.1', 5005, credit_scoring_wsgi_application)
    print("Service de scoring de crédit en cours d'exécution sur http://127.0.0.1:5005")
    credit_scoring_server.serve_forever()
