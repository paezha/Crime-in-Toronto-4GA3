import arcpy as ap
ap.env.overwriteOutput = True

census = "C:/ENVSOCTY 4GA3 Group Project/ENVSOCTY 4GA3 Group Project/CensusData.shp"
crimes = "C:/ENVSOCTY 4GA3 Group Project/Major_Crime_Indicators_Open_Data/Major_Crime_Indicators_Open_Data.shp"
out_path = "C:/ENVSOCTY 4GA3 Group Project/ENVSOCTY 4GA3 Group Project/ENVSOCTY 4GA3 Group Project.gdb"

crimes_2016 = ap.SelectLayerByAttribute_management(crimes, 'NEW_SELECTION', '"OCC_YEAR" = 2016')

sql_exp = "MCI_CATEGO = 'Robbery' OR MCI_CATEGO = 'Auto Theft' OR MCI_CATEGO = 'Break and Enter' OR MCI_CATEGO = 'Theft Over'"

crimes_2016 = ap.SelectLayerByAttribute_management(crimes_2016, 'ADD_TO_SELECTION', sql_exp)

crime_buffer = ap.Buffer_analysis(crimes_2016, out_path + '/CrimeBuffer', '5 meters')

ap.AddMessage('Crime buffers created.')

crime_types = ['Robbery', 'Auto Theft', 'Break and Enter', 'Theft Over']
field_names = []
for type in crime_types:
    field_name = ap.ValidateFieldName(type)
    field_names.append(field_name)
    ap.AddField_management(crime_buffer, field_name, 'SHORT', field_alias=type)
    with ap.da.UpdateCursor(crime_buffer, ['MCI_CATEGO', field_name]) as cursor:
        for row in cursor:
            if row[0] == type:
                row[1] = 1
            else:
                row[1] = 0
            cursor.updateRow(row)

ap.AddMessage('Crime count columns created.')

crime_by_CT = ap.ApportionPolygon_analysis(crime_buffer, field_names, census, out_path + '/CrimebyCT')

ap.AddMessage('Apportioned polygon created.')

ap.AddField_management(crime_by_CT, 'Income', 'LONG')
ap.AddField_management(crime_by_CT, 'Population', 'LONG')
ap.AddField_management(crime_by_CT, 'Unemployment', 'DOUBLE')

ap.AddMessage('Field names changed.')

with ap.da.UpdateCursor(crime_by_CT, ['vAtiohi2_', 'Income', 'v_CA1Ur', 'Unemployment', 'v_CA1P2', 'Population']) as cursor:
    for row in cursor:
        row[1] = row[0]
        row[3] = row[2]
        row[5] = row[4]
        cursor.updateRow(row)

ap.DeleteField_management(crime_by_CT, 'vAtiohi2_')
ap.DeleteField_management(crime_by_CT, 'v_CA1Ur')
ap.DeleteField_management(crime_by_CT, 'v_CA1P2')

ap.ExportFeatures_conversion(crime_by_CT, 'C:/ENVSOCTY 4GA3 Group Project/Census Crimes Shapefile/CrimesbyCT.shp')
