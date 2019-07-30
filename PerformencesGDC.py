#Generation automatique des staistiques journalières
import arcpy, os, time
from datetime import datetime, date, time
import xlrd
from xlwt import Workbook

#----------------------------------------------------------------------------------------------------------------------
now = datetime.now()
tdate = str(now.day) + str(now.month) + str(now.year) + '_' + str(now.hour) + str(now.minute) + str(now.second)

gdb = arcpy.GetParameterAsText(0)
startDate = datetime.strptime(arcpy.GetParameterAsText(1), '%d/%m/%Y')
endDate = datetime.strptime(arcpy.GetParameterAsText(2), '%d/%m/%Y')
output_file = arcpy.GetParameterAsText(3)

entities = {'PL':'PL', 'PL_Inaccessible':'PL_Inaccessible', 'Supports':'Supports', 'Eclairage_Public':'Eclairage_Public'}
performance = {}
def buildGDCList(dictionary):
	return gdc
def getPerformance(gdb, entity, beginPeriod, endPeriod, where_clause):
	fc = os.path.join(gdb, entity)
	pl_add = {}
	where_clause = ""
	visit = "Date_de_visite"
	if entity == 'PL_Inaccessible' or entity == 'Supports': 
		if entity == 'PL_Inaccessible' :
			fields = ("OBJECTID", "controleur")
		if entity == 'Supports' :
			fields = ("OBJECTID", "Data_Creator")
		visit = "Date_Visite"
	elif entity == 'PL':
		fields = ("OBJECTID", "Data_Creator", "CONTRACT_NUMBER")
		pl_add = {'contracts' : 0, 'telephones' : 0}
		where_clause = "Data_Creator IS NOT NULL"
		print fields
	else:
		fields = ("OBJECTID", "Data_Creator")
	if len(where_clause) > 1:
		where_clause = where_clause + " AND " + visit + " >= date '" + str(beginPeriod) + "' AND " + visit + " <= date '" + str(endPeriod) + "'"
	else:
		where_clause = visit + " >= date '" + str(beginPeriod) + "' AND " + visit + " <= date '" + str(endPeriod) + "'"
	performance = {}
	arcpy.AddMessage( "Calculating performances of " + str(entity) + " entity with " + where_clause)
	with arcpy.da.SearchCursor(fc, fields,  where_clause) as cursor:
		for row in cursor:
			if performance.has_key(row[1]) :
				#print "Incrementation des perf de " + str(row[1])
				temp = performance[row[1]]
				temp[entity] += 1
				if entity == 'PL' :
					if row[2] > 999 :
						temp['contracts'] += 1
				performance[row[1]] = temp	
				#performance[row[1]] += 1
			else:
				#print "Initialisation des perf de " + str(row[1])
				temp = {entity : 1}
				temp.update(pl_add)
				performance[row[1]] = temp	
	arcpy.AddMessage( "Finished.")
	return performance
def buildPerformances(gdb, entities, begin, end, where):
	arcpy.AddMessage( "Building performances for given entities...")
	performances = {}
	for key, value in entities.iteritems():
		arcpy.AddMessage( "Adding values of " + str(key) + " entity...")
		perf = getPerformance(gdb, key, begin, end, where)
		for dc, stat  in perf.iteritems():
			if performances.has_key(dc):
				performances[dc].update(stat)
			else:
				performances[dc] = stat
	arcpy.AddMessage( "Performances generated...")
	return performances
def dictToFile(dict, sheet_perf):

	#Adding headers to the sheet
	sheet_perf.write(0,0, 'DATA_CREATOR')
	sheet_perf.write(0,1, 'PL')
	sheet_perf.write(0,2, 'CONTRACTS')
	sheet_perf.write(0,3, 'TEL_NUMBERS')
	sheet_perf.write(0,4, 'PL_Inaccessibles')
	sheet_perf.write(0,5, 'ECLAIRAGE_PUBLIC')
	sheet_perf.write(0,6, 'SUPPORTS')
	arcpy.AddMessage( "Generating report file....")
	line = 1
	arcpy.AddMessage( "Starting " + str(len(dict)) + " Collectors")
	total = {}
	for col in entities.keys():
		total[col] = 0
	total['contracts'] = 0
	total['telephones'] = 0
	for key, value in dict.iteritems():
		if key != None :
			for col in entities.keys():
				if col not in value.keys():
					value[col] = 0
				con = 'contracts'
				tel = 'telephones'
				if con not in value.keys():
					value['contracts'] = 0
				if tel not in value.keys():
					value['telephones'] = 0
			sheet_perf.write(line,0, key)
			sheet_perf.write(line,1, value['PL'])
			sheet_perf.write(line,2, value['contracts'])
			sheet_perf.write(line,3, value['telephones'])
			sheet_perf.write(line,4, value['PL_Inaccessible'])
			sheet_perf.write(line,5, value['Eclairage_Public'])
			sheet_perf.write(line,6, value['Supports'])				
			line += 1
		else:
			continue
		total['PL'] += value['PL']
		total['PL_Inaccessible'] += value['PL_Inaccessible']
		total['Eclairage_Public'] += value['Eclairage_Public']
		total['Supports'] += value['Supports']
		total['contracts'] += value['contracts']
		total['telephones'] += value['telephones']
	#Adding total line
	sheet_perf.write(line,0, 'TOTAL')
	sheet_perf.write(line,1, total['PL'])
	sheet_perf.write(line,2, total['contracts'])
	sheet_perf.write(line,3, total['telephones'])
	sheet_perf.write(line,4, total['PL_Inaccessible'])
	sheet_perf.write(line,5, total['Eclairage_Public'])
	sheet_perf.write(line,6, total['Supports'])
	
	arcpy.AddMessage( "Finished " + str(len(dict)) + " Collectors")
	
	arcpy.AddMessage( "Printing output file...")
	arcpy.AddMessage( "Finished.")
	
perf = buildPerformances(gdb, entities, startDate, endDate, "")

wb = Workbook()
sheet = wb.add_sheet('Performances')
dictToFile(perf, sheet)
wb.save(output_file)

