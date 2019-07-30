# -*- coding: cp1252 -*-
import arcpy, os
import xlrd
from xlwt import Workbook
import sys

#-------------------------------------------------------------------------------------------------------------------
#-------- Creation des features class en fonction du code_itineraire
def createFC_ByItineraire(in_table, codeTable):

    try:
        #Set environements settings
        arcpy.env.workspace = 'F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/'
        arcpy.env.qualifiedFieldNames = False
        
        fields=["OBJECTID", "CODE"]
        cursor = arcpy.da.SearchCursor(codeTable, fields)
        cpt=0

        #Initialize the workbook and the excelSheet
        print("On cree le workbook et on add une feuille")
        workbook = Workbook()
        sheet = workbook.add_sheet('Itineraire')
        print("Workbook et sheet crees")
        
        exRows = 1
        exColumns = 0
        sheet.write(0, 0, "CODE ITINERAIRE")
        sheet.write(0, 1, "NOMBRE DE PL_NEWBELL")
        print("Nomenclature des FC PL = PL + _10 (code du cycle) + _CodeItineraire")
        for row in cursor:            
            layerName = ("PL_JoinSelect"+str(row[1]))
            arcpy.MakeFeatureLayer_management(in_table, layerName)
            print("Feature layer succesfully created")

            sql_clause = ("ITINERARY_ = "+str(row[1]))
            arcpy.SelectLayerByAttribute_management(layerName, "NEW_SELECTION", sql_clause)
            print("Selection of ("+ sql_clause + ") done succesfully")
            
            result = arcpy.GetCount_management(layerName)
            count = int(result.getOutput(0))
            print("Nombre de lignes  Itineraire = "+str(row[1]) + " = " + str(count))

            print("Ecriture dans la sheet excel")
            #On charge les itineraire et le nombre de PLs dans le excelFile
            sheet.write(exRows, exColumns, str(row[1]))
            exColumns += 1
            sheet.write(exRows, exColumns, str(count))
            exRows += 1
            print("Ecriture dans la sheet excel avec succes")
            print("-----------------------------------------------------------")
            #----------------------------------
##            outFeature = ("F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/PL_RDGCycle10_"+str(row[1]))
##            arcpy.CopyFeatures_management(layerName, outFeature)
##            print("Copy of "+ outFeature +" done succesfully")
            print("----------------------------------------------------------------------")
            cpt=cpt+1

        #On enregistre le fichier excel
        print("Saving the excel file")
        workbook.save("F:/GIS_PROJECT_GDB/Data_Copy_CMS/Itineraires_NewBell.xls")
        print("Nombre total de FC crées = " + str(cpt))
    except Exception as e:
        # Si une exception est capturée, on affiche le line number et le message d'erreur
        tb = sys.exc_info()[2]
        print "Line %i" % tb.tb_lineno
        print e.message    
#-------------------------------------------------------------------------------------------------------------------------
        # On lance la creation des PL_Join en fonction des codes Itineraire
print("Lancecment du script ...")

createFC_ByItineraire('F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/PL_RDGCycle10',
                      'F:/GIS_PROJECT_GDB/Data_Copy_CMS/NewBell_Gathering_Compil.gdb/Itineraire')    
#-------------------------------------------------------------------------------------------------------------------------

