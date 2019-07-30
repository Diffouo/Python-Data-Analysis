# -*- coding: cp1252 -*-
import arcpy
import sys

#--------------------------------------------------------------------------------------------------------------
#--------------------- Fonction qui cree a jointure entre PL de GIS et la table Reading.dbf
def joinPL_to_Reading(environnement, inFeature, layerName, in_field,  joinTable, joinField, outFeature, sql_clause):
    try:
        #Set environements settings
        arcpy.env.workspace = environnement
        arcpy.env.qualifiedFieldNames = False

        # Create a feature layer from the PL featureclass
        arcpy.MakeFeatureLayer_management(inFeature, layerName)
        print("Feature layer succesfully created")
    
        # Join the feature layer to a table
        arcpy.AddJoin_management(layerName, in_field, joinTable, joinField, "KEEP_COMMON")
        print("Join succesfully added")
        
        # Select desired features from PL with SQL_Clause
        arcpy.SelectLayerByAttribute_management(layerName, "NEW_SELECTION", sql_clause)
        print("Selection done succesfully")

        result = arcpy.GetCount_management(layerName)
        count = int(result.getOutput(0))
        print("Nombre de PL_NewBell croisés avec Reading.dbf= " + str(count))

        arcpy.CopyFeatures_management(layerName, outFeature)
        print("Copy done succesfully")

    except Exception as e:
        # If an error occurred, print line number and error message
        tb = sys.exc_info()[2]
        print "Line %i" % tb.tb_lineno
        print e.message
#---------------------------------------------------------------------------------------------------------------
        
        ## Fonction qui selectionne les PLs croisés avec Reading.dbf en fonction d'un cycle
def createPL_Reading_ByCycle(in_table, codeCycle):

    try:
        #Set environements settings
        arcpy.env.workspace = 'F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/'
        arcpy.env.qualifiedFieldNames = False
             
        layerName = "PL_JoinReadaingSelect"
        
        arcpy.MakeFeatureLayer_management(in_table, layerName)
        print("Feature layer succesfully created")

        sql_clause = ("CYCLE = "+codeCycle)
        arcpy.SelectLayerByAttribute_management(layerName, "NEW_SELECTION", sql_clause)
        print("Selection done succesfully")

        result = arcpy.GetCount_management(layerName)
        count = int(result.getOutput(0))
        print("Nombre de clients relevés au cycle " + str(codeCycle) + " = " + str(count))

        outFeature = ("F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/PL_RDGCycle"+codeCycle)
        arcpy.CopyFeatures_management(layerName, outFeature)
        print("Copy of PL_RDGCycle"+ str(codeCycle) + " done succesfully")
        print("----------------------------------------------------------------------")  
    except Exception as e:
        # Si une exception est capturée, on affiche le line number et le message d'erreur
        tb = sys.exc_info()[2]
        print "Line %i" % tb.tb_lineno
        print e.message
        
#-----------------------------------------------------------------------------------------------------------------------
inFeature = 'F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/PL'
joinTable = 'F:/GIS_PROJECT_GDB/Data_Copy_CMS/Reading.dbf'

print("Lancement de la jointure avec la table Reading.dbf ...")
joinPL_to_Reading('F:/GIS_PROJECT_GDB/Data_Copy_CMS/', inFeature, 'PL_Selection_BYCN', 'CONTRACT_NUMBER', joinTable, 'CONTRACT_I',
              'F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/PL_Join_Reading', 'Date_de_visite IS NOT NULL')
        
#-----------------------------------------------------------------------------------------------------------------------
    # De la jointure effectuee ci-dessus, on  extrait juste les data du Cycle 10 dans une new FC
    # ----- (Nous choisirons uniquement le cycle 10 de 2015 pour cette analyse)

print("Selection du croisement du cycle 10 ...")
createPL_Reading_ByCycle('F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/PL_Join_Reading', "10")

