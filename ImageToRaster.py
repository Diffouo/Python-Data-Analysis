import arcpy
import datetime
from datetime import datetime, date, time

input_folder = arcpy.GetParameterAsText(0)
inputfc = arcpy.GetParameterAsText(1)
rasterCol = arcpy.GetParameterAsText(2)

#Let us set the workspace into the output folder
arcpy.env.workspace = input_folder
cpt = 0
fields = arcpy.ListFields(inputfc)

for field in fields:
    if field.name == "Photo":
        rasterNameCol = field.name

#Then let us upload files into the blob column of the consolidated .gdb

with arcpy.da.UpdateCursor(inputfc, [rasterCol, rasterNameCol, "Data_Creator", "Date_de_visite"],
                           "Date_de_visite IS NOT NULL AND Data_Creator LIKE 'Djoko%' AND " + rasterNameCol +" IS NULL") as cursor:
    for row in cursor :
        suffix = datetime.strftime(row[3], '%Y-%m-%d %H:%M:%S %p')
        arcpy.AddMessage("time is {0}".format(suffix))
        suffixDate = str(suffix).replace(':', '_')

        filename = input_folder+"\\{0}.tif".format(row[2]+"_"+suffixDate)
        #filename = input_folder+"\\{0}.tif".format((row[2]).strip()+"_"+suffixDate)
        #filename = str(filename).replace(u'\0x80', ' ')
        arcpy.AddMessage("Trying to read the image file {0}".format(filename))

        try:
            myFile = open(filename, 'rb').read()
            if myFile is not None:
                arcpy.AddMessage("Trying to set the value of the raster column")
                #myFile = myFile.replace(u'\0x80', ' ')
                row[1] = myFile
                row.setValue(myFile)  
                cursor.updateRow(row)
                arcpy.AddMessage("Raster column as been updated successfuly!")
            
        except Exception as ex:
            arcpy.AddError("Erreur fichier {0} introuvable".format(str(filename)))

        cpt += 1

arcpy.AddMessage("Count {0} rows update successfully".format(str(cpt)))
