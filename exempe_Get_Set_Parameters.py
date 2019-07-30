import arcpy

# Get the feature class from the tool.
#
fc = arcpy.GetParameterAsText(0)

# Determine the shape type of the feature class.
# 
dscFC = arcpy.Describe(fc)

# Set tool output parameters based on shape type.
# 
if dscFC.ShapeType.lower() == "polygon":
    arcpy.AddMessage("Feature Type is polygon")
    arcpy.SetParameterAsText(1, "true")  # Is polygon
    arcpy.SetParameterAsText(2, "false") # Is not line
    arcpy.SetParameterAsText(3, "false") # Is not point

elif dscFC.ShapeType.lower() == "polyline":
    arcpy.AddMessage("Feature Type is polyline")
    arcpy.SetParameterAsText(1, "false") # Is not polygon
    arcpy.SetParameterAsText(2, "true")  # Is line
    arcpy.SetParameterAsText(3, "false") # Is not point

elif dscFC.ShapeType.lower() == "point":
    arcpy.AddMessage("Feature Type is point")
    arcpy.SetParameterAsText(1, "false") # Is not polygon
    arcpy.SetParameterAsText(2, "false") # Is not line
    arcpy.SetParameterAsText(3, "true")  # Is point

else:
    arcpy.AddMessage("Unknown feature type")
    arcpy.SetParameterAsText(1, "false") # Is not polygon
    arcpy.SetParameterAsText(2, "false") # Is not line
    arcpy.SetParameterAsText(3, "false") # Is not point
