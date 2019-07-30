# -*- coding: cp1252 -*-
import arcpy
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
#-----------------------------------------------------------------------------------------------------------------------
#-------- Retourne tous les branchements de longueur >=50 
def get_reseau_long(in_table, out_table, sql_condition, lngmaxReso, lngmaxBranch, xls_path):

    fields=["OBJECTID", "SHAPE", "Code_Poste", "Code_Transfo", "Type", "Section_Cable", "Reseau",
            "Depart_BT", "Date_Visite", "Data_Creator", "Observations", "SHAPE_Length"]

    cursor = arcpy.da.SearchCursor(in_table, fields, sql_condition)
    cursorInsert = arcpy.da.InsertCursor(out_table, fields)
    
    cpt=0
    for row in cursor:
        if row[6]==1 and row[11]>=lngmaxReso: #Insertion du resea long
            print("Insertion du reseau long ...")
            cursorInsert.insertRow(row)
            print("Reseau long insere ...")
            cpt+=1
        if row[6]==2 and row[11]>=lngmaxBranch: #Insertion du branchement long
            print("Insertion du branchement long ...")
            cursorInsert.insertRow(row)
            print("Branchement long insere ...")
            cpt+=1
    print("Nombre lignes insérées = " + str(cpt))
    if xls_path!='':
        exportToExcel(out_table, xls_path)
    #On supprime de le curseur d'insertion
    del cursorInsert
    
#-------------------------------------------------------------------------------------------------------------------------
sql_clause="Date_Visite is not null"

reseau_template_fc = r'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/Reseaux'
reseau_anomalie_fc = r'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/Reseaux_Branch_Long'

#-------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------- EXECUTION DES FONCTIONS -------------------------------------------------
#-------------- On laisse le user proposer les longueurs max des reseaux et branchements
reso_max = input("Entrer la longueur max du reseau entre deux entités : ")
print("Valeur = %f" % (reso_max))

branch_max = input("Entrer la longueur max du branchement entre deux entités : ")
print("Valeur = %f" % (branch_max))

#----- Recupere les reso et branch long, ensuite les insere dans la GDB des anomalies
#get_reseau_long(reseau_template_fc, reseau_anomalie_fc, sql_clause, reso_max, branch_max, 'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Reseaux_Branch_Long.xls')

exportToExcel(reseau_anomalie_fc, 'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Reseaux_Branch_Long.xls');
