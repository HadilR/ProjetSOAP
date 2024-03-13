from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json

class ServiceExtraction(ServiceBase):

    @rpc(_returns=Unicode)
    def extract_data(ctx):
        # Lecture du fichier client_info.txt
        with open('demande_client.txt', 'r', encoding='utf-8') as f:
            new_data_content = f.read()

        # Charger les données existantes depuis le fichier JSON (s'il existe)
        try:
            with open('client_info.json', 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            existing_data = {}

        # Extraire les données du nouveau texte
        new_data = {}
        lines = new_data_content.split("\n")
        for line in lines:
            if ':' in line:
                key, value = line.split(":", 1)
                new_data[key.strip()] = value.strip()
        
        # Obtenir le prochain identifiant unique
        unique_id = len(existing_data)

        # Stocker les nouvelles données sous l'identifiant unique
        existing_data[unique_id] = new_data

        # Convertir les données fusionnées en format JSON
        json_data = json.dumps(existing_data, indent=4)

        # Écrire le JSON dans le fichier
        with open('client_info.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)

        return f"Nouvelles données extraites et ajoutées à client_info.json avec l'ID {unique_id}"

# Crée une application Spyne
application = Application([ServiceExtraction],
                          'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Crée une application WSGI pour servir le service d'extraction
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 5000, wsgi_application)
    print("Service d'extraction SOAP en cours d'exécution sur http://127.0.0.1:5000")
    server.serve_forever()
