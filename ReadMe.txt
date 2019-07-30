
---------------------------- SCRIPTS PYTHON POUR QUELQUES ANALYSES SUR LES POSTES ACHEVES -----------------------

1. Executer le fichier Create_GDB_FC_Anomalies.py pour creer la .gdb et les features classes des anomalies (PL, Supports, Reseaux)

2. Executer les autres scripts en fonctions de la feature class que l'on desire examiner
	
	* Anomalies_Fraudes.py : Extrait les anomalies de la couche PL

	* Supports_defectueux.py : Extrait les supports dont l'etat est soit Cassé, Pourri, Pourri-Operationnel et Tombé

	* Reseaux_Branchements_Long.py : Extrait les Reseaux et branchements longs entre deux entités.

				NB: Les longueurs maximales sont saisies par l'utilisateur