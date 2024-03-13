from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json

class ServiceDecisionApprobation(ServiceBase):

    @rpc(Unicode, _returns=Unicode)
    def prendre_decision(ctx, client_info_file):
        results = prendre_decision(client_info_file)
        return results

def prendre_decision(client_info_file):
    try:
        with open(client_info_file, 'r', encoding='utf-8') as json_file:
            client_data = json.load(json_file)
    except FileNotFoundError:
        return "Fichier client_info.json introuvable"


    for client_id, client_info in client_data.items():
        solvabilite = client_info.get("Solvabilite", "N/A")
        evaluation_propriete = client_info.get("evaluation propriete", "N/A")

        if solvabilite == "Solvable" and evaluation_propriete == "Bien evalue":
            client_info["decision_approbation"] = "Positif"
        else:
            client_info["decision_approbation"] = "Negatif"


    # Enregistrez les résultats dans le fichier client_info.json
    with open(client_info_file, 'w', encoding='utf-8') as json_file:
        json.dump(client_data, json_file, indent=4)

    return "Décisions d'approbation ajoutées au dernier client ajouté"

# Crée une application Spyne pour le service de décision d'approbation
decision_approbation_application = Application([ServiceDecisionApprobation],
                                              'spyne.examples.decision_approbation.soap',
                                              in_protocol=Soap11(validator='lxml'),
                                              out_protocol=Soap11())

# Crée une application WSGI pour servir le service de décision d'approbation
decision_approbation_wsgi_application = WsgiApplication(decision_approbation_application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    decision_approbation_server = make_server('127.0.0.1', 5003, decision_approbation_wsgi_application)
    print("Service de décision d'approbation SOAP en cours d'exécution sur http://127.0.0.1:5003")
    decision_approbation_server.serve_forever()
