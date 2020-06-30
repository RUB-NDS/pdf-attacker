import sys
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTFigure, LTText, LTTextBox, LTTextBoxVertical, LTTextBoxHorizontal

def shadow_hide_detector(document):
    warnings = 0
    #Create resource manager
    rsrcmgr = PDFResourceManager()
    #Set parameters for analysis.
    laparams = LAParams()
    #Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(document):
        interpreter.process_page(page)  
        #Receive the LTPage object for the page.
        layout = device.get_result()

        #Search for elements in pdf
        for element0 in layout:      
            if isinstance(element0, LTFigure or LTText or LTTextBox or LTTextBoxVertical or LTTextBoxHorizontal):
                s = str(element0)
                tmp = s.split(" ")
                #Extract text name
                figure_name = tmp[0]

                #Extract coordinates (figure)
                coordinates_a = tmp[1].split(",")

                #Set points for rectangle a 
                a_left = float(coordinates_a[0])
                a_bottom = float(coordinates_a[1])
                a_right = float(coordinates_a[2])
                a_top = float(coordinates_a[3])

                #Search for text in pdf
                for element1 in layout:
                    if isinstance(element1, LTText or LTTextBox or LTTextBoxVertical or LTTextBoxHorizontal):
                        s = str(element1)
                        tmp = s.split(" ")
                        #Extract coordinates (text)
                        coordinates_b = tmp[1].split(",")

                        #Extract text from content
                        text_content = s[s.index(coordinates_b[3]) + len(coordinates_b[3]):]

                        #Set points for rectangle b
                        b_left = float(coordinates_b[0])
                        b_bottom = float(coordinates_b[1])
                        b_right = float(coordinates_b[2])
                        b_top = float(coordinates_b[3])

                        #Calculate surface area for rectangle b
                        b_S = (b_right - b_left) * (b_top - b_bottom)

                        #Calculate overlap
                        a_b_I = max(0, min(a_right, b_right) - max(a_left, b_left)) * max(0, min(a_top, b_top) - max(a_bottom, b_bottom))

                        #Caluculate ratio r
                        r = a_b_I / b_S

                        #Calculate overlap in percentage p
                        p = round((r*100), 2)

                        if (p > 0 and p < 100):
                            warnings += 1
                            print('WARNING! element: "' + figure_name + '" overlaps ' + str(p) + ' percent of the following content:\n' + text_content)
                        if (p >= 100):
                            warnings += 1
                            print('WARNING! element: "' + figure_name + '" overlaps completely the following content:\n' + text_content)
    return warnings;


#Start
#Check arguments
if(len(sys.argv) < 2):
    print("Please pass the PDF file to be checked as argument!")
elif not(str(sys.argv[1]).endswith('.pdf')):
    print("Please pass only PDF files!")
else:
    document = open(str(sys.argv[1]), 'rb')
    
    #Call detector for category Hide
    warnings = shadow_hide_detector(document)

    if (warnings == 0):
        print('\nCheck complete: no Shadow Attacks in category "Hide" detected.')
    else:
        print('\nCheck complete: WARNING! ' + str(warnings) + ' Shadow Attack(s) in category "Hide" detected.')






