import arcpy
import os

class ToolValidator(object):
    """Class for validating a tool's parameter values and controlling
    the behavior of the tool's dialog."""

    def __init__(self):
        """Setup arcpy and the list of tool parameters."""
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        return

    def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        def _generateOutputName(intable):
            if hasattr(intable, 'value'):
                intablevalue = u'{0}'.format(intable.value)
            elif isinstance(intable, arcpy.mapping.Layer):
                intablevalue = u'{0}'.format(intable.name)
            elif isinstance(intable, str) or isinstance(intable, unicode):
                intablevalue = intable
            else:
                intablevalue = u''

            # Seperate the name and path
            name = os.path.basename(intablevalue).split(".")[0]
            pth = os.path.dirname(intablevalue)

            # If input is a layer, use the layer's datasource's as the path
            if intable:
                try:
                    d = arcpy.Describe(intable)
                    if (d.dataType.lower().find("layer") != -1) or \
                       (d.dataType.lower() == "tableview"):
                        pth = os.path.dirname(d.catalogPath)

                except Exception as e:
                    pass

            d = arcpy.Describe(pth)
            if hasattr(d, 'workspaceType'):
                workspace_type = d.workspaceType
            else:
                workspace_type = None

            if arcpy.env.scratchFolder and os.path.isdir(arcpy.env.scratchFolder):
                pth = arcpy.env.scratchFolder
            elif arcpy.env.workspace:
                pth = arcpy.env.workspace
            elif workspace_type == 'RemoteDatabase':
                pth = arcpy.env.scratchFolder

            d = arcpy.Describe(pth)
            if hasattr(d, 'workspaceType'):
                workspace_type = d.workspaceType
            else:
                pth = os.path.dirname(pth)
                workspace_type = arcpy.Describe(pth).workspaceType

            if workspace_type == 'LocalDatabase':
                pth = os.path.dirname(pth)
                workspace_type = arcpy.Describe(pth).workspaceType

            # Now have path and name of outfile
            if name:
                outfile = u'{0}_TableToExcel'.format(os.path.join(pth, name))
            else:
                outfile = u'TableToExcel'

            # add extension (xls)
            ext = u'.xls'

            # if the file exists, name it _1, or _2, or _3...
            if os.path.isfile(outfile + ext):
                i = 1
                while os.path.isfile(outfile + "_" + unicode(i) + ext):
                    i += 1
                outfile = outfile + "_" + unicode(i) + ext
            else:
                outfile = outfile + ext

            return outfile

        # If the output xls hasnt been changed at all, set it to be the same
        # name as the input table
        if not self.params[1].altered:
            if self.params[0]:
                if self.params[0].value:
                    self.params[1].value = _generateOutputName(
                        self.params[0].value)

        return

    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
