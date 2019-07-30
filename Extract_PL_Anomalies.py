# -*- coding: cp1252 -*-
# --------- Fonction qui retourne les PL en fonction de la requete SQL
def extractPL_BySQL(workspace, in_table, out_table, SQL, xls_path):

    arcpy.env.worspace = workspace
    
    fields=["OBJECTID", "SHAPE", "METER_NUMBER", "CLIENT_NAME", "CONTRACT_NUMBER", "SERVICE_STATUS", "Contrat_Facture_Terrain", "Compteur_Terrain",
            "Type_Compteur", "Phasage_Compteur","Calibre_Disjoncteur", "Reglage_Disjoncteur", "Norme_Branchement", "Etat_Compteur",
            "Activite_Principale", "Type_Construction", "Distributeur_Coffret", "Anomallies", "CCFBD", "BCC", "Famille_Activite", "Index",
            "CONFIRMATION_INDEX", "NB_Roues", "Compteur_Scelle", "Disjoncteur_Scelle", "Coffret_Scelle", "Visibilite_Cable",
            "Accessibilite_Compteur", "Disjoncteur", "Code_Transfo", "Data_Creator", "Date_de_visite", "Observations", "GlobalID"]
    
    cursor = arcpy.da.SearchCursor(in_table, fields, SQL)
    cursorInsert = arcpy.da.InsertCursor(out_table, fields)
    
    cpt=0
    for row in cursor:
        cursorInsert.insertRow(row)
        cpt+=1
    print("Nombre lignes insérées = " + str(cpt))

    #On supprime de le curseur d'insertion
    del cursorInsert

    print("Extration effectée avec succes !")
    if xls_path!='':
        exportToExcel(out_table, xls_path)
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

#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------- PL AVEC COMPTEUR ET SANS CONTRAT -----------------------------------------------------------------

print("CLIENT AVEC COMPTEUR ET SANS CONTRAT ... ")
sql_PL_Cpt_NoContrat = "(Compteur_Terrain <>  '') and (CONTRACT_NUMBER = 0 or Contrat_Facture_Terrain = 0 or CONTRACT_NUMBER is null or  Contrat_Facture_Terrain  is null)  and ( METER_NUMBER = '' or METER_NUMBER is null)"
                      
extractPL_BySQL('F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES', 'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL',
                'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL_Cpt_NoContrat', sql_PL_Cpt_NoContrat,
                'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/PL_Compteur_NoContrat.xls')
#---------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------- PL SANS COMPTEUR ET SANS CONTRAT --------------------------------------------------------------------

print("CLIENT SANS COMPTEUR ET SANS CONTRAT ... ")
sql_PL_NoCpt_NoContrat = "(Compteur_Terrain =  '') and (CONTRACT_NUMBER = 0 or Contrat_Facture_Terrain = 0 or CONTRACT_NUMBER is null or  Contrat_Facture_Terrain  is null)  and ( METER_NUMBER = '' or METER_NUMBER is null)"

extractPL_BySQL('F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES', 'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL',
                'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL_NoCpt_NoContrat', sql_PL_NoCpt_NoContrat,
                'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/PL_NoCompteur_NoContrat.xls')

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------- PL EN FRAUDE DIRECTE ----------------------------------------------------------------------
print("CLIENT EN FRAUDE DIRECTE ... ")
sql_PL_FraudeDirecte = "Anomallies = 'AN032'"

extractPL_BySQL('F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES', 'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL',
                'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL_FraudeDirecte', sql_PL_FraudeDirecte,
                'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/PL_FraudeDirecte.xls')

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------ PL AVEC BCC OUVERTE ------------------------------------------------------------------------
print("PL AVEC BCC OUVERTE ... ")
sql_PL_BCCOpen = "BCC = 'BCC sans couvercle'"

extractPL_BySQL('F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES', 'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL',
                'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL_OpenBCC', sql_PL_BCCOpen,
                'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/PL_BCCOpen.xls')
