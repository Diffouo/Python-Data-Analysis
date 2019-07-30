# -*- coding: cp1252 -*-
import arcpy

#-------- Retourne tous les supports Cassés, Pourris, Pourri-Operationnel, Tombés
        # et les insere dans la fc_Supports (de la .gdb des anomalies)
def get_support_anomalies(in_table, out_table, sql_condition):

    fields=["OBJECTID", "SHAPE", "ID_Support", "Nature", "Reseau", "Effort", "Etat", "Hauteur", "Localisation", "GlobalID", "Data_Creator", "Assemblage", "Date_Visite"]

    cursor = arcpy.SearchCursor(in_table, sql_condition, fields)
    cursorInsert = arcpy.InsertCursor(out_table, fields)
    
    cpt=0
    for row in cursor:
        print(row)
        print("Insertion d'un support defectueux...")
        cursorInsert.insertRow(row)
        print("Support defectueux insere ...")
        cpt+=1
    print("Nombre lignes insérées = " + str(cpt))

    #On supprime de le curseur d'insertion
    del cursorInsert
#------------------------------------------------------------------------------------------------------------------------
        # Fonction qui demande au user s'il desire exporter les data sous excel
def exportToExcel(out_table, xls_path):
    # On demande au user s'il desire effectuer une exportation du resultat sous excel
    print("Veuillez tapez: ")
    print("1 >>> pour exporter le resultat sous excel")
    print("2 >>> pour quitter le programme")
    rep = input("Entrer votre choix : ")
    
    if rep==1:
        print("Lancement exportation sous excel ...")
        arcpy.TableToExcel_conversion(out_table, xls_path)
        print("Exportation effectuée avec succès ...")
    elif rep==2:
        print("Fin du programme.")
    else:
        print("Fin du programme.")
#---------------------------------------------------------------------------------------------------------------------------
sql_clause="Etat = 'Cassé' OR Etat = 'Pourri' OR Etat = 'Pourri-Operationnel' OR Etat = 'Tombé'"

support_fc = r'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/Supports'
support_anomalie_fc = r'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/Supports_Defectueux'

#-------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------- EXECUTION DES FONCTIONS -------------------------------------------------
get_support_anomalies(support_fc, support_anomalie_fc, sql_clause)
exportToExcel(support_anomalie_fc, 'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Supports_Defectueux.xls')

# Update la valeur 'Etat' par le libelle
#updateSupport_ByLib(support_anomalie_fc)
