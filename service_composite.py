from suds.client import Client
import tkinter as tk
import json

#######################################################################
#interface pour la saisie de la demande : Si vous voulez l'activer, il faut suivre les étapes dans le fichier ReadMe
#######################################################################

def save_text():
    user_text = text_box.get("1.0", "end-1c")
    with open('demande_client.txt', 'w') as f:
        f.write(user_text)
    root.destroy()

# Créez une fenêtre Tkinter pour l'interface utilisateur
root = tk.Tk()
root.title("Entrer un texte")
root.geometry("400x300")

# Créez un champ de texte pour que l'utilisateur puisse entrer du texte
text_box = tk.Text(root)
text_box.pack(fill="both", expand=True, padx=10, pady=10)

# Ajoutez un bouton pour sauvegarder le texte
save_button = tk.Button(root, text="Enregistrer", command=save_text)
save_button.pack(pady=5)

root.mainloop()


#############################################################
########Appel de tous les services pour traiter la demande
############################################################

# Création d'un client SOAP pour le service d'extraction
extraction_service_client = Client('http://localhost:8000/?wsdl')

# Appel de la méthode du service d'extraction
extraction_result = extraction_service_client.service.extract_data()

# Affichage du résultat de l'extraction
print("Résultat du service d'extraction:")
print(extraction_result)

##########################

# Fichier d'enregistrement des données
file_path = 'client_info.json'


# Creation de client SOAP pour le service credit scoring
credit_scoring_service_client = Client('http://localhost:8005/?wsdl')

# Appel de la méthode du service credit scoring
credit_score_result = credit_scoring_service_client.service.calculate_credit_score(file_path)  # Replace client_id with the appropriate client identifier

# affichage de resultat 
print("Credit Scoring attribué au dernier client ajouté")

##############################

# Creation de client SOAP pour le service solvabilite
solvabilite_service_client = Client('http://localhost:8001/?wsdl')

# Appel de la méthode du service solvabilite
solvabilite_result = solvabilite_service_client.service.check_solvency(file_path)

# affichage du resultat
print("Résultat du service de solvabilité:")
print(solvabilite_result)

##########################

# Création d'un client SOAP pour le service d'évaluation de propriété
evaluation_propriete_service_client = Client('http://localhost:8002/?wsdl')

# Appel de la méthode du service d'évaluation de propriété avec le chemin du fichier JSON
evaluation_result = evaluation_propriete_service_client.service.evaluer_propriete(file_path)

# Affichage du résultat de l'évaluation de propriété
print("Résultat de l'évaluation de propriété :")
print(evaluation_result)

##################################

# Création d'un client SOAP pour le service de décision d'approbation
decision_approbation_service_client = Client('http://localhost:8003/?wsdl')

# Appel de la méthode du service d'évaluation de propriété avec le chemin du fichier JSON
approbation_result = decision_approbation_service_client.service.prendre_decision(file_path)

# Affichage du résultat de l'évaluation de propriété
print("Résultat de décision d'approbation :")
print(approbation_result)


################################################################################
#interface pour l'affichage du résultat de traitement de la demande : Si vous voulez l'activer, il faut suivre les étapes dans le fichier ReadMe
################################################################################

# Charger le fichier JSON
with open('client_info.json', 'r') as f:
    data = json.load(f)

# Récupérer la dernière méthode dans le fichier JSON
last_method = None
for key, value in data.items():
    last_method = key

if last_method:
    # Ajouter la décision d'approbation à la dernière méthode
    approbation_result_msg = data[last_method]["decision_approbation"]

    # Enregistrer les modifications dans le fichier JSON
    with open('client_info.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Créer une fenêtre Tkinter pour l'interface utilisateur de la décision d'approbation
    root = tk.Tk()
    root.title("Décision d'approbation : ")
    root.geometry("400x200")

    # Ajouter une étiquette pour afficher la décision d'approbation de la dernière méthode
    label = tk.Label(root, text=f"Décision d'approbation de votre demande : {approbation_result_msg}")
    label.pack(pady=20)

    root.mainloop()
else:
    print("Aucune méthode trouvée dans le fichier JSON.")
    
