import arcpy

fc = 'F:/GIS_PROJECT_GDB/COMPILE_GEODATABASE/NEWBELL/NewBell_Gathering_Compil.gdb/Reseaux'
field = "Code_Transfo"


values = [row[0] for row in arcpy.da.SearchCursor(fc, (field), 'Date_Visite is not null')]
uniqueValues = set(values)
print(uniqueValues)

