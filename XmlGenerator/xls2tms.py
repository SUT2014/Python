#!/usr/bin/python
# Description: python script to generate segment and campaign xmls direct from excel xlsx sheets.
# Written by: KD

import sys
import os
import subprocess
from time import strftime
import xlrd
import unicodedata

ATTRIBUTE = 'Attribute ID'
SEGMENT = 'Segment'
CAMPAIGN = 'Matched'
ASSET = 'Campaign ID'
ASSET_TAB = 'Asset List'
CA_OFFSET = 304

# Asset details data structure 
# to be maintained for all known campaign assets
# key = CampaignId+Asset Variant+AssetID
# value tuple is : 'duration','content instance reference','encoding reference'
#
ASSET_DETAILS = {'502SDSD10':('30', 'SD_CI_03', '71312384'),
                 '502HDHD10':('30', 'HD_CI_03', '616580096'),
				 '5023/4 SDTQSD10':('30', '34SD_CI_03', '88089600'),
				 '503SDSD11':('30', 'SD_CI_04', '71312384'),
				}

def log_line():
    f = open('xls2tms.log', 'a')
    f.write(strftime("%Y-%m-%d %H:%M:%S") + ' ' + os.getlogin() + ' ' + ' '.join(sys.argv) + '\n')
    f.close()

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
			
def print_usage():
    print 'xls2tms.py is a tool to generate TMS test data from a test plan xls sheet'
    print 'The xls data sheet can be found in the TMS testcase folder on sharepoint'
    print 'usage: xls2tms.py <xls file, *.xls, *.xlsx>'
	
def p_prof_xml_header(f):
    f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
		
def p_prof_xml_header(f):
    f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
		
def p_prof_xml_profile_tms(f, id, expression):
    f.write('<TargetProfile name="segment' + id + '" xmlns="urn:nds:dyn:profile:targetprofile:version01" xmlns:attribute="urn:nds:dyn:profile:attribute:version01" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
    f.write('<Expression> <![CDATA[' + expression + ']]> </Expression>\n')
    f.write('<Description>profile' + id + '</Description>\n')
    f.write('</TargetProfile>\n')
		
def p_prof_xml_ca_attribute(f, name, min_val, max_val, num_bits, bit_offset):
    f.write('<Attribute name="' + name + '" xmlns="urn:nds:dyn:profile:attribute:version01" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
    f.write('  <DataType>\n')
    f.write('    <EnumData userDefined="true">\n')
    f.write('    <member value="' + min_val + '" name="Min"/>\n')
    f.write('    <member value="' + max_val + '" name="Max"/>\n')
    f.write('    </EnumData>\n')
    f.write('  </DataType>\n')
    f.write('  <LocatorType>\n')
    f.write('    <CAAttributeLocator>\n')
    f.write('      <PersonalBits numBits="' + num_bits  +'" bitOffset="' + bit_offset + '"/>\n')
    f.write('    </CAAttributeLocator>\n')
    f.write('  </LocatorType>\n')
    f.write(' <Description>' + name +  '</Description>\n')
    f.write('</Attribute>\n')

def p_prof_xml_he_attribute(f, name, min_val, max_val, defaultValue):
    f.write('<Attribute name="' + name + '" xmlns="urn:nds:dyn:profile:attribute:version01" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
    f.write('  <DataType>\n')
    if defaultValue == 'TRUE' or defaultValue == 'FALSE':
	f.write('    <BooleanData userDefined="true">\n')
	f.write('    <member value="FALSE" name="FALSE"/>\n')
	f.write('    <member value="TRUE" name="TRUE"/>\n')
	f.write('    </BooleanData>\n')
    else:
        if (max_val == '65535' or max_val == '4294967295'):
             f.write('    <IntegerData userDefined="true">\n')
             f.write('    <member value="' + min_val + '" name="Min"/>\n')
             f.write('    <member value="' + max_val + '" name="Max"/>\n')
             f.write('    </IntegerData>\n')
        else:
	     f.write('    <EnumData userDefined="true">\n')
	     f.write('    <member value="' + min_val + '" name="Min"/>\n')
	     f.write('    <member value="' + max_val + '" name="Max"/>\n')
	     f.write('    </EnumData>\n')
    f.write('  </DataType>\n')
    f.write('  <LocatorType>\n')
    f.write('    <HEAttributeLocator defaultValue="'+ defaultValue+ '"/>\n')
    f.write('  </LocatorType>\n')
    f.write(' <Description>' + name +  '</Description>\n')
    f.write('</Attribute>\n')

def do_set_campaign(f,campaign):
    """ set a campaign, internal interface """
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<campaign\n')
    f.write('       handle="' + 'C' + str(campaign['campaignId']) + '"\n')
    f.write('       campaignId="' + campaign['campaignId'] + '"\n')
    f.write('       campaignType="Substitution"\n')
    f.write('       startDateTime="' + campaign['startDateTime'] + '"\n')
    f.write('       endDateTime="' + campaign['endDateTime'] + '"\n')
    f.write('       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
    f.write('       xmlns="urn:nds:dyn:campaign:version' + campaign['version']  + '"\n')
    f.write('       maxImpressions="' + campaign['maxImpressions'] + '"\n')
    f.write('       maxImpressionsInTimePeriod="' + campaign['maxImpressionsInTimePeriod'] + '"\n')
    f.write('       timePeriodInDays="' + campaign['timePeriodInDays'] + '"\n')
    f.write('       separation="' + campaign['separation'] + '" >\n')

    for i in range(0, int(campaign['numTargetProfiles'])):
        ts = 'targetProfileName' + str(i)
        f.write('       <targetProfileName>' + str(campaign[ts]) + '</targetProfileName>\n');

    f.write('       <adContent vamAssetHandle="' + campaign['vamAssetHandle'] + '">\n')
    f.write('       <adId adId="' + campaign['adId'] + '" idNamespace="urn:nds:dynamic:assetIdNamespace:vamAssetId" />\n')

    for i in range(0, int(campaign['numContentInstances'])):
        ts = 'contentInstance' + str(i)
        f.write('               <contentInstance xsi:type="AVInstanceType"\n' )
        f.write('                       durationSeconds="' + campaign[ts]['durationSeconds'] + '"\n');
        f.write('                       durationFrames="' + campaign[ts]['durationFrames'] + '"\n');
        f.write('                       framesPerSecond="' + campaign[ts]['framesPerSecond'] + '">\n');
        f.write('                       <contentInstanceRef>' + campaign[ts]['contentInstanceRef'] + '</contentInstanceRef>\n')
        f.write('                       <encodingProfile>' + campaign[ts]['encodingProfile'] + '</encodingProfile>\n')
        f.write('               </contentInstance>\n')

    f.write('       </adContent>\n')
    if campaign['noBARB'] == '1':
        f.write('        <operatorSignaling>1000000</operatorSignaling>\n' )

    f.write('</campaign>\n')
    f.close()	

def find_row_col(workbook,worksheet_name,field_name):
    worksheet = workbook.sheet_by_name(worksheet_name)
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = -1
    while curr_row < num_rows:
	    curr_row += 1
	    curr_cell=-1
	    while curr_cell < num_cells:
		    curr_cell += 1
		    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
		    cell_type = worksheet.cell_type(curr_row, curr_cell)
		    if (cell_type == 2):
       		        cell_value = str(int(worksheet.cell_value(curr_row, curr_cell))).strip().lower()
		    else:
                        cell_value = str(worksheet.cell_value(curr_row, curr_cell)).strip().lower()
	            
		    if(cell_value == field_name.lower()):
	                return (curr_row, curr_cell)
    return(-1,-1)
				
def handle_adt_sheet(workbook,worksheet_name):
    print 'working on adt sheet'
    (row,col) = find_row_col(workbook,worksheet_name,ATTRIBUTE)
    if (row == -1):
        print 'Error processing ',worksheet_name,'page..returning'
        return
    # sheet has attribute information, process 
    worksheet = workbook.sheet_by_name(worksheet_name)
    num_rows = worksheet.nrows - 1
    bit_offset = CA_OFFSET
    # create directory with worksheet name
    if not os.path.exists(worksheet_name.strip()):
       os.mkdir(worksheet_name.strip())
    while row < num_rows:
        row += 1
	#read a row of data
	attribute_name = str(worksheet.cell_value(row,col))
	ca_he = worksheet.cell_value(row,col+1)
        min_value = worksheet.cell_value(row,col+2)
        min_value_desc = worksheet.cell_value(row,col+3)
	max_value = worksheet.cell_value(row,col+4)
        max_value_desc = worksheet.cell_value(row,col+5)
        attribute_type = worksheet.cell_value(row,col+6)
	attribute_name = attribute_name.strip()
        f = open(worksheet_name.strip()+'/'+attribute_name + '.xml', 'w');
        p_prof_xml_header(f)
        if (max_value == 1):
            num_bits = 1
        if (max_value == 3):
            num_bits = 2
        if (max_value == 7):
            num_bits = 3	
        if (max_value == 15):
            num_bits = 4
        if (max_value == 31):
            num_bits = 5
        if (max_value == 65536):
            num_bits = 16
        if (max_value == 4294967295):
            num_bits = 32
	# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
	if (worksheet.cell_type(row,col+2) == 4):
	    if min_value == 0:
                min_value_desc = 'FALSE'
            else:
	        min_value_desc = 'TRUE'
	if (ca_he.find('CA') != -1):
            p_prof_xml_ca_attribute(f, attribute_name, str(int(min_value)), str(int(max_value)), str(num_bits), str(bit_offset))
            bit_offset += num_bits
        else:
            p_prof_xml_he_attribute(f, attribute_name, str(int(min_value)), str(int(max_value)), str(min_value_desc).strip())
        f.close()

def get_assets(campaign,workbook,asset_id):
    worksheet = workbook.sheet_by_name(ASSET_TAB)
    num_rows = worksheet.nrows - 1
    (row,col) = find_row_col(workbook,ASSET_TAB,asset_id)
    if (row == -1):
        print 'Error processing ',ASSET_TAB,'asset not found',asset_id
        return
    # merged cells not working on this library, so, use the age old technique
    # browse through rows 
    iter=0
    while (row < num_rows):
        (duration,contentInstanceRef,encodingProfile) = ASSET_DETAILS[asset_id+worksheet.cell_value(row,col+1).strip()+worksheet.cell_value(row,col+2).strip()]
        campaign['contentInstance' + str(iter)]['durationSeconds'] = duration
        campaign['contentInstance' + str(iter)]['durationFrames'] = '0';
        campaign['contentInstance' + str(iter)]['framesPerSecond'] = '25Frames';
        campaign['contentInstance' + str(iter)]['contentInstanceRef'] = contentInstanceRef
        campaign['contentInstance' + str(iter)]['encodingProfile'] = encodingProfile
        row += 1
        iter += 1
        if (worksheet.cell_type(row,col) == 2): #empty
            break
    campaign['numContentInstances'] = str(iter)    

    return
		
def handle_campaigns(workbook,worksheet_name):
    (row,col) = find_row_col(workbook,worksheet_name,CAMPAIGN)
    if (row == -1):
        print 'Error processing ',worksheet_name,'page..returning'
        return
	# sheet has campaign information, process 
    worksheet = workbook.sheet_by_name(worksheet_name)
    num_rows = worksheet.nrows - 1
    campaign = AutoVivification()
    # create directory with worksheet name
    if not os.path.exists(worksheet_name):
        os.mkdir(worksheet_name)
    while row < num_rows:
        row += 1
        campaign['campaignId'] = str(int(worksheet.cell_value(row,col+2))).strip()
        campaign['startDateTime'] = '2010-08-10T06:00:00';
        campaign['endDateTime']   = '2020-12-30T23:59:59';
        campaign['version'] = str(int(worksheet.cell_value(row,col+1))).strip();
        campaign['maxImpressions'] = '10'
        campaign['maxImpressionsInTimePeriod'] = str(int(worksheet.cell_value(row,col+5))).strip()
        campaign['timePeriodInDays'] = '1';
        campaign['separation'] = str(int(worksheet.cell_value(row,col+6))).strip()
        campaign['numTargetProfiles'] = '1';
        campaign['targetProfileName0'] = 'segment'+str(int(worksheet.cell_value(row,col+3))).strip()
        campaign['vamAssetHandle'] = 'ASSET' + str(int(worksheet.cell_value(row,col+2))).strip()
        campaign['adId'] = 'ADID_' + str(int(worksheet.cell_value(row,col+2))).strip()
        campaign['noBARB'] = '0'
        get_assets(campaign,workbook,str(int(worksheet.cell_value(row,col+2))).strip())
        file_name = worksheet_name.strip()+'/'+'auto_campaign_' + str(campaign['campaignId']) + '.xml'
        f = open(file_name, 'w')
        do_set_campaign(f,campaign)
		
        
	
def handle_campaign_sheet(workbook,worksheet_name):
    print 'working on campaign sheet'
    (row,col) = find_row_col(workbook,worksheet_name,SEGMENT)
    if (row == -1):
        print 'Error processing ',worksheet_name,'page..returning'
        return
    # sheet has segment information, process 
    worksheet = workbook.sheet_by_name(worksheet_name)
    num_rows = worksheet.nrows - 1
    # create directory with worksheet name
    if not os.path.exists(worksheet_name):
        os.mkdir(worksheet_name)
    while row < num_rows:
        row += 1
        #read a row of data
        segment_id = str(int(worksheet.cell_value(row,col))).strip()
        expression = str(worksheet.cell_value(row,col+2)).strip()
        name = 'segment' + segment_id
        f = open(worksheet_name.strip()+'/'+'auto_' + name + '.xml', 'w');
        p_prof_xml_header(f)
        p_prof_xml_profile_tms(f, segment_id, expression)
        f.close()
	#pass on control to create manifests
	handle_campaigns(workbook,worksheet_name)
	

def main():
	log_line()
	if (len(sys.argv) < 2):
		print_usage()
		return
	workbook = xlrd.open_workbook(sys.argv[1])
	worksheets = workbook.sheet_names()
	for worksheet_name in worksheets:
		temp = worksheet_name.lower()
		if (temp.find('adt') != -1):
			handle_adt_sheet(workbook,worksheet_name)
		if (temp.find('campaign') != -1):
			handle_campaign_sheet(workbook,worksheet_name)

if __name__ == "__main__":
    main()
