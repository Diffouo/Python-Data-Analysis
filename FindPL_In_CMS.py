# -*- coding: cp1252 -*-
import arcpy
import sys

cmsTable = 'F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/cms'
plTable = 'F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/PL_RDGCycle10'

sqlCMS = "AGENCE_NAME = 'CSC_NEW-BELL'"

#------------------------------------- Recherche de la plainte en fonction du SERVICE_NU ET LE RETOURNE ----------------------------------------
def findCMS_ByContrat(complaintTable, searchValue, sqlComplaint):

    fields = ["CONTRACT_I", "COMPLAINT_", "CURRENT_ST", "COMPLAINT1", "BILL_NUMBE", "COMPLAIN_1"]
    cursor = arcpy.da.SearchCursor(complaintTable, fields, sqlComplaint)
    for row in cursor:
        if searchValue == row[0]:
            #return searchValue
            return (str(searchValue) + "[o]"+ str(row[1]) + "[o]" + str(row[2]) + "[o]" + str(row[3])+ "[o]" + str(row[4]) + "[o]" + str(row[5]))
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #continue
#------------------------------------------------------------------------------------------------------------------------------------------------
    # Fonction pour remplir les variables des plaintes dans la Table Join avec Reading.dbf pour le cycle 10
def fill_complaintStatus(complaintTable, plTable, sqlComplaint):

    fields = ["CONTRACT_NUMBER", "IN_COMPLAINT", "COMPLAINT_EN", "COMPLAINT_STATUS", "COMPLAINT_MODE", "BILL_NUMBER", "COMPLAINT_FR"]
    meterNum=0
    cursorpl  = arcpy.da.UpdateCursor(plTable, fields)

    cpt=1
    for rowpl in cursorpl:
        data = findComplaint_ByContrat(complaintTable, rowpl[0], sqlComplaint)
        if data is not None:
            tabVal = (str(data)).split('[o]')
            data[0] = int(data[0])
            if data[0] > 200000000:
                print("Meter_Number = " + str(data[0]) + "Complaint = " + str(data[1]))
                #rowpl[1] = "YES"
                print("Starting data update ...")
                cursorpl.updateRow(rowpl)
                print("Update done ...")
            else:
                print("let's continue, going to the next step number " + str(cpt))
                #continue
        cpt+=1
    print("Count the PL_RDGCycle10 found in complaints.dbf = " + str(cpt))
#-------------------------------------------------------------------------------------
    # Execution de la fonction
print("Lancement du script ...")
fill_complaintStatus(complaintTable, plTable, sqlComplaint)
