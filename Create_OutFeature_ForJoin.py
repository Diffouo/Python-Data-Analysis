# -*- coding: cp1252 -*-
import arcpy

def create_fc_join(out_gdbname, fc_pl, geometry_type_pl, pl_template_fc, has_m, has_z):
    if not arcpy.Exists(fc_pl):
        pl_spatial_ref = arcpy.Describe(pl_template_fc).spatialReference            #-- On ajoute les references spatiales
        arcpy.CreateFeatureclass_management(out_gdbname, fc_pl, geometry_type_pl, pl_template_fc, has_m, has_z, pl_spatial_ref)

#--------------------------------------------------------------------------------------------------------------
pl_join = "PL_Join_CMS"
pl_cpt_nocontrat = "PL_Cpt_NoContrat"
pl_nocpt_nocontrat = "PL_NoCpt_NoContrat"
pl_fraude_directe = "PL_FraudeDirecte"
pl_open_bcc = "PL_OpenBCC"

ReseauLong = "Reseaux_Branch_Long"
SupportDefectueux = "Supports_Defectueux"

geometry_type_pl = "POINT"
geometry_type_reso = "POLYLINE"


pl_template_fc = r'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/PL'
reso_template_fc = r'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/Reseaux'
support_template_fc = r'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/Supports'

has_m = "DISABLED"
has_z = "DISABLED"

arcpy.env.workspace = r'F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Gathringvide.gdb/'

#----------------------------------------------------------------------------------------------------------------
# On lance la creation  et des FC
# PL join a CMS
try:
    if not arcpy.Exists(pl_join):
        print("Starting create PL_Join_CMS feature ...")
        create_fc_join(arcpy.env.workspace, pl_join, geometry_type_pl, pl_template_fc, has_m, has_z)
        print("PL_Join_CMS successfully created ...")
    else:
        print("PL_Join_CMS join already exists ...")
except Exception as ex:
    print(ex.message)

#----------------------------------------------------------------------------------------------------------------
# PL avec numero compteur et sans contrat
try:
    if not arcpy.Exists(pl_cpt_nocontrat):
        print("Starting create PL_Cpt_NoContrat feature ...")
        create_fc_join(arcpy.env.workspace, pl_cpt_nocontrat, geometry_type_pl, pl_template_fc, has_m, has_z)
        print("PL_Cpt_NoContrat successfully created ...")
    else:
        print("PL_Cpt_NoContrat join already exists ...")
except Exception as ex:
    print(ex.message)

#----------------------------------------------------------------------------------------------------------------
# PL sans numero compteur et sans contrat
try:
    if not arcpy.Exists(pl_nocpt_nocontrat):
        print("Starting create PL_NoCpt_NoContrat feature ...")
        create_fc_join(arcpy.env.workspace, pl_nocpt_nocontrat, geometry_type_pl, pl_template_fc, has_m, has_z)
        print("PL_NoCpt_NoContrat successfully created ...")
    else:
        print("PL_NoCpt_NoContrat join already exists ...")
except Exception as ex:
    print(ex.message)

#----------------------------------------------------------------------------------------------------------------
# PL en fraude directe
try:
    if not arcpy.Exists(pl_fraude_directe):
        print("Starting create PL_FraudeDirecte feature ...")
        create_fc_join(arcpy.env.workspace, pl_fraude_directe, geometry_type_pl, pl_template_fc, has_m, has_z)
        print("PL_FraudeDirecte successfully created ...")
    else:
        print("PL_FraudeDirecte join already exists ...")
except Exception as ex:
    print(ex.message)
#----------------------------------------------------------------------------------------------------------------
# PL avec BCC ouverte
try:
    if not arcpy.Exists(pl_open_bcc):
        print("Starting create PL_OpenBCC feature ...")
        create_fc_join(arcpy.env.workspace, pl_open_bcc, geometry_type_pl, pl_template_fc, has_m, has_z)
        print("PL_OpenBCC successfully created ...")
    else:
        print("PL_OpenBCC join already exists ...")
except Exception as ex:
    print(ex.message)

#----------------------------------------------------------------------------------------------------------------
# Reseau_Branchment Long
try:
    if not arcpy.Exists(ReseauLong):
        print("Starting create Reseaux_Branch_Long feature ...")
        create_fc_join(arcpy.env.workspace, ReseauLong, geometry_type_reso, reso_template_fc, has_m, has_z)
        print("Reseaux_Branch_Long successfully created ...")
    else:
        print("Reseaux_Branch_Long join already exists ...")
except Exception as ex:
    print(ex.message)

#----------------------------------------------------------------------------------------------------------------
# Supports defectueux
try:
    if not arcpy.Exists(SupportDefectueux):
        print("Starting create Supports_Defectueux feature ...")
        create_fc_join(arcpy.env.workspace, SupportDefectueux, geometry_type_pl, support_template_fc, has_m, has_z)
        print("Supports_Defectueux successfully created ...")
    else:
        print("Reseaux_Branch_Long join already exists ...")
except Exception as ex:
    print(ex.message)
