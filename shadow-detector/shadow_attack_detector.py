import os
import os.path
import sys
import time
import re

import pypdftk


from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTFigure, LTText, LTTextBox, LTTextBoxVertical, LTTextBoxHorizontal, LTTextLine
from pdfminer.pdfparser import PDFParser
from pdfminer.psparser import PSLiteral
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

from pdfrw import PdfReader

from random import *

def shadow_hide_preventor(document):
    warnings = 0
    file = open(document, 'rb')

    #Create resource manager
    rsrcmgr = PDFResourceManager()
    #Set parameters for analysis.
    laparams = LAParams()
    #Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(file):
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
                            print('WARNING! element: "' + figure_name + '" overlaps ' + str(p) + ' percent of the following content: ' + text_content)
                        if (p >= 100):
                            warnings += 1
                            print('WARNING! element: "' + figure_name + '" overlaps completely the following content: ' + text_content)
    file.close()
    return warnings

def shadow_hide_preventor_v2(document):

    warnings = 0
    try:
        doc_path = document
        doc = PdfReader(doc_path)
        check = 0
    except:
        doc_path = decompress_file(document)
        doc = PdfReader(doc_path)
        check = 1

    file = open(document, 'rb')

    #Create resource manager
    rsrcmgr = PDFResourceManager()
    #Set parameters for analysis.
    laparams = LAParams()
    #Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    #Search for forms in pdf
    for page in doc.Root.Pages.Kids:
        try:
            for annot in page.Annots:
                try:
                    rect1 = str(annot.Rect)
                    rect1 = rect1.replace('[', '')
                    rect1 = rect1.replace(']', '')
                    rect1 = rect1.replace(',', '')
                    rect1 = rect1.replace("'", '')
                    value1 = str(annot.V)
                    #Extract coordinates (figure)
                    coordinates_a = rect1.split(" ")

                    #Set points for rectangle a
                    a_left = float(coordinates_a[0])
                    a_bottom = float(coordinates_a[1])
                    a_right = float(coordinates_a[2])
                    a_top = float(coordinates_a[3])

                    for page in PDFPage.get_pages(file):
                        interpreter.process_page(page)
                        #Receive the LTPage object for the page.
                        layout = device.get_result()

                        #Search for elements in pdf
                        for element0 in layout:

                            s = str(element0)
                            value0 = element0.get_text()
                            tmp = s.split(" ")

                            #Extract coordinates (figure)
                            coordinates_b = tmp[1].split(",")

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
                                print('WARNING! element: "' + value1 + '" overlaps ' + str(p) + ' percent of the following content: ' + value0)
                            if (p >= 100):
                                warnings += 1
                                print('WARNING! element: "' + value1 + '" overlaps completely the following content: ' + value0)
                except:
                    pass
        except:
            pass

    file.close()
    return warnings

def shadow_hide_preventor_v3(document):

    warnings = 0
    try:
        doc_path = document
        doc = PdfReader(doc_path)
        check = 0
    except:
        doc_path = decompress_file(document)
        doc = PdfReader(doc_path)
        check = 1

    #Search for forms in pdf
    double_check = []
    for page0 in doc.Root.Pages.Kids:
        try:
            for annot0 in page0.Annots:
                try:
                    double_check.append(str(annot0))
                    rect0 = str(annot0.Rect)
                    rect0 = rect0.replace('[', '')
                    rect0 = rect0.replace(']', '')
                    rect0 = rect0.replace(',', '')
                    rect0 = rect0.replace("'", '')
                    value0 = str(annot0.V)
                    #Extract coordinates (figure)
                    coordinates_a = rect0.split(" ")

                    #Set points for rectangle a
                    a_left = float(coordinates_a[0])
                    a_bottom = float(coordinates_a[1])
                    a_right = float(coordinates_a[2])
                    a_top = float(coordinates_a[3])

                    for page1 in doc.Root.Pages.Kids:
                        try:
                            for annot1 in page1.Annots:
                                try:
                                    if(annot0 != annot1):
                                        rect1 = str(annot1.Rect)
                                        rect1 = rect1.replace('[', '')
                                        rect1 = rect1.replace(']', '')
                                        rect1 = rect1.replace(',', '')
                                        rect1 = rect1.replace("'", '')
                                        value1 = str(annot1.V)
                                        #Extract coordinates (figure)
                                        coordinates_b = rect1.split(" ")

                                        #Set points for rectangle a
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

                                        if not(str(annot1) in double_check):
                                            if (p > 0 and p < 100):
                                                warnings += 1
                                                print('WARNING! form: "' + value0 + '" and ' + value1 + ' overlaps each other to: ' + str(p) + ' percent')
                                            if (p >= 100):
                                                warnings += 1
                                                print('WARNING! form: "' + value0 + '" and ' + value1 + ' overlaps each other completely')
                                except:
                                     pass
                        except:
                            pass
                except:
                    pass
        except:
            pass

    return warnings

def shadow_hide_preventor_form(document):
    warnings = 0

    try:
        doc_path = document
        doc = PdfReader(doc_path)
        check = 0
    except:
        doc_path = decompress_file(document)
        doc = PdfReader(doc_path)
        check = 1

    for page in doc.Root.Pages.Kids:
        try:
            for annot in page.Annots:
                try:
                    value0 = annot.V
                    tmp = annot.AP.N.stream
                    index_value1_start = tmp.find("(")
                    index_value1_end = tmp.find(") ")
                    value1 = tmp[index_value1_start:index_value1_end+1]
                except:
                    break
                if(value0 != value1):
                    print('WARNING! Form text: "' + value0 + '" overlayed by text: "' + value1 + '"')
                    warnings+=1
        except:
            break

    if(check == 1):
        if os.path.exists(doc_path):
            os.remove(doc_path)

    return warnings

def shadow_hide_replace_preventor(document):
    warnings = 0

    file = open(document, 'rb')
    content_encoded = file.read()
    file.close()
    content = content_encoded.decode("iso-8859-1")
    content_str = str(content)
    content_str_lower = content_str.lower()

    #Get byte value of Pages object.
    i = 0
    pages_string = "/type /pages"
    index_of_pages = [content_str_lower.find(pages_string)]
    if(index_of_pages[0] < 0):
        pages_string = "/type/pages"
        index_of_pages = [content_str_lower.find(pages_string)]
    if(index_of_pages[0] > 0):
        while(True):
            tmp = content_str_lower.find(pages_string, index_of_pages[i]+6)
            if(tmp > 0):
                index_of_pages.append(tmp)
                i+=1
            else:
                break
    else:
        print("Error: no Pages object found.")
        return warnings

    #Get byte value of endobj of Pages object
    #Get content of Pages object
    #Get index of Kids element
    index_of_pages_end = []
    content_of_pages = []
    index_of_kids = []
    i = 0
    for byte_value in index_of_pages:
        tmp = content_str_lower.find("endobj", byte_value)
        index_of_pages_end.append(tmp)
        tmp = content_str_lower[byte_value:index_of_pages_end[i]]
        content_of_pages.append(tmp)
        tmp = content_str_lower.find("/kids", byte_value, index_of_pages_end[i])
        index_of_kids.append(tmp)
        i+=1

    #Get byte value of newline of Kids element
    #Get content of Kids element
    index_of_kids_end = []
    content_of_kids= []
    i = 0
    for byte_value in index_of_kids:
        tmp = content_str_lower.find('\n', byte_value)
        index_of_kids_end.append(tmp)
        tmp = content_str[byte_value:index_of_kids_end[i]]
        content_of_kids.append(tmp)
        i+=1

    #Replace referenced content objects
    i = 0
    for byte_value in index_of_kids:
        #Check if kids element is not empty
        object_number_kids = re.findall('[0-9]+', content_of_kids[i])
        if(len(object_number_kids) > 1):
            j = 0
            for byte_value2 in index_of_kids:
                if(byte_value != byte_value2):
                    object_number_kids = re.findall('[0-9]+', content_of_kids[j])
                    if(len(object_number_kids) > 1):
                        content_str_replaced = content_str[:byte_value] + content_of_kids[j] + content_str[index_of_kids_end[i]:]
                        content_str_replaced = content_str_replaced[:byte_value2] + content_of_kids[i] + content_str_replaced[index_of_kids_end[j]:]
                        content_encoded = content_str_replaced.encode("iso-8859-1")

                        #Create test file
                        tmpfile_str = "tmpfile_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"
                        tmpfile = open(tmpfile_str, "xb")
                        tmpfile.write(content_encoded)
                        tmpfile.close()

                        #Compare initial document and test file
                        warnings = compare_files_prevent(document, tmpfile_str)
                        if os.path.exists(tmpfile_str):
                            os.remove(tmpfile_str)
                j+=1
        i+=1

    return warnings

def shadow_hide_form_detector(document):
    warnings = 0

    file = open(document, 'rb')
    content_encoded = file.read()
    file.close()
    content = content_encoded.decode("iso-8859-1")
    content_str = str(content)
    content_str_lower = content_str.lower()

    #Get byte value of first signature
    tmp = content_str_lower.find("/type/sig")
    if (tmp > 0):
        index_of_first_sig = tmp
    else:
        index_of_first_sig = content_str_lower.find("/type /sig")

    #Get byte value of EOFs.
    i = 0
    index_of_eof = [content_str.find("%%EOF")+6]
    if(index_of_eof[0] > 0):
        while(True):
            tmp = content_str.find("%%EOF", index_of_eof[i]+6)
            if(tmp > 0):
                index_of_eof.append(tmp+6)
                i+=1
            else:
                break

    if (i == 0):
        print("Error while capturing the EOF byte values!")
        return warnings

    #Get byte value of signature-EOF
    index_of_sig_eof = 0
    i = 0
    for byte_value in index_of_eof:
        if (byte_value > index_of_first_sig):
            index_of_sig_eof = index_of_eof[i-1]
            break
        i+=1

    #Remove incremental updates
    if(len(content_str) >= index_of_eof[-1]):
        content_str_no_updates = content_str[0: index_of_sig_eof:] + content_str[index_of_eof[-1] + 1::]

    content_encoded = content_str_no_updates.encode("iso-8859-1")



    rand = str(randint(1, 9999))
    tmpfile_str = "tmpfile_" + time.strftime("%Y-%m-%d_%H-%M-%S") + rand + ".pdf"
    tmpfile = open(tmpfile_str, "xb")
    tmpfile.write(content_encoded)
    tmpfile.close()



    warnings = compare_files_detection_hide_overlay(document, tmpfile_str)
    if(warnings == 0):
        warnings = compare_files_detection_hide_overlay_v2(document, tmpfile_str)
    if(warnings == 0):
        warnings = shadow_hide_preventor(document)
    if os.path.exists(tmpfile_str):
        os.remove(tmpfile_str)
    return warnings

def shadow_hide_and_hide_replace_detector(document):
    warnings = 0

    file = open(document, 'rb')
    content_encoded = file.read()
    file.close()
    content = content_encoded.decode("iso-8859-1")
    content_str = str(content)
    content_str_lower = content_str.lower()

    #Get byte value of first signature
    tmp = content_str_lower.find("/type/sig")
    if (tmp > 0):
        index_of_first_sig = tmp
    else:
        index_of_first_sig = content_str_lower.find("/type /sig")

    #Get byte value of EOFs.
    i = 0
    index_of_eof = [content_str.find("%%EOF")+6]
    if(index_of_eof[0] > 0):
        while(True):
            tmp = content_str.find("%%EOF", index_of_eof[i]+6)
            if(tmp > 0):
                index_of_eof.append(tmp+6)
                i+=1
            else:
                break

    if (i == 0):
        print("Error while capturing the EOF byte values!")
        return warnings

    #Get byte value of signature-EOF
    index_of_sig_eof = 0
    i = 0
    for byte_value in index_of_eof:
        if (byte_value > index_of_first_sig):
            index_of_sig_eof = index_of_eof[i-1]
            break
        i+=1

    #Remove incremental updates
    if(len(content_str) >= index_of_eof[-1]):
        content_str_no_updates = content_str[0: index_of_sig_eof:] + content_str[index_of_eof[-1] + 1::]


    content_encoded = content_str_no_updates.encode("iso-8859-1")

    rand = str(randint(1, 9999))
    tmpfile_str = "tmpfile_" + time.strftime("%Y-%m-%d_%H-%M-%S") + rand + ".pdf"
    tmpfile = open(tmpfile_str, "xb")
    tmpfile.write(content_encoded)
    tmpfile.close()


    warnings = compare_files(document, tmpfile_str)
    if os.path.exists(tmpfile_str):
        os.remove(tmpfile_str)

    return warnings

def shadow_replace_font_detector(document):
    warnings = 0
    file = open(document, 'rb')
    content_encoded = file.read()
    file.close()
    content = content_encoded.decode("iso-8859-1")
    content_str = str(content)
    content_str_lower = content_str.lower()

    #Get byte value of first signature
    tmp = content_str_lower.find("/type/sig")
    if (tmp > 0):
        index_of_first_sig = tmp
    else:
        index_of_first_sig = content_str_lower.find("/type /sig")

    #Get byte value of EOFs.
    i = 0
    index_of_eof = [content_str.find("%%EOF")+6]
    if(index_of_eof[0] > 0):
        while(True):
            tmp = content_str.find("%%EOF", index_of_eof[i]+6)
            if(tmp > 0):
                index_of_eof.append(tmp+6)
                i+=1
            else:
                break

    if (i == 0):
        print("Error while capturing the EOF byte values!")
        return warnings

    #Get byte value EOF after signature
    index_of_sig_eof = 0
    i = 0
    for byte_value in index_of_eof:
        if (byte_value > index_of_first_sig):
            index_of_sig_eof = index_of_eof[i]
            break
        i+=1

    #Get byte value of FontFile.
    i = 0
    index_of_fontfile = [content_str_lower.find("fontfile")]
    if(index_of_fontfile[0] > 0):
        while(True):
            tmp = content_str_lower.find("fontfile", index_of_fontfile[i]+8)
            if(tmp > index_of_sig_eof):
                break
            elif(tmp > 0):
                index_of_fontfile.append(tmp)
                i+=1
            else:
                break

    if (index_of_fontfile[0] < 0):
        return warnings

    #Get FontFile Object Number
    object_number_fontfile = []
    for byte_value in index_of_fontfile:
        tmp = content_str_lower[byte_value:byte_value+15].split()
        object_number_fontfile.append(tmp[1])


    #Search for FontFiles after signature
    for object_number in object_number_fontfile:
        if(content_str_lower.find(str(object_number)+" 0 obj", index_of_sig_eof) > 0):
            print('WARNING! FontFile: ' + str(object_number)+' 0 obj was added after signing!')
            warnings += 1

    return warnings

def shadow_replace_form_detector(document):
    warnings = 0

    file = open(document, 'rb')
    content_encoded = file.read()
    file.close()
    content = content_encoded.decode("iso-8859-1")
    content_str = str(content)
    content_str_lower = content_str.lower()

    #Get byte value of first signature
    tmp = content_str_lower.find("/type/sig")
    if (tmp > 0):
        index_of_first_sig = tmp
    else:
        index_of_first_sig = content_str_lower.find("/type /sig")

    #Get byte value of EOFs.
    i = 0
    index_of_eof = [content_str.find("%%EOF")+6]
    if(index_of_eof[0] > 0):
        while(True):
            tmp = content_str.find("%%EOF", index_of_eof[i]+6)
            if(tmp > 0):
                index_of_eof.append(tmp+6)
                i+=1
            else:
                break

    if (i == 0):
        print("Error while capturing the EOF byte values!")
        return warnings

    #Get byte value of signature-EOF
    index_of_sig_eof = 0
    i = 0
    for byte_value in index_of_eof:
        if (byte_value > index_of_first_sig):
            index_of_sig_eof = index_of_eof[i-1]
            break
        i+=1

    #Remove incremental updates
    if(len(content_str) >= index_of_eof[-1]):
        content_str_no_updates = content_str[0: index_of_sig_eof:] + content_str[index_of_eof[-1] + 1::]

    content_encoded = content_str_no_updates.encode("iso-8859-1")

    rand = str(randint(1, 9999))
    tmpfile_str = "tmpfile_" + time.strftime("%Y-%m-%d_%H-%M-%S") + rand +".pdf"
    tmpfile = open(tmpfile_str, "xb")
    tmpfile.write(content_encoded)
    tmpfile.close()

    warnings = compare_files_detection_replace_value(document, tmpfile_str)
    if os.path.exists(tmpfile_str):
        os.remove(tmpfile_str)

    return warnings

def compare_files(document0, document1):
    warnings = 0
    file0 = open(document0, 'rb')

    file1 = open(document1, 'rb')

    #Create resource manager
    rsrcmgr0 = PDFResourceManager()
    rsrcmgr1 = PDFResourceManager()
    #Set parameters for analysis.
    laparams0 = LAParams()
    laparams1 = LAParams()
    #Create a PDF page aggregator object.
    device0 = PDFPageAggregator(rsrcmgr0, laparams=laparams0)
    device1 = PDFPageAggregator(rsrcmgr1, laparams=laparams1)
    interpreter0 = PDFPageInterpreter(rsrcmgr0, device0)
    interpreter1 = PDFPageInterpreter(rsrcmgr1, device1)

    for page0 in PDFPage.get_pages(file0):
        interpreter0.process_page(page0)
        #Receive the LTPage object for the page.
        layout0 = device0.get_result()

        #Search for elements in pdf
        for element0 in layout0:
            s0 = str(element0)
            check = 0
            #Search for element in pdf
            for page1 in PDFPage.get_pages(file1):
                #Ignore signature fields
                tmp = s0.split(" ")
                if(tmp[0] == "<LTRect"):
                    check = 1
                    break

                interpreter1.process_page(page1)
                #Receive the LTPage object for the page.
                layout1 = device1.get_result()
                for element1 in layout1:
                    s1 = str(element1)
                    if (s0 == s1):
                        check = 1
            if (check == 0):
                print('WARNING! Object added to document after signing: ' + s0)
                warnings+=1

    for page1 in PDFPage.get_pages(file1):
        interpreter1.process_page(page1)
        #Receive the LTPage object for the page.
        layout1 = device1.get_result()

        #Search for elements in pdf
        for element1 in layout1:
            s1 = str(element1)
            check = 0
            #Search for element in pdf
            for page0 in PDFPage.get_pages(file0):
                #Ignore signature fields
                tmp = s1.split(" ")
                if(tmp[1] == "<LTRect"):
                    check = 1
                    break

                interpreter0.process_page(page0)
                #Receive the LTPage object for the page.
                layout0 = device0.get_result()
                for element0 in layout0:
                    s0 = str(element0)
                    if (s1 == s0):
                        check = 1
            if (check == 0):
                print('WARNING! Object removed from document after signing:\n' + s1)
                warnings+=1



    file0.close()
    file1.close()
    return warnings

def compare_files_prevent(document0, document1):
    warnings = 0
    file0 = open(document1, 'rb')

    file1 = open(document0, 'rb')

    #Create resource manager
    rsrcmgr0 = PDFResourceManager()
    rsrcmgr1 = PDFResourceManager()
    #Set parameters for analysis.
    laparams0 = LAParams()
    laparams1 = LAParams()
    #Create a PDF page aggregator object.
    device0 = PDFPageAggregator(rsrcmgr0, laparams=laparams0)
    device1 = PDFPageAggregator(rsrcmgr1, laparams=laparams1)
    interpreter0 = PDFPageInterpreter(rsrcmgr0, device0)
    interpreter1 = PDFPageInterpreter(rsrcmgr1, device1)

    for page0 in PDFPage.get_pages(file0):
        interpreter0.process_page(page0)
        #Receive the LTPage object for the page.
        layout0 = device0.get_result()

        #Search for elements in pdf
        for element0 in layout0:
            s0 = str(element0)
            check = 0
            #Search for element in pdf
            for page1 in PDFPage.get_pages(file1):

                interpreter1.process_page(page1)
                #Receive the LTPage object for the page.
                layout1 = device1.get_result()
                for element1 in layout1:
                    s1 = str(element1)
                    if (s0 == s1):
                        check = 1
            if (check == 0):
                print('WARNING! Document contains hidden content: ' + s0)
                warnings+=1

    file0.close()
    file1.close()
    return warnings

def compare_files_detection_hide_overlay(document0, document1):
    warnings = 0

    try:
        doc0_path = document0
        doc0 = PdfReader(doc0_path)
        check0 = 0
    except:
        doc0_path = decompress_file(document0)
        doc0 = PdfReader(doc0_path)
        check0 = 1

    try:
        doc1_path = document1
        doc1 = PdfReader(doc1_path)
        check1 = 0
    except:
        doc1_path = decompress_file(document1)
        doc1 = PdfReader(doc1_path)
        check1 = 1

    for page0 in doc1.Root.Pages.Kids:
        try:
            for annot0 in page0.Annots:
                #Ignore signature field
                title = annot0.T.lower()
                if(title.find("signature") == -1):
                    check = 0
                    try:
                        value0 = annot0.AP.N.stream
                    except:
                        break
                    index_value0_start = value0.find("(")
                    index_value0_end = value0.find(") ")
                    string_value0 = value0[index_value0_start:index_value0_end+1]
                    for page1 in doc0.Root.Pages.Kids:
                        for annot1 in page1.Annots:
                            #Ignore signature field
                            title = annot1.T.lower()
                            try:
                                value1 = annot1.AP.N.stream
                            except:
                                break
                            if(value0 == value1):
                                check = 1
                    if(check == 0):
                        print('WARNING! Form text: "' + string_value0 + '" was removed after signing!')
                        warnings+=1
        except:
            break

    if(check0 == 1):
        if os.path.exists(doc0_path):
            os.remove(doc0_path)

    if(check1 == 1):
        if os.path.exists(doc1_path):
            os.remove(doc1_path)

    return warnings

def compare_files_detection_hide_overlay_v2(document0, document1):
    warnings = 0

    try:
        doc0_path = document0
        doc0 = PdfReader(doc0_path)
        check0 = 0
    except:
        doc0_path = decompress_file(document0)
        doc0 = PdfReader(doc0_path)
        check0 = 1

    try:
        doc1_path = document1
        doc1 = PdfReader(doc1_path)
        check1 = 0
    except:
        doc1_path = decompress_file(document1)
        doc1 = PdfReader(doc1_path)
        check1 = 1

    for page0 in doc1.Root.Pages.Kids:
        try:
            for annot0 in page0.Annots:
                check = 0
                try:
                    value0 = annot0.V
                except:
                    pass
                for page1 in doc0.Root.Pages.Kids:
                    for annot1 in page1.Annots:
                        try:
                            value1 = annot1.V
                        except:
                            pass
                        if(value0 == value1):
                            check = 1
                if(check == 0):
                    print('WARNING! Form text: "' + str(value0) + '" was removed after signing!')
                    warnings+=1
        except:
            pass

    if(check0 == 1):
        if os.path.exists(doc0_path):
            os.remove(doc0_path)

    if(check1 == 1):
        if os.path.exists(doc1_path):
            os.remove(doc1_path)

    return warnings

def compare_files_detection_replace_value(document0, document1):
    warnings = 0

    try:
        doc0_path = document0
        doc0 = PdfReader(doc0_path)
        check0 = 0
    except:
        doc0_path = decompress_file(document0)
        doc0 = PdfReader(doc0_path)
        check0 = 1

    try:
        doc1_path = document1
        doc1 = PdfReader(doc1_path)
        check1 = 0
    except:
        doc1_path = decompress_file(document1)
        doc1 = PdfReader(doc1_path)
        check1 = 1

    for page0 in doc0.Root.Pages.Kids:
        try:
            for annot0 in page0.Annots:
                #Ignore signature field
                title = annot0.T.lower()
                if(title.find("signature") == -1):
                    check = 0
                    try:
                        value0 = annot0.AP.N.stream
                    except:
                        break
                    index_value0_start = value0.find(" Tf")
                    index_value0_end = value0.find(") Tj")
                    string_value0 = value0[index_value0_start+5:index_value0_end]
                    for page1 in doc1.Root.Pages.Kids:
                        for annot1 in page1.Annots:
                            #Ignore signature field
                            title = annot1.T.lower()
                            if(title.find("signature") == -1):
                                try:
                                    value1 = annot1.AP.N.stream
                                except:
                                    break
                                index_value1_start = value1.find(" Tf")
                                index_value1_end = value1.find(") Tj")
                                string_value1 = value1[index_value1_start+5:index_value1_end]
                                if(value0 == value1):
                                    check = 1
                    if(check == 0):
                        print('WARNING! Form text: "' + string_value1 + '" replaced by text: "' + string_value0 + '"')
                        warnings+=1
        except:
            break

    if(check0 == 1):
        if os.path.exists(doc0_path):
            os.remove(doc0_path)

    if(check1 == 1):
        if os.path.exists(doc1_path):
            os.remove(doc1_path)

    return warnings

def check_sig_state(document):
    sig_state = 0
    file = open(document, 'rb')
    content = file.read()
    file.close()
    content = content.decode("iso-8859-1")
    content_str = str(content)

    #Check if the pdf contains signatures
    sig_state = content_str.count("/Type/Sig")
    if (sig_state <= 0):
        sig_state = content_str.count("/Type /Sig")


    return sig_state

def remove_sig_and_updates(document):
    file = open(document, 'rb')
    content_encoded = file.read()
    file.close()
    content = content_encoded.decode("iso-8859-1")
    content_str = str(content)
    content_str_lower = content_str.lower()

    #Get byte value of first signature
    tmp = content_str_lower.find("/type/sig")
    if (tmp > 0):
        index_of_first_sig = tmp
    else:
        index_of_first_sig = content_str_lower.find("/type /sig")

    #Get byte value of EOFs.
    i = 0
    index_of_eof = [content_str.find("%%EOF")+6]
    if(index_of_eof[0] > 0):
        while(True):
            tmp = content_str.find("%%EOF", index_of_eof[i]+6)
            if(tmp > 0):
                index_of_eof.append(tmp+6)
                i+=1
            else:
                break

    if (i == 0):
        print("Error while capturing the EOF byte values!")
        return warnings

    #Get byte value of signature-EOF
    index_of_sig_eof = 0
    i = 0
    for byte_value in index_of_eof:
        if (byte_value > index_of_first_sig):
            index_of_sig_eof = index_of_eof[i-1]
            break
        i+=1

    #Remove incremental updates
    if(len(content_str) >= index_of_eof[-1]):
        content_str_no_updates = content_str[0: index_of_sig_eof:] + content_str[index_of_eof[-1] + 1::]

    content_encoded = content_str_no_updates.encode("iso-8859-1")

    rand = str(randint(1, 9999))
    tmpfile_str = "tmpfile_" + time.strftime("%Y-%m-%d_%H-%M-%S") + rand + ".pdf"
    tmpfile = open(tmpfile_str, "xb")
    tmpfile.write(content_encoded)
    tmpfile.close()

    return tmpfile_str

def show_elements(document):
    warnings = 0
    file = open(document, 'rb')

    parser = PDFParser(file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    text = ''
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                text += lt_obj.get_text()
    print(text)


    return warnings

def decompress_file(document):
    rand = str(randint(1, 9999))

    try:
        tmpfile_str = "tmpfile_" + time.strftime("%Y-%m-%d_%H-%M-%S") + rand + ".pdf"
        pypdftk.uncompress(document, tmpfile_str)
        return tmpfile_str
    except:
        return document

def detector(document):
    print("Start Detection-Mode.")
    warnings_detection_all = 0

    #Call detector for category Hide and Hide-and-Replace
    warnings_dec_hide_and_replace = shadow_hide_and_hide_replace_detector(document)

    #Call detector for category Hide (form)
    warnings_dec_hide_form = shadow_hide_form_detector(document)

    #Call detector for category Replace
    warnings_dec_replace_font = shadow_replace_font_detector(document)
    warnings_dec_replace_form = shadow_replace_form_detector(document)

    warnings_detection_all = warnings_dec_replace_font + warnings_dec_replace_form + warnings_dec_hide_and_replace + warnings_dec_hide_form
    if (warnings_detection_all == 0):
        print('Check complete: no active Shadow Attacks detected.')
    else:
        print('\nCheck complete: WARNING! ' + str(warnings_detection_all) + ' active Shadow Attack(s) detected.')

    return warnings_detection_all

def preventor(document):
    print("Start Prevention-Mode.")
    warnings_prevention_all = 0

    #Call preventor for category Hide
    warnings_pre_hide = shadow_hide_preventor(document)
    if(warnings_pre_hide == 0):
        warnings_pre_hide = shadow_hide_preventor_v2(document)
    if(warnings_pre_hide == 0):
        warnings_pre_hide = shadow_hide_preventor_v3(document)

    warnings_pre_hide_form = shadow_hide_preventor_form(document)

    #Call preventor for category Hide-and-Replace
    warnings_pre_hide_replace = shadow_hide_replace_preventor(document)

    warnings_prevention_all =  warnings_pre_hide_replace + warnings_pre_hide + warnings_pre_hide_form
    if (warnings_prevention_all == 0):
        print('Check complete: no inactive Shadow Attacks detected.')
    else:
        print('\nCheck complete: WARNING! ' + str(warnings_prevention_all) + ' inactive Shadow Attack(s) detected.')

    return warnings_prevention_all

def start_preventor_detector(document):
    #show_elements(document)
    warnings = 0

    if(check_sig_state(document) > 0):
        #Detector
        print("PDF File contains signatures.")
        try:
            warnings = detector(document)
        except:
            print("Error in Detection process!")

        if (warnings == 0):
            print('\nNo active Shadow Attacks were found. Search for inactive Shadow Attacks.')
            doc_prev = remove_sig_and_updates(document)
            try:
                warnings = preventor(doc_prev)
            except:
                print("Error in Prevention process!")
            if os.path.exists(doc_prev):
                os.remove(doc_prev)

    else:
        #Preventor
        print("PDF File contains no signatures.")
        try:
            warnings = preventor(document)
        except:
            print("Error in Prevention process!")

    return warnings

def start_directory_search(path):
    warnings = 0
    file_counter = 0
    malicious_files = []
    malicious_file_numbers = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if(file_name.lower().endswith('.pdf')):
                file_counter += 1
                file_name = os.path.join(root, file_name)
                print("*****Start analysis for PDF file #" + str(file_counter) + "*****")
                print("Current file: " + file_name)
                warnings_round = 0
                warnings_round = start_preventor_detector(file_name)
                if(warnings_round > 0):
                    malicious_files.append(file_name)
                    malicious_file_numbers.append(file_counter)
                warnings = warnings + warnings_round
                print("*****End of analysis for this file.*****\n")

    return [warnings, file_counter, malicious_files, malicious_file_numbers]

def main():
    #Start
    print("*****Start PDF-Detector*****\n")
    warnings = 0
    file_counter = 1
    #Check arguments
    if(len(sys.argv) < 2):
        print("Please pass the PDF file or directory to be checked as argument!")
        print("\n*****End*****")
    elif not(os.path.exists(sys.argv[1])):
        print("Wrong file path!")
        print("\n*****End*****")
    elif str(sys.argv[1]).endswith('.pdf'):
        document = str(sys.argv[1])
        warnings = start_preventor_detector(document)
        malicious_files = [document]
        malicious_file_numbers = [file_counter]
    else:
        path = str(sys.argv[1])
        array = start_directory_search(path)
        warnings = array[0]
        file_counter = array[1]
        malicious_files = array[2]
        malicious_file_numbers = array[3]

    print("\n*****End*****\n")
    if(file_counter < 1):
        print("No PDF file found in directory or subdirectory.")
    else:
        print("Checked PDF files: " + str(file_counter))

    if(warnings == 0):
        print("Malicious PDF files: 0")
        print("\nNo Shadow Attacks were found.")
    else:
        print("Malicious PDF files: " + str(len(malicious_files)))
        print("Malicious PDF file names:")
        i = 0
        for file_name in malicious_files:
            print("File #" + str(malicious_file_numbers[i]) + ": " + file_name)
            i += 1
        print("\nWARNING! A total of " + str(warnings) + " Shadow Attack(s) were found!")

if __name__ == "__main__":
    main()





