'''Exporting raster field from one file gdb and store it into a directory'''
import arcpy
import datetime
from datetime import datetime, date, time

inputfc = arcpy.GetParameterAsText(0)
rasterCol = arcpy.GetParameterAsText(1)
output_folder = arcpy.GetParameterAsText(2)
outputFC = arcpy.GetParameterAsText(3)


#Let us set the workspace into the output folder
arcpy.env.workspace = output_folder
cpt = 0
fields = arcpy.ListFields(inputfc)

filename = ''

for field in fields:
    if field.name == "Photo":
        rasterNameCol = field.name

#Let us first download rasters into the specified folder
with arcpy.da.SearchCursor(inputfc, (rasterCol, rasterNameCol, "Data_Creator", "Date_de_visite"),
                           "Date_de_visite IS NOT NULL AND Data_Creator IS NOT NULL AND " + rasterNameCol +" IS NOT NULL") as cursor:
    for row in cursor:
        suffix = datetime.strftime(row[3], '%Y-%m-%d %H:%M:%S %p')
        arcpy.AddMessage("time is {0}".format(suffix))
        suffixDate = str(suffix).replace(':', '_')
        filename = output_folder+"\\{0}.tif".format(row[2]+"_"+suffixDate)
        arcpy.AddMessage("Saving the image file {0}".format(filename))
        row[0].save(filename)
        arcpy.AddMessage("File {0} saved successfully!".format(filename))
        cpt+=1
arcpy.AddMessage("{0} picture exported successfully!".format(str(cpt)))
arcpy.AddMessage('Finished')

with arcpy.da.UpdateCursor(outputFC, [rasterCol, rasterNameCol, "Data_Creator", "Date_de_visite"],
                           "Date_de_visite IS NOT NULL AND Data_Creator LIKE 'Djoko%' AND " + rasterNameCol +" IS NULL") as cursor:
    for row in cursor :
        try:
            myFile = open(filename, 'rb').read()
            if myFile is not None:
                arcpy.AddMessage("Trying to set the value of the raster column")
                #myFile = myFile.replace(u'\0x80', ' ')
                #row[1] = myFile
                row.setValue(rasterCol, myFile)  
                cursor.updateRow(row)
                arcpy.AddMessage("Raster column as been updated successfuly!")
            
        except Exception as ex:
            arcpy.AddError("Erreur fichier {0} introuvable".format(str(filename)))

        cpt += 1

arcpy.AddMessage("Count {0} rows update successfully".format(str(cpt)))


