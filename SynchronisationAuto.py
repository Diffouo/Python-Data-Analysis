import arceditor
import os
#Let us give the map

''' The map file(file.mxd link to the geodatabase.gdb save during the creation of the mobile project)'''
mxdFile = arcpy.GetParameterAsText(0)

'''The folder where the mobile cache is stored'''
folder = arcpy.GetParameterAsText(1)

def getSubDirectories(path) :
	step = 0
	jrs = ''
	arcpy.AddMessage('Count the folder cache from {0}'.format(path))
	for root, dirs, files in os.walk(path):
		step += 1
		if step == 1 :
			jrs = dirs
	arcpy.AddMessage('{0} mobile cache(s) found'.format(len(jrs)))
	return jrs
terminaux = getSubDirectories(path)
arcpy.AddMessage('Trying to Synchronize caches')
try:
	for ter in terminaux :
		path_to_cache =  path + "\\" + str(ter) + u'\Data_Gathering_Koumassi_Akwa'
		arcpy.AddMessage('Synchronizing from {0}'.format(ter))
		arcpy.SynchronizeMobileCache_mobile(v, path_to_cache, "UPLOAD_CHANGES", "NO_DOWNLOAD_CHANGES",
                                                    "PL;Eclairage_Public;PL_Inaccessible;Reseau;Supports","")
		arcpy.AddMessage('Synchronizing from {0} finished'.format(ter))
except Exception as ex:
        arcpy.AddError(ex.message)
        
arcpy.AddMessage('All cache have been synchronized')
