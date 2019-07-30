# -*- coding: cp1252 -*-
import arcpy
import codecs
import xlrd
from xlwt import Workbook

inputFC = arcpy.GetParameterAsText(0)
outputFC = arcpy.GetParameterAsText(1)
outputExcel = arcpy.GetParameterAsText(2)
#-----------------------------------------------------------------------------------------------------------------------
    # -------- Retourne le libelle de l'accessibilité compteur en fonction de son code
def getEtatSupport_byCode(in_code):
    if in_code=='Bon': return 'Bon-Operationnel'
    if in_code==('Cass'+u'\xe9'): return 'Couche sur cloture, mur, toiture'
    if in_code==('Tomb'+u'\xe9'): return 'Couche par terre ou a hauteur d homme'
    if in_code== 'Pourri': return 'Pourri'
    if in_code== 'Pourri-Operationnel': return  'Pourri-Operationnel'

#-----------------------------------------------------------------------------------------------------------------------
#-------- Update le champ Etat des supports par le libelle correspondant au code (ds la .gdb des anomalie)
def updateSupport_ByLib(in_table):

    field=("Etat")

    cursor = arcpy.da.UpdateCursor(in_table, field)
    cpt=0
    for row in cursor:
        row[0] = getEtatSupport_byCode(row[0])
        print("Mise a jour des valeurs ...")
        cursor.updateRow(row)
        print("Mise a jour effectuee avec succes ...")
        cpt+=1
    print("Nombre lignes update = " + str(cpt))
#-------------------------------------------------------------------------------------------------------------------------
def correct_char(value):
    rep = ''
    espion=0
    for charVal in value:
        if charVal==u'\xe9': #é : e with acute
            value =  value.replace(charVal, 'e')
        if charVal==u'\xc9': # E with acute
            print("char trouve = " + charVal)
            value =  value.replace(charVal, 'E')

        if charVal==u'\xe0': # à : a with grave
            value = value.replace(charVal, 'a')
        if charVal==u'\xe2': # a with circumflex
            value = value.replace(charVal, 'a')
        if charVal==u'\xe8': # è : e with grave
            value = value.replace(charVal, 'e')
        if charVal==u'\xb0': #Degree sign
            value = value.replace(charVal,'m')
        if charVal==u'\xf4': #ô : o with circumflex
            value = value.replace(charVal,'o')
        return value
#-------------------------------------------------------------------------------------------------------------------------------------
#-------- Retourne tous les supports Cassés, Pourris, Pourri-Operationnel, Tombés
        # et les insere dans la fc_Supports (de la .gdb des anomalies)
def get_support_anomalies(in_table, out_table, sql_condition, outputExcel):
        fields=["OBJECTID", "SHAPE", "ID_Support", "Nature", "Reseau", "Effort", "Etat", "Hauteur",
                "Localisation", "GlobalID", "Data_Creator", "Assemblage", "Date_Visite"]
        
        cursor = arcpy.da.SearchCursor(in_table, fields, sql_condition,)
        cursorInsert = arcpy.da.InsertCursor(out_table, fields)
        arcpy.AddMessage("Collecting the list of Supports pourris ...")
        cpt=0
        wb = Workbook()
	sheet = wb.add_sheet('Performances')
	#Adding headers to the sheet
	sheet.write(0,0, 'ID_SUPPORT')
	sheet.write(0,1, 'NATURE')
	sheet.write(0,2, 'RESEAU')
	sheet.write(0,3, 'EFFORT')
	sheet.write(0,4, 'ETAT')
	sheet.write(0,5, 'HAUTEUR')
	sheet.write(0,6, 'LOCALISATION')
	sheet.write(0,7, 'DATA CREATOR')
	sheet.write(0,8, 'ASSEMBLAGE')
	sheet.write(0,9, 'DATE VISITE')
	
	line = 1

        reseau = ''
        fileIndex=0
        info = arcpy.Describe(inputFC)
	arcpy.AddMessage("Start printing the excel file")
	arcpy.SetProgressor("step", "Collecting '\Supports_Pourris\'...", 0, 100, 1)
        for row in cursor:
            arcpy.SetProgressorLabel("Insert rows in the output feature class {0} ...".format(info.name))
            arcpy.SetProgressorPosition()
            cursorInsert.insertRow(row)
            
            sheet.write(line,0, str(row[2]))
            sheet.write(line,1, str(row[3]))

            if row[4] == ('R'+u'\xe9'+'seau BT'):
                reseau = 'Reseau BT'
            sheet.write(line,2, reseau)
            sheet.write(line,3, str(row[5]))
            etat = getEtatSupport_byCode(row[6])
            sheet.write(line,4, etat)
            sheet.write(line,5, str(row[7]))

            local = correct_char(row[8])
            sheet.write(line,6, local)
            sheet.write(line,7, row[10])
            assemb = correct_char(row[11])
            sheet.write(line,8, assemb)
            sheet.write(line,9, row[12])

            if cpt <= 65535:
                arcpy.SetProgressorLabel("Saving the row " + str(cpt) +"to {0}".format(outputExcel))
                arcpy.SetProgressorPosition(50)
                wb.save(outputExcel)
            elif cpt > 65535 or cpt%65535==0:
                arcpy.SetProgressorLabel("Saving the " +  str(fileIndex+1)+ " file")
                arcpy.SetProgressorPosition(75)
                fileIndex += 1
                fileInfo = outputExcel.split('.')
                fileName = fileInfo[0]+str(fileIndex)
                outfile = fileName+str(fileInfo[1])
                wb.save(outfile)
            line += 1
            cpt+=1
            
        arcpy.AddMessage("-----------------------------")
        wb.save(outputExcel)
        arcpy.SetProgressorLabel("Finishing the process ...")
        arcpy.SetProgressorPosition(75)
        arcpy.AddMessage("... Export done successfully")
        arcpy.AddMessage("Count rows = " + str(cpt))

        #On supprime de le curseur d'insertion
        del cursorInsert
#---------------------------------------------------------------------------------------------------------------------------
sql_clause="Etat = 'Cassé' OR Etat = 'Pourri' OR Etat = 'Pourri-Operationnel' OR Etat = 'Tombé'"

#-------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------- EXECUTION DES FONCTIONS -------------------------------------------------
get_support_anomalies(inputFC, outputFC, sql_clause, outputExcel)
##
### Update la valeur 'Etat' par le libelle
##updateSupport_ByLib(support_anomalie_fc)


