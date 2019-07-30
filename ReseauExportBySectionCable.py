import arcpy

stat = 0
fields = ["SHAPE@LENGTH", "Code_Transfo"]
where_clause  = "Section_Cable LIKE '3x70mm%' AND Code_Transfo = '822110201'"
method = True

print("Starting the process ...")
with arcpy.da.SearchCursor("F:/GIS_PROJECT_GDB/COMPILE_POSTES_TERMINES/Compilcomplete_Update/NewBell_Gathering_Compil.gdb/Reseaux", fields, where_clause) as cursor:
    stat = 0
    for row in cursor:
        print("current lenght = " + str(row[0]))
        if method :
            add = row[0]
        else :
            add = 1
        print("------------------------------------------------------------")
        print("Incrementing the lenght")
        stat += add
print("Resultat des statistiques. Longueur du reseau 822110201 = " + str(stat))
