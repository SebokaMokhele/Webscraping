
from bs4 import BeautifulSoup
import requests
import xlsxwriter
import re

#------------------------------------------
# A request to university and college page
#------------------------------------------
State_colleges = requests.get('https://www.ugc.ac.in/stateuniversity.aspx').text
#print(State_colleges)
soup = BeautifulSoup(State_colleges, 'lxml')

#------------------------------------------------
# Find states of universities and colleges page
#------------------------------------------------
findstates = soup.find('ul', class_ = 'links-ul')


#----------------------------------------------------------
#In order to print college information to spreadsheet
#First let us define xlsx (ext. for excel) writer
#----------------------------------------------------------

#create excel file
workbook = xlsxwriter.Workbook('Col_data.xlsx')

#specify a name
worksheet = workbook.add_worksheet("college_data")

cell_format = workbook.add_format()
cell_format.set_bg_color('#f4b084')
cell_format.set_bold()
cell_format.set_align('center')
cell_format.set_bottom()
cell_format.set_left()
cell_format.set_right()

worksheet.set_column('A:G', 70)


worksheet.write(0, 0, "Name of college", cell_format)
worksheet.write(0, 1, "Courses Offered", cell_format)
worksheet.write(0, 2, "Contact-phone", cell_format)
worksheet.write(0, 3, "Email ID", cell_format)
worksheet.write(0, 4, "Website of College", cell_format)
worksheet.write(0, 5, "Address of College", cell_format)
worksheet.write(0, 6, "Type - engineering/medical/commerce/arts", cell_format)

Sheetrows = 1
Sheetcolumns =0 

#------------------------------------------------
# Find and get states URL in a table
#------------------------------------------------
AllStates = findstates.find_all('td')


count = 1
count2 = 1
locater = 1


for index, singleState in enumerate(AllStates):
	
	a_tag = singleState.find('a')

		
	# To get rid of an empty td an the end of the table
	if(count == 27):
		break

	state_col_link = a_tag.get('href')

	#--------------------------------------------------
	# concatenate the Url and request state infor
	#--------------------------------------------------
	full_col_link = "https://www.ugc.ac.in/"+state_col_link
	#full_col_link = "https://www.ugc.ac.in/stateuniversitylist.aspx?id=9U80RXV93k09HNgOCkd8+w==&Unitype=iA7z/ds2To+MdcuCvitOpQ=="
	Open_college_link = requests.get(full_col_link).text
	soup1 = BeautifulSoup(Open_college_link, 'lxml')
	AllColleges = soup1.find('div', class_ = 'centerpaneltable')
	
	single_college_infor = AllColleges.find_all('tr')

	#-----------------------------------------------------------------------
	# traverse through the table and output the colleges infor in this state
	#-----------------------------------------------------------------------
	
	menu = 0	
	for collegeinfo in single_college_infor:
		
		collegeName = collegeinfo.find('b').text.replace(' ','')

		collegewebsiteA_tag = collegeinfo.find('a')
		collegeWebsite = collegewebsiteA_tag.get('href')

		CollegeAddress = collegeinfo.find(class_ = 'box200').text.replace(' ','')
	
		#--------------------------------------------------------
		# access a table of each university in a new link
		#--------------------------------------------------------
		#Spec_col_panel = soup1.find_all('div', class_ = 'panel-body')

		coverted_num = str(menu)
		#Spec_col_link = Spec_col_panel.find('div', id = 'menu51')
		Spec_col_link = collegeinfo.find('div', id = 'menu5'+coverted_num)
		
		i_tag = Spec_col_link.find('iframe')

		Get_col_link = i_tag.get('src')
	
		#--------------------------------------------------
		# concatenate the Url and request state infor
		#--------------------------------------------------
		full_col_tab_link = "https://www.ugc.ac.in/"+Get_col_link
		specificCollegeInfo = requests.get(full_col_tab_link).text

		soup0 = BeautifulSoup(specificCollegeInfo, 'lxml')

		findinfo = soup0.find('table', class_ = 'text')

		pointer = findinfo.find_all('td')

		i = 0
		k = 0
		for index, contact in enumerate(pointer):
			if index == 2:
				CollegeContact = contact.font.text.replace(' ','')
				
				searcher = re.search("PhoneNo:", CollegeContact)

				if(searcher):
					PhoneNo_Str = re.split('PhoneNo:', CollegeContact)
					
					Sec_seacher = re.search("\r\nE-mail:", PhoneNo_Str[1])
					
					if(Sec_seacher):
						EmailArray = re.split('\r\nE-mail:', PhoneNo_Str[1])
						collegephone = (EmailArray[0])

						thrd_searcher = re.search('\r\nWebsite', EmailArray[1])
						
						if(thrd_searcher):
							WebsiteArray = re.split('\r\nWebsite', EmailArray[1])
							CollegeEmail = WebsiteArray[0]
							collegeWebsite = WebsiteArray[1]
						else:
							WebsiteArray = re.split('\nWebsite:', EmailArray[1])
							CollegeEmail = WebsiteArray[0]
							collegeWebsite = WebsiteArray[1]
					else:
						print("\nnot found")
				else:
					print("serch not found")
		print("\n")
		#--------------------------------------------------------
		#write in excel sheet
		#--------------------------------------------------------
        
		worksheet.write(Sheetrows, Sheetcolumns, collegeName)
	#   worksheet.write(Sheetrows, Sheetcolumns + 1, collegecourses)
		worksheet.write(Sheetrows, Sheetcolumns + 2, collegephone)
		worksheet.write(Sheetrows, Sheetcolumns + 3, CollegeEmail)
		worksheet.write(Sheetrows, Sheetcolumns + 4, collegeWebsite)
		worksheet.write(Sheetrows, Sheetcolumns + 5, CollegeAddress)
	# 	worksheet.write(Sheetrows, Sheetcolumns + 6, Collegetype)

		Sheetrows +=1

		menu = int(coverted_num)
		menu += 1
	
	count += 1

workbook.close()

