# -*- coding: cp1252 -*-
import arcpy


#-------------------------- FONCTION QUI CREE LES FEATURES CLASSES NECESSAIRES
def create_fc_anomalie(out_gdbname, fc_pl, geometry_type_pl, pl_template_fc, fc_supports, support_template_fc,
                       fc_reseau_branchement, geometry_type_reseau, has_m, has_z, reseau_template_fc):
    
    if not arcpy.Exists(fc_pl):
        pl_spatial_ref = arcpy.Describe(pl_template_fc).spatialReference            #-- On ajoute les references spatiales
        arcpy.CreateFeatureclass_management(out_gdbname, fc_pl, geometry_type_pl, pl_template_fc, has_m, has_z, pl_spatial_ref)
        arcpy.AddMessage("Feature class PL_Anomalies buid succesfully ...")
            
    if not arcpy.Exists(fc_supports):
        sup_spatial_ref = arcpy.Describe(support_template_fc).spatialReference      #-- On ajoute les references spatiales
        arcpy.CreateFeatureclass_management(out_gdbname, fc_supports, geometry_type_pl, support_template_fc, has_m, has_z, sup_spatial_ref)
        arcpy.AddMessage("Feature class Supports_Defectueux buid succesfully ...")
            
    if not arcpy.Exists(fc_reseau_branchement):
        res_spatial_ref = arcpy.Describe(reseau_template_fc).spatialReference       #-- On ajoute les references spatiales
        arcpy.CreateFeatureclass_management(out_gdbname, fc_reseau_branchement, geometry_type_reseau, reseau_template_fc, has_m, has_z, res_spatial_ref)
        arcpy.AddMessage("Feature class Reseaux_Long buid succesfully ...")

#--------------------------------------------------------------------------------------------------------------
output_folderpath= arcpy.GetParameterAsText(0)
out_gdbname = "Gathering_Anomalies.gdb"

fc_pl = "PL_Anomalies"
pl_template_fc = arcpy.GetParameterAsText(1)

fc_supports = "Supports_Defectueux"
support_template_fc = arcpy.GetParameterAsText(2)

fc_reseau_branchement = "Reseaux_Long"
reseau_template_fc = arcpy.GetParameterAsText(3)

geometry_type_pl = "POINT"
geometry_type_reseau = "POLYLINE"


has_m = "DISABLED"
has_z = "DISABLED"

arcpy.env.workspace = output_folderpath
anomalie_gdb = output_folderpath + "/" + out_gdbname

# On lance la creation de la Geodatabase et des FC
try:
    if not arcpy.Exists(out_gdbname):
        arcpy.AddMessage("Start building the geodatabase ... ")
        arcpy.CreateFileGDB_management(output_folderpath, out_gdbname)
        arcpy.AddMessage("... Create de fatures classes ")
        create_fc_anomalie(anomalie_gdb, fc_pl, geometry_type_pl, pl_template_fc, fc_supports, support_template_fc,
                           fc_reseau_branchement, geometry_type_reseau, has_m, has_z, reseau_template_fc)
    else:
        arcpy.AddMessage("The geaodatabase " + out_gdbname + " already exists ...")
        #Le new workspace devient la gdb existante
        arcpy.env.workspace = anomalie_gdb
        if not arcpy.Exists(fc_pl) and not arcpy.Exists(fc_supports) and not arcpy.Exists(fc_reseau_branchement):
              arcpy.AddMessage("The geaodatabase " + out_gdbname + " is empty ... Starting create the features classes")
              create_fc_anomalie(arcpy.env.workspace, fc_pl, geometry_type_pl, pl_template_fc, fc_supports, support_template_fc,
                                 fc_reseau_branchement, geometry_type_reseau, has_m, has_z, reseau_template_fc)
        else:
              arcpy.AddMessage("The features classes already exists ...")
    arcpy.AddMessage("Geodatabase and features classes created")
except Exception as ex:
    arcpy.AddError(ex.message)

#-----------------------------------------------------------------------------------------------------------
