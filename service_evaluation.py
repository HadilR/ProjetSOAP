from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json

class ServiceEvaluationPropriete(ServiceBase):

    @rpc(Unicode, _returns=Unicode)
    def evaluer_propriete(ctx, client_info_file):
        result = evaluer_propriete(client_info_file)
        return result

def evaluer_propriete(client_info_file):
    try:
        with open(client_info_file, 'r', encoding='utf-8') as json_file:
            client_data = json.load(json_file)
    except FileNotFoundError:
        return "Fichier client_info.json introuvable"

    for client_id, client_info in client_data.items():
        # Ici, vous devrez adapter cette partie en fonction de la structure de votre fichier JSON
        indicateur_gaz = client_info.get("indicateur gaz et electricite", "N/A")

        if indicateur_gaz in {'A', 'B', 'C'}:
            client_info["evaluation propriete"] = "Bien evalue"
        else:
            client_info["evaluation propriete"] = "Mal evalue"


    # Enregistrez les résultats dans le fichier client_info.json
    with open(client_info_file, 'w', encoding='utf-8') as json_file:
        json.dump(client_data, json_file, indent=4)

    return "Évaluation de propriété terminée pour le dernier client ajouté"

# Crée une application Spyne pour le service d'évaluation de propriété
evaluation_propriete_application = Application([ServiceEvaluationPropriete],
                                              'spyne.examples.evaluation_propriete.soap',
                                              in_protocol=Soap11(validator='lxml'),
                                              out_protocol=Soap11())

# Crée une application WSGI pour servir le service d'évaluation de propriété
evaluation_propriete_wsgi_application = WsgiApplication(evaluation_propriete_application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    evaluation_propriete_server = make_server('127.0.0.1', 8002, evaluation_propriete_wsgi_application)
    print("Service d'évaluation de propriété SOAP en cours d'exécution sur http://127.0.0.1:8002")
    evaluation_propriete_server.serve_forever()
