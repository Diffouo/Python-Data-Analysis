# -*- coding: cp1252 -*-
import arcpy
import sys

consoTable = arcpy.GetParameterAsText(0)
plTable = arcpy.GetParameterAsText(1)

sqlConso = "\"AGENCY\" = 'CSC_NEW-BELL'"

#------- Recherche de la consommation en fonction du SERVICE_NU ET LE RETOURNE ----------------------
def findConso_ByContrat(consoTable, searchValue, sqlConso):

    fields = ["SERVICE_NU"]
    cursor = arcpy.da.SearchCursor(consoTable, fields, sqlConso)
    for row in cursor:
        if searchValue == row[0]:
            return searchValue
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #continue
#----------------------------------------------------------------------------- 
    # Fonction pour remplir le status de la  consommation dans la Table Join avec Reading.dbf pour le cycle 10 (
def fill_consoStatus(consoTable, plTable, sqlConso):

    fields = ["CONTRACT_NUMBER", "IN_CONSO"]
    meterNum=0
    cursorpl  = arcpy.da.UpdateCursor(plTable, fields)

    cpt=1
    for rowpl in cursorpl:
        meterNum = findConso_ByContrat(consoTable, rowpl[0], sqlConso)
        if meterNum > 200000000:
            arcpy.AddMessage("Valeur trouvee = " + str(meterNum))
            rowpl[1] = "YES"
            arcpy.AddMessage("Starting data update ...")
            cursorpl.updateRow(rowpl)
            arcpy.AddMessage("Update done ...")
        else:
            arcpy.AddMessage("let's continue, going to the next step number " + str(cpt))
            #continue
        cpt+=1
    arcpy.AddMessage("Count the PL_RDGCycle10 found in Consommation2.dbf = " + str(cpt))
#-------------------------------------------------------------------------------------
    # Execution de la fonction
arcpy.AddMessage("Lancement du script ...")
fill_consoStatus(consoTable, plTable, sqlConso)
