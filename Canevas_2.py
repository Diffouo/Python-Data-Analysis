# -*- coding: cp1252 -*-
#----------------------------------------------------- CANEVAS DE RESTITUTION -----------------------------------------------------#
import xlrd
from xlwt import Workbook
import arcpy, os
from arcpy import env
import time

readTime = 2.5
fc = arcpy.GetParameterAsText(0)
output_file = arcpy.GetParameterAsText(1)

def get_geodatabase_path(input_table):
        '''Return the Geodatabase path from the input table or feature class.
        :param input_table: path to the input table or feature class 
        '''
        workspace = os.path.dirname(input_table)
        if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
                return workspace
        else:
                return os.path.dirname(workspace)
#-----------------------------------------------------------------------------------------------------
#get count the number of FC by Code_Transfo
def countFCByTransfo(FeatureClass, SQL):
        
        get_geodatabase_path(FeatureClass)
        layerName = FeatureClass+"Selection"
	arcpy.MakeFeatureLayer_management (FeatureClass, layerName)
	arcpy.SelectLayerByAttribute_management (layerName, "NEW_SELECTION", SQL)
	result = arcpy.GetCount_management(layerName)
        count = int(result.getOutput(0))

        #Reset the layer name by deleting the current LayerName
        arcpy.Delete_management(layerName)

        return count
#------------------------------------------------------------------------------------------------------

#Spatial Join between Reseaux and PL
def spatialJoin_ReseauxPL(plFC, reseauFC, outputFC): 
        arcpy.AddMessage("Starting Spatial join between Reseaux and PL ...")
        arcpy.SpatialJoin_analysis(reseauFC, plFC, outputFC, "JOIN_ONE_TO_ONE", "KEEP_COMMON", None, "INTERSECT")
        arcpy.AddMessage("Spatial join done succeccfully. Output features class = " + outputFC)
        
#-----------------------------------------------------------------------------------------------------
#Summary Statistics
def summaryOfField(inputFC, outputTable, whereClause, transfo):

        layerName = inputFC+'_Summary_'+transfo
        arcpy.MakeFeatureLayer_management (inputFC, layerName)
        arcpy.SelectLayerByAttribute_management (layerName, "NEW_SELECTION", whereClause)

        arcpy.AddMessage("Calculating the summary of the input field")
        arcpy.Statistics_analysis(layerName, outputTable, [["Join_Count", "SUM"]])

        #On selectionne le SUM_Join_Count dans le ouputTable
        result = arcpy.GetCount_management(outputTable)
        count = int(result.getOutput(0))
        total = 0
        field = ["SUM_Join_Count"]
        if count > 0:                
                cursor = arcpy.da.SearchCursor(outputTable, field)
                for row in cursor:
                        if row[0] is not None:
                                total = row[0]
                        else:
                                total = 0
        else:
                #La table est vide
                total = 0    
                
        arcpy.AddMessage("Summary of field Join_Count has been done successfully. Sum = "+ str(total))

        arcpy.Delete_management(layerName)

        return total
#-----------------------------------------------------------------------------------------------------
        
#get count the number of FC by Code_Transfo and section cable
def countPLBySectionCable(inputJoinLayer, transfo, joinCol, sectionCable):
        get_geodatabase_path(inputJoinLayer)

        transfo.upper()
	whereSql = joinCol+ " LIKE '"+transfo+"%' AND Section_Cable LIKE '"+sectionCable+"'"

        layerName = inputJoinLayer+"Selection"
	arcpy.MakeFeatureLayer_management (inputJoinLayer, layerName)
	arcpy.SelectLayerByAttribute_management (layerName, "NEW_SELECTION", whereSql)
	result = arcpy.GetCount_management(layerName)
        count = int(result.getOutput(0))
        return count

#-----------------------------------------------------------------------------------------------------
#get reseau LENGHT by sectionCable and transfo
def lenghtReseauxByTransfo(reseauFC, transfo, sectionCable):
        get_geodatabase_path(reseauFC)
        transfo.upper()
	fields = ["OBJECTID", "Section_Cable", "SHAPE_Length"]
	whereSql = "Code_Transfo LIKE '"+transfo+"%' AND Section_Cable LIKE '"+sectionCable+"%'"

	longueur = 0
	cursor = arcpy.da.SearchCursor(reseauFC, fields, whereSql)
	if cursor is not None:
                for row in cursor:
                        longueur += row[2]
        return longueur
#------------------------------------------------------------------------------------------------------
def CanevasRestituion(fc, sh):
        
        try:
                #Setting the workspace
                environ = get_geodatabase_path(fc)
                arcpy.env.workspace = environ

                #On call la jointure de reseau vers PL
                spatialJoin_ReseauxPL("PL", "Reseaux", "Reso_PL_Join")
                
                fields = ("Post_Name", "Code_Poste", "Code_Transfo", "Puiss_Nom", "X", "Y")

                arcpy.AddMessage("Printing the header ...")                
                sh.write(0, 0, "Nom Poste")
                sh.write(0, 1, "Coord_X")
                sh.write(0, 2, "Coord_Y")
                sh.write(0, 3, "Code Poste")
                sh.write(0, 4, "Code Transfo") #codeTransfo.strip(codePoste) : il va rester en principe "01"
                sh.write(0, 5, "Puissance Transfo")
                sh.write(0, 6, "NB de PL inventories")
                sh.write(0, 7, "PL en section 3x70mm")
                sh.write(0, 8, "PL en section 3x50mm")
                sh.write(0, 9, "PL en section 4x25mm")
                sh.write(0, 10, "PL en section 4x16mm")
                sh.write(0, 11, "PL en section 2x16mm")
                sh.write(0, 12, "PL en Classique Monophase")
                sh.write(0, 13, "PL en Classique Triphase")
                sh.write(0, 14, "NB PL en direct")
                sh.write(0, 15, "NB BCC ouvertes")
                sh.write(0, 16, "NB Installation avec compact")
                sh.write(0, 17, "3x70mm")
                sh.write(0, 18, "3x50mm")
                sh.write(0, 19, "4x25mm")
                sh.write(0, 20, "4x16mm")
                sh.write(0, 21, "2x16mm")
                sh.write(0, 22, "Classique monophase")
                sh.write(0, 23, "Classique triphase")
                sh.write(0, 24, "NB Supports BT")
                sh.write(0, 25, "Casse")
                sh.write(0, 26, "Pourri")
                sh.write(0, 27, "Pourri-Operationnel")
                sh.write(0, 28, "Tombe")
                sh.write(0, 29, "NB lampes EP")
                arcpy.AddMessage("Header printed successfully ...")
                arcpy.AddMessage("--------------------------------------------------------------------------------------")
                line = 1

                fcPostePL = 'F:/GIS_PROJECT_GDB/COMPILE_GEODATABASE/NEWBELL/postes_pl'
                n = int(arcpy.GetCount_management(fcPostePL).getOutput(0))
                p = 1
                count = 0
                arcpy.SetProgressor("step", "Step progressor: Processing from 0 to {0}".format(n), 0, n, p)
                
                time.sleep(readTime)
                cursor1 = arcpy.da.SearchCursor(fcPostePL, ["POSTES_DAN"]) # On parcours la table qui stocke les transfo PL
                for row1 in cursor1:
                    count += 1
                    if (count % p) == 0:
                        arcpy.SetProgressorLabel("Searching statistics for Poste "+ row1[0] +"... printing at rows {0}".format(count))
                        arcpy.SetProgressorPosition(count)
                    #----------------------------------------------------------------------------------------------------------------------------
                    arcpy.AddMessage("Printing data at the row {0} for Poste {1}".format(count, row1[0]))
                    #Recuperation des données et ecriture dans excel
##                            sh.write(line, 0, row[0]) #NomPoste
##                            sh.write(line, 1, row[4]) #Coordonnées_X
##                            sh.write(line, 2, row[5]) #Coordonnées_Y
##                            sh.write(line, 3, row[1]) #CodePoste
##                            sh.write(line, 4, row[2]) #code du transfo
##                            sh.write(line, 5, row[3])
                    codeTrans = row1[0]+"01"
                    sh.write(line, 0, "EMPTY_NAME") #NomPoste
                    sh.write(line, 1, "EMPTY_X") #Coordonnées_X
                    sh.write(line, 2, "EMPTY_Y") #Coordonnées_Y
                    sh.write(line, 3, row1[0]) #CodePoste
                    sh.write(line, 4, codeTrans) #code du transfo
                    sh.write(line, 5, "EMPTY_POWER")
                    
                    #----------------------------------------------------------------------------------------------------------------------------
                    #Count the number of PL for the current transfo
                    nbPL = countFCByTransfo("PL", "Code_Transfo LIKE '"+row1[0]+"%' AND Data_Creator IS NOT NULL")
                    sh.write(line, 6, nbPL)
                    
                    #----------------------------------------------------------------------------------------------------------------------------
                    #Nombre de PL en fonction de la section du cable et du reseau
                    PL3par70 = summaryOfField("Reso_PL_Join", ("Stats3par70_"+str(row1[0])), "Code_Transfo_1 LIKE '"+row1[0]+"%' AND Section_Cable LIKE '3x70mm%'", str(row1[0]))
                    #PL3par70 = countFCByTransfo("Reso_PL_Join", "Code_Transfo LIKE '"+row[1]+"%' AND Section_Cable LIKE '3x70mm%'")
                    sh.write(line, 7, PL3par70)

                    PL3par50 = summaryOfField("Reso_PL_Join", ("Stats3par50_"+str(row1[0])), "Code_Transfo_1 LIKE '"+row1[0]+"%' AND Section_Cable LIKE '3x50mm%'", str(row1[0]))
                    #PL3par50 = countFCByTransfo("Reso_PL_Join", "Code_Transfo LIKE '"+row[1]+"%' AND Section_Cable LIKE '3x50mm%'")
                    sh.write(line, 8, PL3par50)

                    PL4par25 = summaryOfField("Reso_PL_Join", ("Stats4par25_"+str(row1[0])), "Code_Transfo_1 LIKE '"+row1[0]+"%' AND Section_Cable LIKE '4x25mm%'", str(row1[0]))
                    #PL4par25 = countFCByTransfo("Reso_PL_Join", "Code_Transfo LIKE '"+row[1]+"%' AND Section_Cable LIKE '4x25mm%'")
                    sh.write(line, 9, PL4par25)

                    PL4par16 = summaryOfField("Reso_PL_Join", ("Stats4par16_"+str(row1[0])), "Code_Transfo_1 LIKE '"+row1[0]+"%' AND Section_Cable LIKE '4x16mm%'", str(row1[0]))
                    #PL4par16 = countFCByTransfo("Reso_PL_Join", "Code_Transfo LIKE '"+row[1]+"%' AND Section_Cable LIKE '4x16mm%'")
                    sh.write(line, 10, PL4par16)

                    PL2par16 = summaryOfField("Reso_PL_Join", ("Stats2par16_"+str(row1[0])), "Code_Transfo_1 LIKE '"+row1[0]+"%' AND Section_Cable LIKE '2x16mm%'", str(row1[0]))
                    #PL2par16 = countFCByTransfo("Reso_PL_Join", "Code_Transfo LIKE '"+row[1]+"%' AND Section_Cable LIKE '2x16mm%'")
                    sh.write(line, 11, PL2par16)

                    PL_ClassMono = summaryOfField("Reso_PL_Join", ("StatsClassMono_"+str(row1[0])), "Code_Transfo_1 LIKE '"+row1[0]+"%' AND Section_Cable LIKE 'Classique Monophas%'", str(row1[0]))
                    #PL_ClassMono = countFCByTransfo("Reso_PL_Join", "Code_Transfo LIKE '"+row[1]+"%' AND Section_Cable LIKE 'Classique Monophas%'")
                    sh.write(line, 12, PL_ClassMono)

                    PL_ClassTri = summaryOfField("Reso_PL_Join", ("StatsClassTri_"+str(row1[0])), "Code_Transfo_1 LIKE '"+row1[0]+"%' AND Section_Cable LIKE 'Classique Triphas%'", str(row1[0]))
                    #PL_ClassTri = countFCByTransfo("Reso_PL_Join", "Code_Transfo LIKE '"+row[1]+"%' AND Section_Cable LIKE 'Classique Triphas%'")
                    sh.write(line, 13, PL_ClassTri)

                    #-----------------------------------------------------------------------------------------------------------------------------
                    #PL en fraude directe
                    PL_EnDirect = countFCByTransfo("PL", "Code_Transfo LIKE '"+row1[0]+"%' AND Anomallies = 'AN032'")
                    sh.write(line, 14, PL_EnDirect)
                    
                    #PL avec BCC ouverte
                    PL_OpenBCC = countFCByTransfo("PL", "Code_Transfo LIKE '"+row1[0]+"%' AND BCC = 'BCC sans couvercle'")
                    sh.write(line, 15, PL_OpenBCC)

                    #PL avec disjoncteur compact
                    PL_CompactDisj = countFCByTransfo("PL", "Code_Transfo LIKE '"+row1[0]+"%' AND Calibre_Disjoncteur = 'Compact'")
                    sh.write(line, 16, PL_CompactDisj)
                    
                    #-----------------------------------------------------------------------------------------------------------------------------
                    #Longueur des reseaux par section de cable
                    len3par70 = lenghtReseauxByTransfo("Reseaux", row1[0], "3x70mm")
                    sh.write(line, 17, len3par70)
                    
                    len3par50 = lenghtReseauxByTransfo("Reseaux", row1[0], "3x50mm")
                    sh.write(line, 18, len3par50)
                    
                    len4par25 = lenghtReseauxByTransfo("Reseaux", row1[0], "4x25mm")
                    sh.write(line, 19, len4par25)
                    
                    len4par16 = lenghtReseauxByTransfo("Reseaux", row1[0], "4x16mm")
                    sh.write(line, 20, len4par16)
                    
                    len2par16 = lenghtReseauxByTransfo("Reseaux", row1[0], "2x16mm")
                    sh.write(line, 21, len2par16)
                    
                    lenClassMono = lenghtReseauxByTransfo("Reseaux", row1[0], "Classique Monophas")
                    sh.write(line, 22, lenClassMono)
                    
                    lenClassTriph = lenghtReseauxByTransfo("Reseaux", row1[0], "Classique Triphas")
                    sh.write(line, 23, lenClassTriph)
                    
                    #-------------------------------------------------------------------------------------------------------------------------------
                    #Nombre de Supports
                    Nbre_Support = countFCByTransfo("Supports", "ID_Support LIKE '"+row1[0]+"%'")
                    sh.write(line, 24, Nbre_Support)

                    #Supports cassé
                    supportCasse = countFCByTransfo("Supports", "ID_Support LIKE '"+row1[0]+"%' AND Etat LIKE 'Cass%'")
                    sh.write(line, 25, supportCasse)

                    SupportPourri = countFCByTransfo("Supports", "ID_Support LIKE '"+row1[0]+"%' AND Etat = 'Pourri'")
                    sh.write(line, 26, SupportPourri)

                    SupportPourriOP = countFCByTransfo("Supports", "ID_Support LIKE '"+row1[0]+"%' AND Etat = 'Pourri-Operationnel'")
                    sh.write(line, 27, SupportPourriOP)

                    SupportTombe = countFCByTransfo("Supports", "ID_Support LIKE '"+row1[0]+"%' AND Etat LIKE 'Tomb%'")
                    sh.write(line, 28, SupportTombe)
                    
                    #-------------------------------------------------------------------------------------------------------
                    # Eclairage_Public
                    NbreEP = countFCByTransfo("Eclairage_Public", "Code_Transfo LIKE '"+row1[0]+"%'")
                    sh.write(line, 29, NbreEP)
                    arcpy.AddMessage("Data printed succesfully at the row {0}".format(count))
                    arcpy.AddMessage("--------------------------------------------------------------------------------------")
                    
                    line += 1
                            
                #Reset the Reso_PL_Join by deleting the current Reso_PL_Join feature class
                arcpy.Delete_management("Reso_PL_Join")
                arcpy.AddMessage(str(count) + "Items found. Printing found items: ")
        except Exception as ex:
                arcpy.AddMessage("Rolling back all the printed data")
                # Si une exception est capturée, on affiche le line number et le message d'erreur
                tb = sys.exc_info()[2]
                arcpy.AddError( "An excption occured on line %i" % tb.tb_lineno)
                arcpy.AddError("Error message : " + ex.message)
                arcpy.AddMessage("RollBack done...")
                
#----------------------------------------------------------------------------------------------------------------------------------------
#Opening a fresh excel workbook
wb = Workbook()
#Adding a sheet into the workbook
excelSheet = wb.add_sheet('Restitution_NewBell')
CanevasRestituion(fc, excelSheet)
arcpy.AddMessage("Saving the statistic result in the Excel output {0}".format(output_file))
wb.save(output_file)
#----------------------------------------------------------------------------------------------------------------------------------------
