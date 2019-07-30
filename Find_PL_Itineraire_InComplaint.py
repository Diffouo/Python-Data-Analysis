# -*- coding: cp1252 -*-
import arcpy
import sys

complaintTable = arcpy.GetParameterAsText(0)
plTable = arcpy.GetParameterAsText(1)

sqlComplaint = "\"OFFICE\" = 'CSC_NEW-BELL'"

#------- Recherche de la plainte en fonction du SERVICE_NU ET LE RETOURNE ---------
def findComplaint_ByContrat(complaintTable, searchValue, sqlComplaint):

    fields = ["CONTRACT_I", "COMPLAINT_", "CURRENT_ST", "COMPLAINT1", "BILL_NUMBE", "COMPLAIN_1"]
    cursor = arcpy.da.SearchCursor(complaintTable, fields, sqlComplaint)
    for row in cursor:
        if searchValue == row[0]:
            return searchValue
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #continue
#-----------------------------------------------------------------------------

#------- Recherche le COMPLAINT_EN en fonction du Contrat ---------
def findComplaintEN_ByContrat(complaintTable, contractNum, sql):

    fields = ["CONTRACT_I", "COMPLAINT_"]
    cursor = arcpy.da.SearchCursor(complaintTable, fields, sql)
    for row in cursor:
        if contractNum == row[0]:
            return str(row[1])
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #continue
#-----------------------------------------------------------------------------
        #------- Recherche le COMPLAINT_STATUS en fonction du Contrat ---------
def findComplaintStatus_ByContrat(complaintTable, contractNum, sql):

    fields = ["CONTRACT_I", "CURRENT_ST"]
    cursor = arcpy.da.SearchCursor(complaintTable, fields, sql)
    for row in cursor:
        if contractNum == row[0]:
            return str(row[1])
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #continue
#-----------------------------------------------------------------------------
        #------- Recherche le COMPLAINT_MODE en fonction du Contrat ---------
def findComplaintMode_ByContrat(complaintTable, contractNum, sql):

    fields = ["CONTRACT_I", "COMPLAINT1"]
    cursor = arcpy.da.SearchCursor(complaintTable, fields, sql)
    for row in cursor:
        if contractNum == row[0]:
            return str(row[1])
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #continue
#-----------------------------------------------------------------------------
        #------- Recherche le BILL_NUMBE du complaint en fonction du Contrat ---------
def findBillNum_OfCmplt_ByContrat(complaintTable, contractNum, sql):

    fields = ["CONTRACT_I", "BILL_NUMBE"]
    cursor = arcpy.da.SearchCursor(complaintTable, fields, sql)
    for row in cursor:
        if contractNum == row[0]:
            return str(row[1])
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #continue
#-----------------------------------------------------------------------------
        #------- Recherche le COMPLAIN_1 (Libelle de la plainte en francais) en fonction du Contrat ---------
def findComplaintFR_ByContrat(complaintTable, contractNum, sql):

    fields = ["CONTRACT_I", "COMPLAIN_1"]
    cursor = arcpy.da.SearchCursor(complaintTable, fields, sql)
    for row in cursor:
        if contractNum == row[0]:
            return str(row[1])
            #print("Valeur trouvee = " + str(row[0]))
        #else:
            #continue
#-----------------------------------------------------------------------------
        
    # Fonction pour remplir les variables des plaintes dans la Table Join avec Reading.dbf pour le cycle 10
def fill_complaintStatus(complaintTable, plTable, sqlComplaint):

    #fieldConso = ["CONTRACT_I", "COMPLAINT_", "CURRENT_ST", "COMPLAINT1", "BILL_NUMBE", "COMPLAIN_1"]
    fields = ["CONTRACT_NUMBER", "IN_COMPLAINT"]
    sql2 = "IN_COMPLAINT IS NULL OR IN_COMPLAINT = ''"
    cursorpl  = arcpy.da.UpdateCursor(plTable, fields)

    cpt=1
    for rowpl in cursorpl:
        contractNum = findComplaint_ByContrat(complaintTable, rowpl[0], sqlComplaint)
        if contractNum is not None:
            if contractNum > 200000000:
                print("Contract_Number = " + str(contractNum))
                #sql = "\"CONTRACT_I\" = "+ str(contractNum)
##                complaintEN = findComplaintEN_ByContrat(complaintTable, contractNum, sql)
##                complaintST = findComplaintStatus_ByContrat(complaintTable, contractNum, sql)
##                complaintMODE = findComplaintMode_ByContrat(complaintTable, contractNum, sql)
##                complaintBillNum = findBillNum_OfCmplt_ByContrat(complaintTable, contractNum, sql)
##                complaintFR = findComplaintFR_ByContrat(complaintTable, contractNum, sql)
                
##                print("ComplaintEN = " + str(complaintEN))
##                print("complaintST = " + str(complaintST))
##                print("complaintMODE = " + str(complaintMODE))
##                print("complaintBillNum = " + str(complaintBillNum))
                #print("complaintFR = " + str(complaintFR))
                
                rowpl[1] = "YES"
##                rowpl[2] = complaintEN
##                rowpl[3] = complaintST
##                rowpl[4] = complaintMODE
##                rowpl[5] = complaintBillNum
                #rowpl[6] = complaintFR
                print("Starting data update ...")
                cursorpl.updateRow(rowpl)
                print("Update done ...")
                cpt+=1
            else:
                print("let's continue, going to the next step number " + str(cpt))
                #continue
    print("Count the PL found in complaints.dbf = " + str(cpt))
#-------------------------------------------------------------------------------------
    # Execution de la fonction
print("Lancement du script ...")
fill_complaintStatus(complaintTable, plTable, sqlComplaint)
