#********************************************************************************
# Laila Zouaki
# TP4
#********************************************************************************


import json
import os, os.path
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


# fichiers est une liste de liste de dictionnaires. Elle comporte 37 listes de dictionnaires
# fichiers[i] est le ième dossier de data et contient mille fichiers (sauf pour le dernier dossier)
# fichiers[i][0] donne accès à la première commune du dossier i
def ouvrir_tous_fichiers(nombre_dossiers):
	fichiers = [ouvrir_fichiers_par_dossier("0{}".format(i)) for i in range(10)]
	fichiers += [ouvrir_fichiers_par_dossier("{}".format(i)) for i in range(10, nombre_dossiers)]

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


#********************************************************************************
# Main
#********************************************************************************

if __name__ == "__main__":

	start_time = time.time()

	fichiers = ouvrir_tous_fichiers(37)
	statuts, departements, regions = initialiser_donnees(fichiers)
	print(nombre_statuts(statuts))
	print(commune_par_statut(fichiers, statuts))
	print(population_par_departement(fichiers, departements))
	print(population_par_region(fichiers, regions))
	print(moyenne_commune_par_departement(fichiers, departements))
	print(moyenne_departement_par_region(fichiers, regions))
	print(moyenne_commune_par_region(fichiers, regions))

	print("--- %s seconds --- " %(time.time()-start_time))
