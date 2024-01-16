from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json

#Seuil pour évaluer la solvabilité
seuil = 1.5

class ServiceSolvabilite(ServiceBase):

    @rpc(Unicode, _returns=Unicode)
    def check_solvency(ctx, client_info_file):
        result = check_solvency(client_info_file)
        return result

def check_solvency(client_info_file):
    try:
        with open(client_info_file, 'r', encoding='utf-8') as json_file:
            client_data = json.load(json_file)
    except FileNotFoundError:
        return "Fichier client_info.json introuvable"

    for client_id, client_info in client_data.items():
        if 'credit_score' in client_info:
            credit_score = client_info['credit_score']
            if credit_score > seuil:
                client_info["Solvabilite"] = "Solvable"
            else:
                client_info["Solvabilite"] = "Non Solvable"

    with open(client_info_file, 'w', encoding='utf-8') as json_file:
        json.dump(client_data, json_file, indent=4)

    return "Solvabilite verifiée pour le dernier client ajouté"

# Create a Spyne application for the solvability service
solvabilite_application = Application([ServiceSolvabilite],
                                      'spyne.examples.solvabilite.soap',
                                      in_protocol=Soap11(validator='lxml'),
                                      out_protocol=Soap11())

# Create a WSGI application to serve the solvability service
solvabilite_wsgi_application = WsgiApplication(solvabilite_application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    solvabilite_server = make_server('127.0.0.1', 8001, solvabilite_wsgi_application)
    print("Service de solvabilite SOAP en cours d'exécution sur http://127.0.0.1:8001")
    solvabilite_server.serve_forever()
