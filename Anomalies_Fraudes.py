# -*- coding: cp1252 -*-
import arcpy, sys, os
import codecs, array

''' The PL feature class from where abnormalities should be extraxted'''
inputPl_FC = arcpy.GetParameterAsText(0)
outputPl_FC = arcpy.GetParameterAsText(1)
excelOutput = arcpy.GetParameterAsText(2)

#Fonction qui remplace les 'é' par 'e' dans un curseur
def correct_char(value):
    rep = ''
    espion=0
    for charVal in value:
        if charVal==u'\xe9': #é : e with acute
            value =  value.replace(charVal, 'e')
        if charVal==u'\xc9': # E with acute
            print("char trouve = " + charVal)
            value =  value.replace(charVal, 'E')

        if charVal==u'\xe0': # à : a with grave
            value = value.replace(charVal, 'a')
        if charVal==u'\xe2': # a with circumflex
            value = value.replace(charVal, 'a')
        if charVal==u'\xe8': # è : e with grave
            value = value.replace(charVal, 'e')
        if charVal==u'\xb0': #Degree sign
            value = value.replace(charVal,'m')
        if charVal==u'\xf4': #ô : o with circumflex
            value = value.replace(charVal,'o')
        return value
#-----------------------------------------------------------------------------------------------------------------
# -------- Retourne le libelle de l'anomalie en fonction de son code
def getLibAnom_byCode(in_code):
    if in_code=='AN002': return 'Inaccessible'
    if in_code=='AN021': return 'Compteur bloqué'
    if in_code=='AN024': return 'Couvercle ou Vitre Percée'
    if in_code=='AN026': return 'Compteur defectueux'
    if in_code=='AN032': return 'Fraude Directe Sans Compteur'
    if in_code=='AN041': return 'Compteur Different'
    if in_code=='AN061': return 'Pl Non Trouvé'
    if in_code=='AN081': return 'Compteur a l interieur à Deplacer'
    if in_code=='AN082': return 'Compteur Expose aux Intemperies a Deplacer'
    if in_code=='AN211': return 'Pl Sans Compteur_(Volé, Detruit)'
    if in_code=='AN212': return 'Branchement Detruit'
    if in_code=='AN999': return 'Index Illisible'
    if in_code=='ANX': return 'RAS'
    if in_code=='Selectionner :': return 'RAS' #On retourne 'RAS' si aucune Anomalie n'est selectionné
#--------------------------------------------------------------------------------------------------------------
# -------- Retourne le libelle de l'activité principale en fonction de son code
def getActivitePrin_byCode(in_code):
    if in_code=='A02': return 'Antenne(Orange, MTN,Nexttel)'
    if in_code=='A03': return 'Atelier de Couture'
    if in_code=='A04': return 'Atelier de Soudure'
    if in_code=='A05': return 'Auberge'
    if in_code=='A06': return 'Bar'
    if in_code=='A08': return 'Boulangerie Complexe'
    if in_code=='A11': return 'Bureaux'
    if in_code=='A15': return 'Cybercafé'
    if in_code=='A16': return 'Administration-Commune'
    if in_code=='A18': return 'Eglise'
    if in_code=='A19': return 'Etablissement scolaire'
    if in_code=='A20': return 'Industries'
    if in_code=='A23': return 'Garage'
    if in_code=='A24': return 'Menuiserie'
    if in_code=='A26': return 'Habitation'
    if in_code=='A28': return 'Hotel-Motel'
    if in_code=='A30': return 'Imprimerie'
    if in_code=='A31': return 'Institut de beaute-Salon Coiffure'
    if in_code=='A32': return 'Laverie'
    if in_code=='A34': return 'Moulin'
    if in_code=='A36': return 'Pharmacie'
    if in_code=='A37': return 'Poissonnerie'
    if in_code=='A38': return 'Pressing'
    if in_code=='A39': return 'Restaurant'
    if in_code=='A40': return 'Salle de jeux'
    if in_code=='A43': return 'Snack bar'
    if in_code=='A44': return 'Station Service'
    if in_code=='A45': return 'Supermarche'
    if in_code=='A47': return 'Autres'
    if in_code=='A48': return 'Banques'
    if in_code=='A49': return 'Boutiques'
    if in_code=='Selectionner :': return 'No activity found'
    if in_code is None : return 'No activity found'
    
#-----------------------------------------------------------------------------------------------------------------------
# -------- Retourne le libelle de la famille d'activité en fonction de son code
def getFamilleActv_byCode(in_code):
    if in_code=='1': return 'Residence'
    if in_code=='2': return 'Commercial'
    if in_code=='3': return 'Etat'
    if in_code=='4': return 'Autre'
    if in_code=='5': return 'No family found'
#-----------------------------------------------------------------------------------------------------------------------
    # -------- Retourne le libelle de l'accessibilité compteur en fonction de son code
def getMeterAcces_byCode(in_code):
    if in_code=='1': return 'Simple'
    if in_code=='2': return 'Grille'
    if in_code=='3': return 'Inaccessible'
    if in_code=='4': return 'Index seul lisible'
    if in_code=='5': return 'Hermétiquement fermé'
#-----------------------------------------------------------------------------------------------------------------------
#-------- Update les champs des PL qui on la valeur du code par le libelle correspondant (ds la .gdb des anomalie)
def updatePL_ByLib(in_table):

    fields=("Activite_Principale", "Anomallies", "Famille_Activite", "Accessibilite_Compteur")

    cursor = arcpy.da.UpdateCursor(in_table, fields)
    cpt=0
    for row in cursor:        
        row[0] = getActivitePrin_byCode(row[0]) #---- libelle de l'activite_Principale
        row[1] = getLibAnom_byCode(row[1])      #---- libelle de l'anomalie
        row[2] = getFamilleActv_byCode(row[2])  #---- libelle de la famille d'activite
        row[3] = getMeterAcces_byCode(row[3])   #---- libelle de l'accessibilité compteur
        
        arcpy.AddMessage("Starting data update ...")
        cursor.updateRow(row)
        arcpy.AddMessage("Update done ...")
        cpt+=1
    arcpy.AddMessage("{0} rows updated = ".format(str(cpt)))
#-----------------------------------------------------------------------------------------------------------------------------------
#-------- Retourne tous les PL avec anomalie et les insere
        # dans la fc_PL (de la .gdb des anomalies)
def get_pl_anomalies(in_table, out_table, sql_condition, excelOutput): # export param is a boolean

    fields=["OBJECTID", "SHAPE", "METER_NUMBER", "CLIENT_NAME", "CONTRACT_NUMBER", "SERVICE_STATUS", "Contrat_Facture_Terrain", "Compteur_Terrain",
            "Type_Compteur", "Phasage_Compteur", "Calibre_Disjoncteur", "Reglage_Disjoncteur", "Norme_Branchement", "Index",
            "Etat_Compteur", "Activite_Principale", "Type_Construction", "Distributeur_Coffret", "Anomallies", "CCFBD", "BCC", "Famille_Activite",
            "Photo", "NB_Roues", "Compteur_Scelle", "Disjoncteur_Scelle", "Coffret_Scelle", "Visibilite_Cable",
            "Accessibilite_Compteur", "Disjoncteur", "Code_Transfo", "Date_de_visite", "Data_Creator", "Observations", "CONFIRMATION_INDEX"]

    #------------------ Traitement de la liste des champs de l'input PL feature class --------------------------------
    Fields1 = arcpy.ListFields(in_table)
    Fields2 = arcpy.ListFields(out_table)

    #fields1 = list()
    #fields2 = list()

##    for field in fields1:
##        fields1.append(field)
##        
##    for field3 in fields2:
##        fields2.append(fiel3)
        
    cursor = arcpy.da.SearchCursor(in_table, fields, sql_condition)
    cursorInsert = arcpy.da.InsertCursor(out_table, fields)
    cpt=0
    arcpy.AddMessage("Count fields = " + str(len(fields)))
    for row in cursor:
        cursorInsert.insertRow(row)
        cpt+=1

    arcpy.AddMessage("Export the result to excel ...")
    arcpy.TableToExcel_conversion(out_table, excelOutput)
    arcpy.AddMessage("Export to excel done succesfully.")                   
    arcpy.AddMessage("{0} rows inserted ".format(str(cpt)))

    #On supprime de le curseur d'insertion
    del cursorInsert
    
#-------------------------------------------------------------------------------------------------------------------------
sql_clause="(Anomallies = 'AN002' OR Anomallies = 'AN021' OR Anomallies = 'AN024' OR Anomallies = 'AN026' OR Anomallies = 'AN032' OR"
sql_clause+=" Anomallies = 'AN041' OR Anomallies = 'AN061' OR Anomallies = 'AN081' OR Anomallies = 'AN082' OR Anomallies = 'AN211' OR"
sql_clause+=" Anomallies = 'AN212' OR Anomallies = 'AN999') AND Date_de_visite IS NOT NULL"


#------------------------------- EXECUTION DES FONCTIONS

    # ... On ressort toutes les anomalies et on les insere ds la new fc_PL cree
get_pl_anomalies(inputPl_FC, outputPl_FC, sql_clause, excelOutput)

    #... Mise a jour des champs contenant le codeValue par le libValue
#updatePL_ByLib('F:/GIS_PROJECT_GDB/ANOMALIES_GDB/Gathering_anomalies_NewBell.gdb/PL')

#---------------------------------------------------------------------------------------------------------
decoding_table = (
    u'\x00'     #  0x00 -> NULL
    u'\x01'     #  0x01 -> START OF HEADING
    u'\x02'     #  0x02 -> START OF TEXT
    u'\x03'     #  0x03 -> END OF TEXT
    u'\x04'     #  0x04 -> END OF TRANSMISSION
    u'\x05'     #  0x05 -> ENQUIRY
    u'\x06'     #  0x06 -> ACKNOWLEDGE
    u'\x07'     #  0x07 -> BELL
    u'\x08'     #  0x08 -> BACKSPACE
    u'\t'       #  0x09 -> HORIZONTAL TABULATION
    u'\n'       #  0x0A -> LINE FEED
    u'\x0b'     #  0x0B -> VERTICAL TABULATION
    u'\x0c'     #  0x0C -> FORM FEED
    u'\r'       #  0x0D -> CARRIAGE RETURN
    u'\x0e'     #  0x0E -> SHIFT OUT
    u'\x0f'     #  0x0F -> SHIFT IN
    u'\x10'     #  0x10 -> DATA LINK ESCAPE
    u'\x11'     #  0x11 -> DEVICE CONTROL ONE
    u'\x12'     #  0x12 -> DEVICE CONTROL TWO
    u'\x13'     #  0x13 -> DEVICE CONTROL THREE
    u'\x14'     #  0x14 -> DEVICE CONTROL FOUR
    u'\x15'     #  0x15 -> NEGATIVE ACKNOWLEDGE
    u'\x16'     #  0x16 -> SYNCHRONOUS IDLE
    u'\x17'     #  0x17 -> END OF TRANSMISSION BLOCK
    u'\x18'     #  0x18 -> CANCEL
    u'\x19'     #  0x19 -> END OF MEDIUM
    u'\x1a'     #  0x1A -> SUBSTITUTE
    u'\x1b'     #  0x1B -> ESCAPE
    u'\x1c'     #  0x1C -> FILE SEPARATOR
    u'\x1d'     #  0x1D -> GROUP SEPARATOR
    u'\x1e'     #  0x1E -> RECORD SEPARATOR
    u'\x1f'     #  0x1F -> UNIT SEPARATOR
    u' '        #  0x20 -> SPACE
    u'!'        #  0x21 -> EXCLAMATION MARK
    u'"'        #  0x22 -> QUOTATION MARK
    u'#'        #  0x23 -> NUMBER SIGN
    u'$'        #  0x24 -> DOLLAR SIGN
    u'%'        #  0x25 -> PERCENT SIGN
    u'&'        #  0x26 -> AMPERSAND
    u"'"        #  0x27 -> APOSTROPHE
    u'('        #  0x28 -> LEFT PARENTHESIS
    u')'        #  0x29 -> RIGHT PARENTHESIS
    u'*'        #  0x2A -> ASTERISK
    u'+'        #  0x2B -> PLUS SIGN
    u','        #  0x2C -> COMMA
    u'-'        #  0x2D -> HYPHEN-MINUS
    u'.'        #  0x2E -> FULL STOP
    u'/'        #  0x2F -> SOLIDUS
    u'0'        #  0x30 -> DIGIT ZERO
    u'1'        #  0x31 -> DIGIT ONE
    u'2'        #  0x32 -> DIGIT TWO
    u'3'        #  0x33 -> DIGIT THREE
    u'4'        #  0x34 -> DIGIT FOUR
    u'5'        #  0x35 -> DIGIT FIVE
    u'6'        #  0x36 -> DIGIT SIX
    u'7'        #  0x37 -> DIGIT SEVEN
    u'8'        #  0x38 -> DIGIT EIGHT
    u'9'        #  0x39 -> DIGIT NINE
    u':'        #  0x3A -> COLON
    u';'        #  0x3B -> SEMICOLON
    u'<'        #  0x3C -> LESS-THAN SIGN
    u'='        #  0x3D -> EQUALS SIGN
    u'>'        #  0x3E -> GREATER-THAN SIGN
    u'?'        #  0x3F -> QUESTION MARK
    u'@'        #  0x40 -> COMMERCIAL AT
    u'A'        #  0x41 -> LATIN CAPITAL LETTER A
    u'B'        #  0x42 -> LATIN CAPITAL LETTER B
    u'C'        #  0x43 -> LATIN CAPITAL LETTER C
    u'D'        #  0x44 -> LATIN CAPITAL LETTER D
    u'E'        #  0x45 -> LATIN CAPITAL LETTER E
    u'F'        #  0x46 -> LATIN CAPITAL LETTER F
    u'G'        #  0x47 -> LATIN CAPITAL LETTER G
    u'H'        #  0x48 -> LATIN CAPITAL LETTER H
    u'I'        #  0x49 -> LATIN CAPITAL LETTER I
    u'J'        #  0x4A -> LATIN CAPITAL LETTER J
    u'K'        #  0x4B -> LATIN CAPITAL LETTER K
    u'L'        #  0x4C -> LATIN CAPITAL LETTER L
    u'M'        #  0x4D -> LATIN CAPITAL LETTER M
    u'N'        #  0x4E -> LATIN CAPITAL LETTER N
    u'O'        #  0x4F -> LATIN CAPITAL LETTER O
    u'P'        #  0x50 -> LATIN CAPITAL LETTER P
    u'Q'        #  0x51 -> LATIN CAPITAL LETTER Q
    u'R'        #  0x52 -> LATIN CAPITAL LETTER R
    u'S'        #  0x53 -> LATIN CAPITAL LETTER S
    u'T'        #  0x54 -> LATIN CAPITAL LETTER T
    u'U'        #  0x55 -> LATIN CAPITAL LETTER U
    u'V'        #  0x56 -> LATIN CAPITAL LETTER V
    u'W'        #  0x57 -> LATIN CAPITAL LETTER W
    u'X'        #  0x58 -> LATIN CAPITAL LETTER X
    u'Y'        #  0x59 -> LATIN CAPITAL LETTER Y
    u'Z'        #  0x5A -> LATIN CAPITAL LETTER Z
    u'['        #  0x5B -> LEFT SQUARE BRACKET
    u'\\'       #  0x5C -> REVERSE SOLIDUS
    u']'        #  0x5D -> RIGHT SQUARE BRACKET
    u'^'        #  0x5E -> CIRCUMFLEX ACCENT
    u'_'        #  0x5F -> LOW LINE
    u'`'        #  0x60 -> GRAVE ACCENT
    u'a'        #  0x61 -> LATIN SMALL LETTER A
    u'b'        #  0x62 -> LATIN SMALL LETTER B
    u'c'        #  0x63 -> LATIN SMALL LETTER C
    u'd'        #  0x64 -> LATIN SMALL LETTER D
    u'e'        #  0x65 -> LATIN SMALL LETTER E
    u'f'        #  0x66 -> LATIN SMALL LETTER F
    u'g'        #  0x67 -> LATIN SMALL LETTER G
    u'h'        #  0x68 -> LATIN SMALL LETTER H
    u'i'        #  0x69 -> LATIN SMALL LETTER I
    u'j'        #  0x6A -> LATIN SMALL LETTER J
    u'k'        #  0x6B -> LATIN SMALL LETTER K
    u'l'        #  0x6C -> LATIN SMALL LETTER L
    u'm'        #  0x6D -> LATIN SMALL LETTER M
    u'n'        #  0x6E -> LATIN SMALL LETTER N
    u'o'        #  0x6F -> LATIN SMALL LETTER O
    u'p'        #  0x70 -> LATIN SMALL LETTER P
    u'q'        #  0x71 -> LATIN SMALL LETTER Q
    u'r'        #  0x72 -> LATIN SMALL LETTER R
    u's'        #  0x73 -> LATIN SMALL LETTER S
    u't'        #  0x74 -> LATIN SMALL LETTER T
    u'u'        #  0x75 -> LATIN SMALL LETTER U
    u'v'        #  0x76 -> LATIN SMALL LETTER V
    u'w'        #  0x77 -> LATIN SMALL LETTER W
    u'x'        #  0x78 -> LATIN SMALL LETTER X
    u'y'        #  0x79 -> LATIN SMALL LETTER Y
    u'z'        #  0x7A -> LATIN SMALL LETTER Z
    u'{'        #  0x7B -> LEFT CURLY BRACKET
    u'|'        #  0x7C -> VERTICAL LINE
    u'}'        #  0x7D -> RIGHT CURLY BRACKET
    u'~'        #  0x7E -> TILDE
    u'\x7f'     #  0x7F -> DELETE
    u'\u20ac'   #  0x80 -> EURO SIGN
    u'\ufffe'   #  0x81 -> UNDEFINED
    u'\u201a'   #  0x82 -> SINGLE LOW-9 QUOTATION MARK
    u'\u0192'   #  0x83 -> LATIN SMALL LETTER F WITH HOOK
    u'\u201e'   #  0x84 -> DOUBLE LOW-9 QUOTATION MARK
    u'\u2026'   #  0x85 -> HORIZONTAL ELLIPSIS
    u'\u2020'   #  0x86 -> DAGGER
    u'\u2021'   #  0x87 -> DOUBLE DAGGER
    u'\u02c6'   #  0x88 -> MODIFIER LETTER CIRCUMFLEX ACCENT
    u'\u2030'   #  0x89 -> PER MILLE SIGN
    u'\u0160'   #  0x8A -> LATIN CAPITAL LETTER S WITH CARON
    u'\u2039'   #  0x8B -> SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    u'\u0152'   #  0x8C -> LATIN CAPITAL LIGATURE OE
    u'\ufffe'   #  0x8D -> UNDEFINED
    u'\u017d'   #  0x8E -> LATIN CAPITAL LETTER Z WITH CARON
    u'\ufffe'   #  0x8F -> UNDEFINED
    u'\ufffe'   #  0x90 -> UNDEFINED
    u'\u2018'   #  0x91 -> LEFT SINGLE QUOTATION MARK
    u'\u2019'   #  0x92 -> RIGHT SINGLE QUOTATION MARK
    u'\u201c'   #  0x93 -> LEFT DOUBLE QUOTATION MARK
    u'\u201d'   #  0x94 -> RIGHT DOUBLE QUOTATION MARK
    u'\u2022'   #  0x95 -> BULLET
    u'\u2013'   #  0x96 -> EN DASH
    u'\u2014'   #  0x97 -> EM DASH
    u'\u02dc'   #  0x98 -> SMALL TILDE
    u'\u2122'   #  0x99 -> TRADE MARK SIGN
    u'\u0161'   #  0x9A -> LATIN SMALL LETTER S WITH CARON
    u'\u203a'   #  0x9B -> SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    u'\u0153'   #  0x9C -> LATIN SMALL LIGATURE OE
    u'\ufffe'   #  0x9D -> UNDEFINED
    u'\u017e'   #  0x9E -> LATIN SMALL LETTER Z WITH CARON
    u'\u0178'   #  0x9F -> LATIN CAPITAL LETTER Y WITH DIAERESIS
    u'\xa0'     #  0xA0 -> NO-BREAK SPACE
    u'\xa1'     #  0xA1 -> INVERTED EXCLAMATION MARK
    u'\xa2'     #  0xA2 -> CENT SIGN
    u'\xa3'     #  0xA3 -> POUND SIGN
    u'\xa4'     #  0xA4 -> CURRENCY SIGN
    u'\xa5'     #  0xA5 -> YEN SIGN
    u'\xa6'     #  0xA6 -> BROKEN BAR
    u'\xa7'     #  0xA7 -> SECTION SIGN
    u'\xa8'     #  0xA8 -> DIAERESIS
    u'\xa9'     #  0xA9 -> COPYRIGHT SIGN
    u'\xaa'     #  0xAA -> FEMININE ORDINAL INDICATOR
    u'\xab'     #  0xAB -> LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\xac'     #  0xAC -> NOT SIGN
    u'\xad'     #  0xAD -> SOFT HYPHEN
    u'\xae'     #  0xAE -> REGISTERED SIGN
    u'\xaf'     #  0xAF -> MACRON
    u'\xb0'     #  0xB0 -> DEGREE SIGN
    u'\xb1'     #  0xB1 -> PLUS-MINUS SIGN
    u'\xb2'     #  0xB2 -> SUPERSCRIPT TWO
    u'\xb3'     #  0xB3 -> SUPERSCRIPT THREE
    u'\xb4'     #  0xB4 -> ACUTE ACCENT
    u'\xb5'     #  0xB5 -> MICRO SIGN
    u'\xb6'     #  0xB6 -> PILCROW SIGN
    u'\xb7'     #  0xB7 -> MIDDLE DOT
    u'\xb8'     #  0xB8 -> CEDILLA
    u'\xb9'     #  0xB9 -> SUPERSCRIPT ONE
    u'\xba'     #  0xBA -> MASCULINE ORDINAL INDICATOR
    u'\xbb'     #  0xBB -> RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\xbc'     #  0xBC -> VULGAR FRACTION ONE QUARTER
    u'\xbd'     #  0xBD -> VULGAR FRACTION ONE HALF
    u'\xbe'     #  0xBE -> VULGAR FRACTION THREE QUARTERS
    u'\xbf'     #  0xBF -> INVERTED QUESTION MARK
    u'\xc0'     #  0xC0 -> LATIN CAPITAL LETTER A WITH GRAVE
    u'\xc1'     #  0xC1 -> LATIN CAPITAL LETTER A WITH ACUTE
    u'\xc2'     #  0xC2 -> LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    u'\xc3'     #  0xC3 -> LATIN CAPITAL LETTER A WITH TILDE
    u'\xc4'     #  0xC4 -> LATIN CAPITAL LETTER A WITH DIAERESIS
    u'\xc5'     #  0xC5 -> LATIN CAPITAL LETTER A WITH RING ABOVE
    u'\xc6'     #  0xC6 -> LATIN CAPITAL LETTER AE
    u'\xc7'     #  0xC7 -> LATIN CAPITAL LETTER C WITH CEDILLA
    u'\xc8'     #  0xC8 -> LATIN CAPITAL LETTER E WITH GRAVE
    u'\xc9'     #  0xC9 -> LATIN CAPITAL LETTER E WITH ACUTE
    u'\xca'     #  0xCA -> LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    u'\xcb'     #  0xCB -> LATIN CAPITAL LETTER E WITH DIAERESIS
    u'\xcc'     #  0xCC -> LATIN CAPITAL LETTER I WITH GRAVE
    u'\xcd'     #  0xCD -> LATIN CAPITAL LETTER I WITH ACUTE
    u'\xce'     #  0xCE -> LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    u'\xcf'     #  0xCF -> LATIN CAPITAL LETTER I WITH DIAERESIS
    u'\xd0'     #  0xD0 -> LATIN CAPITAL LETTER ETH
    u'\xd1'     #  0xD1 -> LATIN CAPITAL LETTER N WITH TILDE
    u'\xd2'     #  0xD2 -> LATIN CAPITAL LETTER O WITH GRAVE
    u'\xd3'     #  0xD3 -> LATIN CAPITAL LETTER O WITH ACUTE
    u'\xd4'     #  0xD4 -> LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    u'\xd5'     #  0xD5 -> LATIN CAPITAL LETTER O WITH TILDE
    u'\xd6'     #  0xD6 -> LATIN CAPITAL LETTER O WITH DIAERESIS
    u'\xd7'     #  0xD7 -> MULTIPLICATION SIGN
    u'\xd8'     #  0xD8 -> LATIN CAPITAL LETTER O WITH STROKE
    u'\xd9'     #  0xD9 -> LATIN CAPITAL LETTER U WITH GRAVE
    u'\xda'     #  0xDA -> LATIN CAPITAL LETTER U WITH ACUTE
    u'\xdb'     #  0xDB -> LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    u'\xdc'     #  0xDC -> LATIN CAPITAL LETTER U WITH DIAERESIS
    u'\xdd'     #  0xDD -> LATIN CAPITAL LETTER Y WITH ACUTE
    u'\xde'     #  0xDE -> LATIN CAPITAL LETTER THORN
    u'\xdf'     #  0xDF -> LATIN SMALL LETTER SHARP S
    u'\xe0'     #  0xE0 -> LATIN SMALL LETTER A WITH GRAVE
    u'\xe1'     #  0xE1 -> LATIN SMALL LETTER A WITH ACUTE
    u'\xe2'     #  0xE2 -> LATIN SMALL LETTER A WITH CIRCUMFLEX
    u'\xe3'     #  0xE3 -> LATIN SMALL LETTER A WITH TILDE
    u'\xe4'     #  0xE4 -> LATIN SMALL LETTER A WITH DIAERESIS
    u'\xe5'     #  0xE5 -> LATIN SMALL LETTER A WITH RING ABOVE
    u'\xe6'     #  0xE6 -> LATIN SMALL LETTER AE
    u'\xe7'     #  0xE7 -> LATIN SMALL LETTER C WITH CEDILLA
    u'\xe8'     #  0xE8 -> LATIN SMALL LETTER E WITH GRAVE
    u'\xe9'     #  0xE9 -> LATIN SMALL LETTER E WITH ACUTE
    u'\xea'     #  0xEA -> LATIN SMALL LETTER E WITH CIRCUMFLEX
    u'\xeb'     #  0xEB -> LATIN SMALL LETTER E WITH DIAERESIS
    u'\xec'     #  0xEC -> LATIN SMALL LETTER I WITH GRAVE
    u'\xed'     #  0xED -> LATIN SMALL LETTER I WITH ACUTE
    u'\xee'     #  0xEE -> LATIN SMALL LETTER I WITH CIRCUMFLEX
    u'\xef'     #  0xEF -> LATIN SMALL LETTER I WITH DIAERESIS
    u'\xf0'     #  0xF0 -> LATIN SMALL LETTER ETH
    u'\xf1'     #  0xF1 -> LATIN SMALL LETTER N WITH TILDE
    u'\xf2'     #  0xF2 -> LATIN SMALL LETTER O WITH GRAVE
    u'\xf3'     #  0xF3 -> LATIN SMALL LETTER O WITH ACUTE
    u'\xf4'     #  0xF4 -> LATIN SMALL LETTER O WITH CIRCUMFLEX
    u'\xf5'     #  0xF5 -> LATIN SMALL LETTER O WITH TILDE
    u'\xf6'     #  0xF6 -> LATIN SMALL LETTER O WITH DIAERESIS
    u'\xf7'     #  0xF7 -> DIVISION SIGN
    u'\xf8'     #  0xF8 -> LATIN SMALL LETTER O WITH STROKE
    u'\xf9'     #  0xF9 -> LATIN SMALL LETTER U WITH GRAVE
    u'\xfa'     #  0xFA -> LATIN SMALL LETTER U WITH ACUTE
    u'\xfb'     #  0xFB -> LATIN SMALL LETTER U WITH CIRCUMFLEX
    u'\xfc'     #  0xFC -> LATIN SMALL LETTER U WITH DIAERESIS
    u'\xfd'     #  0xFD -> LATIN SMALL LETTER Y WITH ACUTE
    u'\xfe'     #  0xFE -> LATIN SMALL LETTER THORN
    u'\xff'     #  0xFF -> LATIN SMALL LETTER Y WITH DIAERESIS
)
