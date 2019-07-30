# -*- coding: cp1252 -*-
import arcpy
from arcpy import env
import traceback, sys

#----------------------------------------------------------------------------------------------------------------------
#--------------------- Fonction qui cree a jointure entre PL de GIS et la table cms 
def joinPL_to_CMS(environnement, inFeature, layerName, in_field,  joinTable, joinField, outFeature, sql_clause):
    try:
        #Set environements settings
        env.workspace = environnement
        env.qualifiedFieldNames = False

        # Create a feature layer from the PL featureclass
        arcpy.MakeFeatureLayer_management(inFeature, layerName)
        print("Feature layer succesfully created")
    
        # Join the feature layer to a table
        arcpy.AddJoin_management(layerName, in_field, joinTable, joinField, "KEEP_COMMON")
        print("Join succesfully added")
        
        # Select desired features from PL with SQL_Clause
        arcpy.SelectLayerByAttribute_management(layerName, "NEW_SELECTION", sql_clause)
        print("Selection done succesfully")

        arcpy.CopyFeatures_management(layerName, outFeature)
        print("Copy done succesfully")

    except Exception as e:
        # If an error occurred, print line number and error message
        tb = sys.exc_info()[2]
        print "Line %i" % tb.tb_lineno
        print e.message
#----------------------------------------------------------------------------------------------------------------------
#--------------------- Fonction qui cree a jointure entre PL de GIS et la table cms
def joinPL_CMS_ByMeterNum(environnement, inFeature, layerName, in_field,  joinTable, joinField, outFeature, sql_clause):
    try:
        #Set environements settings
        env.workspace = environnement
        env.qualifiedFieldNames = False

        # Create a feature layer from the PL featureclass
        arcpy.MakeFeatureLayer_management(inFeature, layerName)
        print("Feature layer succesfully created")
    
        # Join the feature layer to a table
        arcpy.AddJoin_management(layerName, in_field, joinTable, joinField, "KEEP_COMMON")
        print("Join succesfully added")
        
        # Select desired features from PL with SQL_Clause
        arcpy.SelectLayerByAttribute_management(layerName, "NEW_SELECTION", sql_clause)
        print("Selection done succesfully")

        cursor = arcpy.da.SearchCursor(layerName)
        cursorInsert = arcpy.da.InsertCursor(outFeature)
    
        cpt=0
        for row in cursor:
            print("Insertion des join Compteur terrain ...")
            cursorInsert.insertRow(row)
            print("Des join Compteur terrain inseré ...")
            cpt+=1
        print("Nombre lignes insérées = " + str(cpt))

        #On supprime de le curseur d'insertion
        del cursorInsert
        
    except Exception as e:
        # If an error occurred, print line number and error message
        tb = sys.exc_info()[2]
        print "Line %i" % tb.tb_lineno
        print e.message
#------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
    # 1. Jointure entre CONTRACT_NUMBER(PL) et CONTRACT_NUMBER(cms)
inFeature = 'F:/GIS_PROJECT_GDB/Gathringvide.gdb/PL'
joinTable = 'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Postes_Complets_NewBell.gdb/cms'

joinPL_to_CMS('F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/', inFeature, 'PL_Selection_BYCN', 'CONTRACT_NUMBER', joinTable, 'CONTRACT_NUMBER',
              'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Postes_Complets_NewBell.gdb/PL_Join', 'Date_de_Visite IS NOT NULL')
###-------------------------------------------------------------------------------------------------------------------------
##        # 2. Jointure entre Compteur_Terrain(PL) et METER_NUMBER(cms)
##print("Join by Compteur_Terrain and METER_NUMBER starting ...")
##joinPL_CMS_ByMeterNum('F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/', inFeature, 'PL_Selection_BY_METERNUM', 'Compteur_Terrain', joinTable, 'METER_NUMBER',
##              'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Postes_Complets_NewBell.gdb/PL_Join_MeterNum', 'Date_de_Visite IS NOT NULL')



