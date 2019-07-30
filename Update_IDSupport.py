# -*- coding: cp1252 -*-
import arcpy

#-------- Update les ID_Support pour que les valeurs puissent etre unique
def update_IDSupport(in_table, sqlClause):

    fields=("ID_Support")
    workspace = 'F:/Douala/Data_gathering/Gathring.gdb'
    
    # Open an edit session and start an edit operation
    with arcpy.da.Editor(workspace) as edit:
        
        cursor = arcpy.da.UpdateCursor(in_table, fields, sqlClause)
        cpt=1
        newVal = ""
        for row in cursor:
            if len(str(cpt))==1:
                newVal = row[0] + "000" + str(cpt)
            elif len(str(cpt))==2:
                newVal = row[0] + "00" + str(cpt)
            elif len(str(cpt))==3:
                newVal = row[0] + "0" + str(cpt)
            elif len(str(cpt))==4:
                newVal = row[0] + str(cpt)

            print("Old value = " + str(row[0]))
            row[0]=newVal
            print("New value = " + newVal)
            print("Starting data update ...")
            cursor.updateRow(row)
            print("Update done ...")
            cpt+=1
        print("Rows updated = " + str(cpt))

update_IDSupport(r'F:/Douala/Data_gathering/Gathring.gdb/Supports', "ID_Support like '8221307%'")

##print("Lancement du tri")
##arcpy.Sort_management("BT_Model_Project/Supports", "Supports_Sort", [["Date_Visite", "ASCENDING"]])
##print("Fin du tri")
