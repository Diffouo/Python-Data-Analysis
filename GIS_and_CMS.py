# -*- coding: cp1252 -*-
import arcpy
import sys
from arcpy import env
import os

#-------------------------------------------------------------
cmsTable = arcpy.GetParameterAsText(0)
plTable = arcpy.GetParameterAsText(1)
excelOutput = arcpy.GetParameterAsText(2)

sqlCMS = "AGENCE_NAME = 'CSC_NEW-BELL'"

def get_geodatabase_path(input_table):
        '''Return the Geodatabase path from the input table or feature class.
        :param input_table: path to the input table or feature class 
        '''
        workspace = os.path.dirname(input_table)
        if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
                return workspace
        else:
                return os.path.dirname(workspace)
#------------------------------------- Recherche de la plainte en fonction du SERVICE_NU ET LE RETOURNE ----------------------------------------
def findCMS_ByContrat(cms, searchValue, whereClause):

    fields = ["CONTRACT_NUMBER", "METER_NUMBER", "AGENCE_NAME"]
    cursor = arcpy.da.SearchCursor(cms, fields, whereClause)
    for row in cursor:
        if searchValue == row[0]:
            return row[1]
        #else:
            #continue
#------------------------------------------------------------------------------------------------------------------------------------------------
    # Fonction pour remplir le champ "IN_CMS" de la FC PL de la compil GIS
def fill_IN_CMS_Field(cms, plTable, whereClause):

    fields = ["CONTRACT_NUMBER", "METER_NUMBER", "Contrat_Facture_Terrain", "CMS_METER"]
    meterNum=''
    cursorpl  = arcpy.da.UpdateCursor(plTable, fields)

    cpt=1
    for rowpl in cursorpl:
        arcpy.AddMessage("Recherche avec le CONTRACT_NUMBER ...")
        if  rowpl[0] > 200000000: #Si le "CONTRACT_NUMBER" est bien renseigné
            meterNum = findCMS_ByContrat(cms, rowpl[0], whereClause)
            if meterNum is not None or meterNum != '':
                rowpl[3] = meterNum
                arcpy.AddMessage("Starting data update ...")
                cursorpl.updateRow(rowpl)
                arcpy.AddMessage("Update done ...")
            else:
                print("let's continue, going to the next step number " + str(cpt))
                #continue
        else:
            if rowpl[2] > 200000000:
                arcpy.AddMessage("Recherche avec le Contrat_Facture_Terrain ...")
                meterNum = findCMS_ByContrat(cms, rowpl[2], whereClause) #on recherche avec le contrat_Facture_Terrain quand le CONTRACT_NUMBER n'est pas bon
                if meterNum is not None or meterNum != '':
                    rowpl[3] = meterNum
                    arcpy.AddMessage("Starting data update 2...")
                    cursorpl.updateRow(rowpl)
                    arcpy.AddMessage("Update 2 done ...")
                else:
                    arcpy.AddMessage("let's continue 2, going to the next step number " + str(cpt))
                    #continue
                
        cpt+=1
    arcpy.AddMessage("Count the PL found in cms = " + str(cpt))
#-------------------------------------------------------------------------------------
    # Execution de la fonction
print("Lancement du script ...")
workspace = get_geodatabase_path(plTable)
arcpy.env.workspace = workspace

fields = arcpy.ListFields(plTable)

for field in fields:
    if field.name == "CMS_METER":
        Arcpy.AddMessage("The field {0} already exists. Deleting field in process ...".format(field.name))
        arcpy.DeleteField_management(plTable, ["CMS_METER"])
        Arcpy.AddMessage("The field {0} has been deleted.".format(field.name))

#Add a field "CMS_METER"
arcpy.AddField_management(plTable, "CMS_METER", "TEXT") 
#-------------------------------------------------------------------------------------
fill_IN_CMS_Field(cmsTable, plTable, sqlCMS)

#Try to export the result on excel
layerName = "PL_InCMS"
arcpy.MakeFeatureLayer_management(plTable, layerName)
print("Feature layer succesfully created")

sql_clause = ("CMS_METER IS NOT NULL") # On ne recupere que les PL identifiés ds CMS
arcpy.SelectLayerByAttribute_management(layerName, "NEW_SELECTION", sql_clause)
print("Selection of ("+ sql_clause + ") done succesfully")

result = arcpy.GetCount_management(layerName)
count = int(result.getOutput(0))

arcpy.AddMessage("Exporting the result on excel")
arcpy.TableToExcel_conversion(layerName, excelOutput)
arcpy.AddMessage("Result exported successfully")





