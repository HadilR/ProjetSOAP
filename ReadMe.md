README

Ce projet consiste en une série de services web SOAP interconnectés visant à automatiser le processus de scoring de crédit. Le projet est divisé en plusieurs composants, chacun ayant une fonction spécifique.

Composants du Projet
	
	1. service_extraction.py
Ce service permet l'extraction de données client à partir d'un fichier texte demande_client.txt.
Il extrait les données, les stocke dans un fichier JSON client_info.json, et attribue un identifiant unique à chaque ensemble de données client.
Pour l'utiliser, exécutez le service et utilisez un client SOAP pour appeler la méthode extract_data.
	
	2. service_solvabilite.py
Ce service évalue la solvabilité du client en fonction des données contenues dans client_info.json.
Il attribue la valeur "Solvable" ou "Non Solvable" pour chaque client en fonction de certains critères.
Pour l'utiliser, exécutez le service et utilisez un client SOAP pour appeler la méthode check_solvency.
	
	3. service_evaluation.py
Ce service évalue la propriété des clients en fonction des données contenues dans client_info.json.
Il attribue la valeur "Bien évalué" ou "Mal évalué" pour chaque client en fonction de certains critères.
Pour l'utiliser, exécutez le service et utilisez un client SOAP pour appeler la méthode evaluer_propriete.

	4. credit_scoring.py
Ce service calcule le score de crédit de chaque client en fonction des données de solvabilité et d'évaluation de propriété.
Il utilise une formule spécifique pour attribuer un score de crédit à chaque client.
Les scores de crédit sont stockés dans client_info.json.
Pour l'utiliser, exécutez le service et utilisez un client SOAP pour appeler la méthode calculate_credit_score.

	5. service_approbation.py
Ce service prend des décisions d'approbation en fonction des scores de crédit, de la solvabilité et de l'évaluation de propriété.
Il attribue une décision "Positif" ou "Négatif" pour chaque client en fonction de certains critères.
Les décisions d'approbation sont stockées dans client_info.json.
Pour l'utiliser, exécutez le service et utilisez un client SOAP pour appeler la méthode prendre_decision.
	
	6. service_composite.py
Ce composant permet à un utilisateur d'entrer des informations client via une interface utilisateur Tkinter.
Il appelle ensuite les autres services de manière séquentielle pour effectuer le scoring de crédit complet et affiche la décision d'approbation.

Prérequis

Avant de lancer les services, veuillez suivre ces étapes :
	1- installer les bibliothèques Spyne et Soap11
	2- Afin de lancer les interfaces graphiques (ce n'est pas obligatoire parce que on a un fichier texte demande_client.txt où il'y a une demande pré-remplie), il faut :
		a- Installez le serveur VcXsrv pour activer les interfaces graphiques.
		b- Dans le terminal, saisissez la commande suivante pour définir la variable d'affichage (DISPLAY) : export DISPLAY=IP_de_votre_système:0.0


Utilisation

Une fois les prérequis installés et configurés, suivez ces étapes pour exécuter l'application :

	1- Lancez tous les services en exécutant les commandes suivantes dans des terminaux séparés :
		python3 service_extraction.py
		python3 credit_scoring.py
		python3 service_solvabilite.py
		python3 service_evaluation.py
		python3 service_approbation.py
	2- Enfin, exécutez le service composite en utilisant la commande suivante :
		python3 service_composite.py


Cela lancera l'interface utilisateur et l'interface résultat qui vous permettra d'entrer des informations client et d'obtenir la décision d'approbation finale si vous avez fait le choix d'exécution des interfaces.
Sinon vous pouvez voir les changement dans le fichier client_info.json .
Assurez-vous que les services s'exécutent sur les ports et les URL spécifiés dans les fichiers respectifs.

Note : Les composants du projet sont conçus pour être utilisés localement, sur la même machine. Pour une utilisation en production, des modifications sont nécessaires pour rendre les services accessibles via le réseau.

