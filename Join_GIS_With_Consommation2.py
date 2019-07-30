import arcpy
import sys
#--------------------------------------------------------------------------------------------------------------
#--------------------- Fonction qui cree a jointure entre PL de GIS et la table Consommation2.dbf
def joinPL_to_Conso(environnement, inFeature, layerName, in_field,  joinTable, joinField, outFeature, sql_clause):
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

        arcpy.CopyFeatures_management(layerName, outFeature)
        print("Copy done succesfully")

    except Exception as e:
        # If an error occurred, print line number and error message
        tb = sys.exc_info()[2]
        print "Line %i" % tb.tb_lineno
        print e.message
#---------------------------------------------------------------------------------------------------------------
inFeature = 'F:/GIS_PROJECT_GDB/Data_Copy_CMS/Gathringvide.gdb/PL'
joinTable = 'F:/GIS_PROJECT_GDB/Data_Copy_CMS/Consommation2.dbf'

joinPL_to_Conso('FF:/GIS_PROJECT_GDB/Data_Copy_CMS/', inFeature, 'PL_Selection_BYCN', 'CONTRACT_NUMBER', joinTable, 'SERVICE_NU',
              'F:/GIS_PROJECT_GDB/Data_Copy_CMS/Gathringvide.gdb/PL_Join_Conso', 'Date_de_visite IS NOT NULL')
