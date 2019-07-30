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
        workspace = os.path.dirname(input_table)
        if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
                return workspace
        else:
                return os.path.dirname(workspace)
#------------------------------------- Recherche de la plainte en fonction du SERVICE_NU ET LE RETOURNE ----------------------------------------
def findPL_ByContrat(plTable, searchValue, whereClause):
    
    fields = ["CONTRACT_NUMBER", "METER_NUMBER"]
    cursor = arcpy.da.SearchCursor(plTable, fields, whereClause)
    for row in cursor:
        arcpy.AddMessage("Recherche avec le CONTRACT_NUMBER ...")
        if searchValue == row[0]:
            return row[1]
        #else:
            #continue
#------------------------------------------------------------------------------------------------------------------------------------------------
    # Fonction pour remplir le champ "PL_METER" de la FC PL de la compil GIS
def fill_IN_CMS_Field(cms, plTable, whereClause):

    field = ["CONTRACT_NUMBER", "METER_NUMBER", "PL_METER"]
    meterNum=''
    cursor  = arcpy.da.UpdateCursor(cms, field)
    cpt=1
    for rowpl in cursor:
        meterNum = findPL_ByContrat(plTable, rowpl[0], whereClause)
        if meterNum is not None or meterNum != '':
            rowpl[2] = meterNum
            arcpy.AddMessage("Starting data update ...")
            cursorpl.updateRow(rowpl)
            arcpy.AddMessage("Update done ...")
            cpt+=1
        else:
            print("let's continue, going to the next step number " + str(cpt))
            #continue      
    arcpy.AddMessage("Count the PL not found in cms = " + str(cpt))
#-------------------------------------------------------------------------------------
    # Execution de la fonction
print("Lancement du script ...")
workspace = get_geodatabase_path(cmsTable)
arcpy.env.workspace = workspace

fields = arcpy.ListFields(cmsTable)

for field in fields:
    if field.name == "PL_METER":
        arcpy.AddMessage("The field {0} already exists. Deleting field in process ...".format(field.name))
        arcpy.DeleteField_management(cmsTable, ["PL_METER"])
        arcpy.AddMessage("The field {0} has been deleted.".format(field.name))

#Add a field "CMS_METER"
arcpy.AddMessage("------------------------------------------------------------------")
arcpy.AddMessage("Adding the field PL_METER in process ...")
arcpy.AddField_management(cmsTable, "PL_METER", "TEXT")
arcpy.AddMessage("The field {0} has been added.".format(field.name))
#-------------------------------------------------------------------------------------
fill_IN_CMS_Field(cmsTable, plTable, sqlCMS)

#Try to export the result on excel
layerName = "CMS_NotInPL"
arcpy.MakeFeatureLayer_management(cmsTable, layerName)
print("Feature layer succesfully created")

sql_clause = ("PL_METER IS NULL") # On ne recupere que les PL identifiés ds CMS
arcpy.SelectLayerByAttribute_management(layerName, "NEW_SELECTION", sql_clause)
print("Selection of ("+ sql_clause + ") done succesfully")

result = arcpy.GetCount_management(layerName)
count = int(result.getOutput(0))

arcpy.AddMessage("Exporting the result on excel")
arcpy.TableToExcel_conversion(layerName, excelOutput)
arcpy.AddMessage("Result exported successfully")





