# -*- coding: cp1252 -*-
import arcpy
import sys

payTable = arcpy.GetParameterAsText(0)
plTable = arcpy.GetParameterAsText(1)

sqlPay = "\"AGENCY\" = 'CSC_NEW-BELL'"
#------- Recherche du payment en fonction du SERVICE_NU ET LE RETOURNE ---------
def findPay_ByContrat(payTable, searchValue, sqlPay):

    fields = ["SERVICE_NU"]
    cursor = arcpy.da.SearchCursor(payTable, fields, sqlPay)
    for row in cursor:
        if searchValue == row[0]:
            return searchValue
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #print("let's continue search... current row " + str(nbre))
            #continue
#----------------------------------------------------------------------------- 
    # Fonction pour remplir le status du payment dans la Table Join avec Reading.dbf pour le cycle 10
def fill_payStatus(payTable, plTable, sqlPay):

    fields = ["CONTRACT_NUMBER", "IN_PAY"]
    meterNum=0
    cursorpl  = arcpy.da.UpdateCursor(plTable, fields)

    cpt=1
    nbr=0
    for rowpl in cursorpl:
        meterNum = findPay_ByContrat(payTable, rowpl[0], sqlPay)
        if meterNum > 200000000:
            arcpy.AddMessage("Valeur trouvee = " + str(meterNum))
            rowpl[1] = "YES"
            arcpy.AddMessage("Starting data update PL_RDGCycle10 ...")
            cursorpl.updateRow(rowpl)
            nbr += 1
            arcpy.AddMessage("Update done ...")
        else:
            arcpy.AddMessage("let's continue, going to the next step number " + str(cpt))
            #continue
        cpt+=1
    arcpy.AddMessage("Count the PL_RDGCycle10 found in Payment = " + str(nbr))

#-------------------------------------------------------------------------------------
    # Execution de la fonction
arcpy.AddMessage("Lancement du script ...")
fill_payStatus(payTable, plTable, sqlPay)
