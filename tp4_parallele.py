#********************************************************************************
# Laila Zouaki
# TP4
#********************************************************************************


import json
import os, os.path
import multiprocessing
import time

# Comparé à la version simple, le temps d'exécution est 2 à 3 fois plus rapide.

#********************************************************************************
# 0. Ouverture de tous les fichiers
#********************************************************************************

def ouvrir_fichier(numero_dossier, nom_fichier):
	with open("data/{}/commune_{}".format(numero_dossier, nom_fichier), 'r') as json_data:
		data = json.load(json_data)

	return data["fields"]

def ouvrir_fichiers_par_dossier(numero_dossier):
	nombre_fichier = len([name for name in os.listdir("data/{}".format(numero_dossier)) if os.path.isfile(os.path.join("data/{}".format(numero_dossier), name))])
	if numero_dossier == "00":
		fichiers = [ouvrir_fichier(numero_dossier, "0000{}".format(i)) for i in range(10)]
		fichiers += [ouvrir_fichier(numero_dossier, "000{}".format(i)) for i in range(10, 100)]
		fichiers += [ouvrir_fichier(numero_dossier, "00{}".format(i)) for i in range(100, 1000)]

	elif int(numero_dossier) < 10:
		fichiers = [ouvrir_fichier(numero_dossier, "0{}".format(i)) for i in range(int(numero_dossier)*1000, int(numero_dossier)*1000+nombre_fichier)]

	else:
		fichiers = [ouvrir_fichier(numero_dossier, "{}".format(i)) for i in range(int(numero_dossier)*1000, int(numero_dossier)*1000+nombre_fichier)]

	return fichiers


# Champs importants : 
# Région "nom_region"
# Département "nom_dept"
# Statut "statut"
# Nombre d'habitants "population"

# 1. Combien existe-t-il de statuts de communes?
# 2. Pour chaque statut, combien de communes ont ce statut?
# 3. Pour chaque départemnt, quel est le nombre d'habitants?
# 4. Pour chaque région, quel est le nombre d'habitants?
# 5. Quel est le nombre moyen de communes par département?
# 6. Quel est le nombre moyen de départements par région?
# 7. Quel est le nombre moyen de communes par région?


#********************************************************************************
# Initialisation des listes 
#********************************************************************************

def initialiser_donnees(fichiers):
	statuts = []
	departements = []
	regions = []
	for numero_dossier, dossier in enumerate(fichiers):
		for numero_commune, commune in enumerate(fichiers[numero_dossier]):
			if fichiers[numero_dossier][numero_commune]["statut"] not in statuts:
				statuts.append(fichiers[numero_dossier][numero_commune]["statut"])

			if fichiers[numero_dossier][numero_commune]["nom_dept"] not in departements:
				departements.append(fichiers[numero_dossier][numero_commune]["nom_dept"])

			if fichiers[numero_dossier][numero_commune]["nom_region"] not in regions:
				regions.append(fichiers[numero_dossier][numero_commune]["nom_region"])

	return statuts, departements, regions


# Chaque fonction renvoie les valeurs attendues et contient un print en commentaire qui présente les résultats plus clairement s

#********************************************************************************
# 1. Combien existe-t-il de statuts de communes?
#********************************************************************************

def nombre_statuts(statuts):
	#print("Il existe {} types de statuts".format(len(statuts)))
	return len(statuts)


#********************************************************************************
# 2. Pour chaque statut, combien de communes ont ce statut?
#********************************************************************************

def commune_par_statut(fichiers, statuts):
	commune_par_statut = [0 for i in range(len(statuts))]

	for indice, statut in enumerate(statuts):	
		for numero_dossier, dossier in enumerate(fichiers):
			for numero_commune, commune in enumerate(fichiers[numero_dossier]):
				if fichiers[numero_dossier][numero_commune]["statut"] == statut:
					commune_par_statut[indice] += 1

	# for indice, statut in enumerate(statuts):
	 	#print("Il y a {} communes pour le statut {}".format(commune_par_statut[indice], statut))

	return commune_par_statut


#********************************************************************************
# 3. Pour chaque départemnt, quel est le nombre d'habitants?
#********************************************************************************

def population_par_departement(fichiers, departements):
	population_par_departement = [0 for i in range(len(departements))]

	for indice, departement in enumerate(departements):
		for numero_dossier, dossier in enumerate(fichiers):
			for numero_commune, commune in enumerate(fichiers[numero_dossier]):
				if fichiers[numero_dossier][numero_commune]["nom_dept"] == departement:
					population_par_departement[indice] += round(fichiers[numero_dossier][numero_commune]["population"], 2)

	for indice, departement in enumerate(departements):
		#print("Il y a {} mille habitants pour le département {}".format(round(population_par_departement[indice],2), departement))
		population_par_departement[indice] = round(population_par_departement[indice], 2)

	return population_par_departement


#********************************************************************************
# 4. Pour chaque région, quel est le nombre d'habitants?
#********************************************************************************

def population_par_region(fichiers, regions):
	population_par_region = [0 for i in range(len(regions))]

	for indice, region in enumerate(regions):
		for numero_dossier, dossier in enumerate(fichiers):
			for numero_commune, commune in enumerate(fichiers[numero_dossier]):
				if fichiers[numero_dossier][numero_commune]["nom_region"] == region:
					population_par_region[indice] += fichiers[numero_dossier][numero_commune]["population"]


	for indice, region in enumerate(regions):
		#print("Il y a {} mille habitants pour la région {}".format(round(population_par_region[indice], 2), region))
		population_par_region[indice] = round(population_par_region[indice], 2)

	return population_par_region


#********************************************************************************
# 5. Quel est le nombre moyen de communes par département?
#********************************************************************************

def moyenne_commune_par_departement(fichiers, departements):
	commune_par_departement  = [0 for i in range(len(departements))]

	for indice, departement in enumerate(departements):
		for numero_dossier, dossier in enumerate(fichiers):
			for numero_commune, commune in enumerate(fichiers[numero_dossier]):
				if fichiers[numero_dossier][numero_commune]["nom_dept"] == departement:
					commune_par_departement[indice] += 1

	nombre_moyen_commune_par_departement = sum(commune_par_departement)/len(commune_par_departement)
	#print("Il y a en moyenne {} communes par département".format(round(nombre_moyen_commune_par_departement)))

	return round(nombre_moyen_commune_par_departement)


#********************************************************************************
# 6. Quel est le nombre moyen de départements par région?
#********************************************************************************

def moyenne_departement_par_region(fichiers, regions):
	departement_par_region = [[] for i in range(len(regions))]

	for indice_region, region in enumerate(regions):
		for numero_dossier, dossier in enumerate(fichiers):
			for numero_commune, commune in enumerate(fichiers[numero_dossier]):
				if fichiers[numero_dossier][numero_commune]["nom_region"] == region:
					if fichiers[numero_dossier][numero_commune]["nom_dept"] not in departement_par_region[indice_region]:
						departement_par_region[indice_region].append(fichiers[numero_dossier][numero_commune]["nom_dept"])

	nombre_moyen_departement_par_region = 0
	for indice_region, dep_region in enumerate(departement_par_region):
		nombre_moyen_departement_par_region += len(dep_region)

	nombre_moyen_departement_par_region /= len(regions)
	#print("Il y a en moyenne {} départements par région".format(round(nombre_moyen_departement_par_region)))

	return round(nombre_moyen_departement_par_region)


#********************************************************************************
# 7. Quel est le nombre moyen de communes par région?
#********************************************************************************

def moyenne_commune_par_region(fichiers, regions):
	commune_par_region = [0 for i in range(len(regions))]

	for indice, region in enumerate(regions):
		for numero_dossier, dossier in enumerate(fichiers):
			for numero_commune, commune in enumerate(fichiers[numero_dossier]):
				if fichiers[numero_dossier][numero_commune]["nom_region"] == region:
					commune_par_region[indice] += 1


	nombre_moyen_commune_par_region = sum(commune_par_region)/len(commune_par_region)
	#print("Il y a en moyenne {} communes par région".format(round(nombre_moyen_commune_par_region)))

	return round(nombre_moyen_commune_par_region)

def parallelisation(nom_fonction):
	if nom_fonction == "nombre_statuts":
		return nombre_statuts(statuts)
	elif nom_fonction == "commune_par_statut":
		return commune_par_statut(fichiers, statuts)
	elif nom_fonction == "population_par_departement":
		return population_par_departement(fichiers, departements)
	elif nom_fonction == "population_par_region":
		return population_par_region(fichiers, regions)
	elif nom_fonction == "moyenne_commune_par_departement":
		return moyenne_commune_par_departement(fichiers, departements)
	elif nom_fonction == "moyenne_departement_par_region":
		return moyenne_departement_par_region(fichiers, regions)
	elif nom_fonction == "moyenne_commune_par_region":
		return moyenne_commune_par_region(fichiers, regions)

#********************************************************************************
# Main
#********************************************************************************

if __name__ == "__main__":

	start_time = time.time()


	# Parallélisation de l'ouverture des fichiers
	pool = multiprocessing.Pool(4)
	dossiers = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", 
	"14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", 
	"30", "31", "32", "33", "34", "35", "36"]

	# fichiers est une liste de liste de dictionnaires. Elle comporte 37 listes de dictionnaires
	# fichiers[i] est le ième dossier de data et contient mille fichiers (sauf pour le dernier dossier)
	# fichiers[i][0] donne accès à la première commune du dossier i
	fichiers = pool.map(ouvrir_fichiers_par_dossier, dossiers)
	statuts, departements, regions = initialiser_donnees(fichiers)


	# Parallélisation de l'utilisation des fonctions
	pool_fonctions = multiprocessing.Pool(4)
	nom_fonction = ["nombre_statuts", "commune_par_statut", "population_par_departement", "population_par_region"
					, "moyenne_commune_par_departement", "moyenne_departement_par_region", "moyenne_commune_par_region"]
	resultats = pool_fonctions.map(parallelisation, nom_fonction)	
	for resultat in resultats:
		print(resultat)

	print("--- %s seconds --- " %(time.time() - start_time))
