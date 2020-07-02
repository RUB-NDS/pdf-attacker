#!/usr/bin/env python3
import re
import zlib
from logging import *

def replaceValueInDictionary(pdfbytes, key, new_value, update_xref):
    """Replaces the value of the given "key" (in the last dictionary in "pdfbytes" which contains the key) with "new_value" and returns the modified pdfbytes."""
    dictionaries = getDictionariesWithKey(pdfbytes, key)
    if len(dictionaries) >= 1:
        info("More than one Dictionary containing key found. Using the last one.")
    dictionary = dictionaries[len(dictionaries) - 1]
    old_value = dictionary.group(4)
    new_dictionary = dictionary.group(0).replace(old_value, new_value.encode(), 1)
    return replaceObject(pdfbytes, [int(dictionary.group(1).decode()), int(dictionary.group(2).decode())], new_dictionary, update_xref)

def replaceValueInSpecificDictionary(pdfbytes, dictionary, key, new_value, update_xref):
    """Replaces the value of the given "key" in the given dictionary with "new_value" and replaces the original dictionary with the new one in "pdfbytes". Returns the modified pdfbytes."""
    old_value = getValueOfKey(dictionary.group(0), key)
    new_dictionary = dictionary.group(0).replace(old_value, new_value.encode(), 1)
    return replaceObject(pdfbytes, [int(dictionary.group(1).decode()), int(dictionary.group(2).decode())], new_dictionary, update_xref)

def removeEntryInDictionary(pdfbytes, key, update_xref):
    """Removes the entry and its value (the whole line) with the given "key" from the last dictionary which contains the key in "pdfbytes" and returns the modified pdfbytes."""
    dictionaries = getDictionariesWithKey(pdfbytes, key)
    if len(dictionaries) >= 1:
        info("More than one Dictionary containing key found. Using the last one.")
    dictionary = dictionaries[len(dictionaries) - 1]
    entry = dictionary.group(3)
    pdfbytes = pdfbytes.replace(entry, "".encode())
    if(update_xref):
        pdfbytes = updateXref(pdfbytes)
    return pdfbytes

def removeEntryInSpecificDictionary(pdfbytes, dictionary, key, update_xref):
    """Removes the entry and its value (the whole line) with the given "key" from the given "dictionary" in "pdfbytes" and returns the modified pdfbytes."""
    value = getValueOfKey(dictionary.group(0), key)
    entry = "/".encode() + key.encode() + " ".encode() + value + "\n".encode()
    pdfbytes = pdfbytes.replace(entry, "".encode())
    if(update_xref):
        pdfbytes = updateXref(pdfbytes)
    return pdfbytes

def replaceObject(pdfbytes, object_ref, new_object, update_xref):
    """Replaces last version of an object given by reference (object number and generation number) in "object_ref" with "new_object" in "pdfbytes" and returns modified pdfbytes."""
    old_object = getObjectByReference(pdfbytes, object_ref[0], object_ref[1])
    old_object = old_object[len(old_object) - 1].group(0)
    old_object = old_object.replace("\n".encode(), "\\n".encode())
    new_object = new_object.replace("\n".encode(), "\\n".encode())
    pdfbytes_one_line = pdfbytes.replace("\n".encode(), "\\n".encode())
    pdfbytes_one_line = pdfbytes_one_line.replace(old_object, new_object, 1)
    pdfbytes_new = pdfbytes_one_line.replace("\\n".encode(), "\n".encode())
    if(update_xref):
        pdfbytes_new = updateXref(pdfbytes_new)
    return pdfbytes_new

def getValueOfKey(dictionary, key):
    """Returns the value of the given "key" from the given "dictionary"."""
    search = "(\d+)\s+(\d+)\s+obj.*?[\n\r]{1,2}(/%s\s+(.*?)[\n\r]{1,2}).*?\nendobj" % key
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(dictionary))[0].group(4)

def getDictionariesWithKey(pdfbytes, key):
    """Returns a list of dictionaries as re.match objects. Each dictionary contains the requested "key". group(0) = whole dictionary object; group(1) = object number; group(2) = generation_number; group(3) = requested key together with value; group(4) = value of requested "key"."""
    search_dictionary = "(?<=[\n\r])\d+\s+\d+\s+obj(?P<content>.*?)\sendobj"
    pattern_1 = re.compile(search_dictionary.encode(), re.MULTILINE | re.DOTALL)
    search_key = "(\d+)\s+(\d+)\s+obj.*?[\n\r]{1,2}(/%s\s+(.*?)[\n\r]{1,2}).*?\nendobj" % key
    dictionaries = []
    pattern_2 = re.compile(search_key.encode(), re.MULTILINE | re.DOTALL)
    for x in list(pattern_1.finditer(pdfbytes)):
        if(len(list(pattern_2.finditer(x.group(0)))) != 0):
            dictionaries.append(list(pattern_2.finditer(x.group(0)))[0])
    return dictionaries

def getObjectByNeedle(pdfbytes, needle):
    """
    Returns a list of re.match objects that match needle.
    E.g. set 
    needle = '/V \(Attacker\)'
    Since needle is compiled as a regex, brackets must be escaped.
    The result matches contain
    match.group('objnr')
    match.group('gennr')
    match.group('needle')
    """
    search = "(?<=[\n\r])\d+\s+\d+\s+obj"
    search += ".*?"
    search += "[\n\r]+endobj"
    objpattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)

    n = "(?P<objnr>\d+)\s+(?P<gennr>\d+)\s+obj"
    n += f".*(?P<needle>{needle}).*"
    #n += ".*"
    n += "[\n\r]+endobj"

    needlepattern = re.compile(n.encode(), re.MULTILINE | re.DOTALL)
    result = list()
    for obj in objpattern.finditer(pdfbytes):
        match = needlepattern.match(pdfbytes, obj.start(), obj.end())
        if match:
            result.append(match)
    return result


def getObjectByReference(pdfbytes, object_number, generation_number):
    """Returns a list of re.match objects. Each object contains the start() and end() offset as well as the content within different groups. group(0) = whole object; group(1) = object number; group(2) = generation_number."""
    search = "(?<=\s)(%d)\s+(%d\sobj).*?endobj" % (object_number, generation_number)
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    lastprint = ""
    return list(pattern.finditer(pdfbytes))

def getObjectByType(pdfbytes, object_type):
    """Returns a list of re.match objects. The function matches PDF objects whose /Type entry contains the desired value. Each object contains the start() and end() offset as well as the content within different groups. group(0) = whole dictionary object; group(1) = object number; group(2) = generation_number; group(3) = requested key together with value; group(4) = value of requested "key"."""
    dictionaries = getDictionariesWithKey(pdfbytes, "Type".encode())
    dictionaries_type = []
    for x in dictionaries:
        if(x.group(4) == object_type):
            dictionaries_type.append(x)
    return dictionaries_type

def updateXrefInformation(pdfbytes, object_ref, old_object, new_object):
    """
    NOT WORKING CORRECTLY! DOES NOT UPDATE OBJECTS WITH LOWER OBJECT NUMBERS THAN THE MANIPULATED ONE BUT STANDING BEHIND IT IN THE DOCUMENT! USE updateXref INSTEAD!!!
    Used to update the XRef sections and trailer referencing XRef sections after the byteoffsets have changed due to a replaced object.
    Limitations:
    - Updates all trailers even when the modified object is behind one trailer which means the byteoffset in the trailer is still correct and does not need to be changed
    - Ignores generation number
    - Updates all XRef entries higher than the given object number. This is correct behavior if the objects have increasing byte offsets corresponsing to their increasing object numbers.
    """
    #Get all XRef sections "pdfbytes" contains
    search_sections = "[\n\r]{1,2}(\d+)\s+(\d+)([\n\r]{1,2}\d{10}\s+\d{5}\s+[n|f])+"
    pattern_sections = re.compile(search_sections.encode(), re.MULTILINE)
    xref_sections = list(pattern_sections.finditer(pdfbytes))
    
    #Calculate how many bytes the old_object and new_object differ
    difference = len(new_object) - len(old_object)

    #Iterate over all XRef sections and update the entries if necessary
    for section in xref_sections:
        #Check if current XRef section only contains references to objects with an object number lower than or equal to the object number of the modified object and continue if this is the case.
        if((int(section.group(1)) + int(section.group(2)) - 1) <= object_ref[0]):
            continue
        ##If the section contains references to objects with an object number higher than the object number of the modified object Update, these entries are updated:
        #info("Object Number: " + str(object_ref[0]) + " section: " + section.group(0) + " entries from: " + section.group(1) + " to: " + str((int(section.group(1)) + int(section.group(2)) - 1)))
        #Extract all XRef entries in this section with a new regex.
        search_entries = "(\d{10})\s(\d{5})\s([n|f])"
        pattern_entries = re.compile(search_entries.encode())
        xref_entries = list(pattern_entries.finditer(section.group(0)))
        #Take entries for objects with object numbers higher than object_ref[0] and recalculate the byte offset by adding/subtracting the calculated difference.
        for i in range(len(xref_entries)):
            if((int(section.group(1)) + i) > object_ref[0]):
                new_byte_offset = int(xref_entries[i].group(1)) + difference
                #Replace updated byte offset in XRef entry.
                new_entry = xref_entries[i].group(0).replace(xref_entries[i].group(1), str(new_byte_offset).zfill(10))
                #Replace whole entry (single line!) with updated one in "pdfbytes".
                pdfbytes = pdfbytes.replace(xref_entries[i].group(0), new_entry)
    #Get all trailer the file contains.
    search_trailers = "startxref[\n\r]{1,2}(\d+)[\n\r]{1,2}"
    pattern_trailers = re.compile(search_trailers.encode(), re.MULTILINE)
    trailers = list(pattern_trailers.finditer(pdfbytes))
    # Update "startxref" entries in all trailers.
    for trailer in trailers:
        new_startxref = int(trailer.group(1)) + difference
        #The replace function only works with single line replacements. Therefore pdfbytes is converted to a single line string first. Afterwards, the startxref entry is replaced and finally pdfbytes is converted back to a multiline string.
        pdfbytes_one_line = pdfbytes.replace("\n", "\\n")
        pdfbytes_one_line = pdfbytes_one_line.replace("startxref\\n" + trailer.group(1), "startxref\\n" + str(new_startxref), 1)
        pdfbytes = pdfbytes_one_line.replace("\\n", "\n")
    return pdfbytes

###############################################

class XrefTable(list):
    def __init__(self):
        self.append(XrefEntry())

    def getXrefTable(self):
        self.sort()
        cntList = list()
        result = "xref\n"
        if (len(self) > 0):
            e  = self[0]
            cur = e.nr
            cnt = 1
            prev = e
            result += "%d {:d}\n" % cur
            result += "%s\r\n" % e.getShortEntry()
            for e in self[1:]:
                if 1+prev.nr == e.nr: # If current entries is a follow-up entry
                    cnt += 1
                else:
                    cntList.append(cnt) # Save number of entries
                    cur = e.nr
                    cnt = 1 # reset counter
                    result += "%d {:d}\n" % cur
                result += "%s\r\n" % e.getShortEntry()
                prev = e
            cntList.append(cnt) # Save number of entries
            result = result.format(*cntList)
        else:
            result += "(empty)\n"
        return result

    def findObjNr(self, nr):
        return list(filter(lambda x: x.nr == nr, self))

    def parseObjects(self, bytes, additionaloffset=0):
        objects = getAllObjectOffsets(bytes)
        for m in objects:
            offset = m.start() + additionaloffset
            nr = int(m.group("object"))
            generation = int(m.group("generation"))
            inuse = True # Defaults to use object
            e = XrefEntry(nr, generation, offset, inuse)
            #debug("Found    %s", e)
            for contained in self.findObjNr(e.nr):
                #debug("Removing %s", contained)
                self.remove(contained)
            self.append(e)


    def parseXref(self, bytes):
        search  = "(?<=[\n\r])"
        search += "("
        search +="(?P<offset>\d{10})\s+(?P<generation>\d{5})\s+(?P<inuse>[nf])" # Or we have something like '0000000015 00000 n'
        search += "|"
        search += "(?P<start>\d+)\s+(?P<count>\d+)"             # Either we have something like '0 8'
        search += ")"
        nr = 0
        pattern = re.compile(search.encode())
        for match in pattern.finditer(bytes):
            if match.group("start"):
                nr = int(match.group("start"))
            else:
                offset = int(match.group("offset"))
                generation = int(match.group("generation"))
                inuse = True if match.group("inuse") == b"n" else False # Careful: "n" is a byte
                e = XrefEntry(nr, generation, offset, inuse)
                self.append(e)
                nr += 1


class XrefEntry(object):

    def __init__(self, nr=0, gen=65535, offset=0, inuse=False):
        self.nr = nr
        self.gen = gen
        self.offset = offset
        self.inuse = inuse

    def __str__(self):
        nf = "n" if self.inuse else "f"
        return "{:d} {:d} obj @ {:010d} {:s}".format(self.nr, self.gen, self.offset, nf)

    def getLongEntry(self):
        nf = "n" if self.inuse else "f"
        return "{:d} 1\n{:010d} {:05d} {:s}".format(self.nr, self.offset, self.gen, nf)

    def getShortEntry(self):
        nf = "n" if self.inuse else "f"
        return "{:010d} {:05d} {:s}".format(self.offset, self.gen, nf)

    def __lt__(self, other):
        if hasattr(other, "getKey"):
            return self.getKey() < other.getKey()

    def __cmp__(self, other):
        if hasattr(other, "getKey"):
            return self.getKey() - other.getKey()

    def __hash__(self):
        return self.getKey()

    def getKey(self):
        return self.nr

def updateXref(pdfbytes, updatexreftable=None, updatestartxref=None, updatetrailerprev=None, updatetrailersize=None,shortxref = True):
    max = len(getXref(pdfbytes))
    if not updatexreftable:
        updatexreftable = range(max)

    if not updatestartxref:
        updatestartxref = updatexreftable
    if not updatetrailerprev:
        updatetrailerprev = updatexreftable
    if not updatetrailersize:
        updatetrailersize = updatexreftable

    previousxrefstart = None

    #debug("Going to update xref tables %s", updatexreftable)
    #debug("Going to update startxref %s", updatestartxref)
    #debug("Going to update /Prev %s", updatetrailerprev)
    #debug("Going to update /Size %s", updatetrailersize)

    for i in range(max):
        xref = getXref(pdfbytes)[i]
        trailer = getTrailer(pdfbytes)[i]
        startxref = getStartxref(pdfbytes)[i]

        # Re-creating xref table
        updatedxref = XrefTable()
        if previousxrefstart and shortxref:
            parserstart = previousxrefstart
        else:
            parserstart = 0
        updatedxref.parseObjects(pdfbytes[parserstart:xref.start()],parserstart)
        updatedxref.sort() # WE MUST USE SORT BEFRE PRINTING XREF TABLE

        if i in updatestartxref:
            newxrefstart = xref.start()
            #debug("Update startxref %d to %d", i, newxrefstart)
            pdfbytes[startxref.start("value"):startxref.end("value")] = "{:d}".format(newxrefstart).encode()

        if i in updatetrailersize and trailer.start("size") > 0:
            # TODO: Non efficient way to determine size, but working...
            tmp = XrefTable()
            tmp.parseObjects(pdfbytes[:xref.start()])
            tmp.sort()
            size = len(tmp)

            #debug("Update /Size in Trailer %d to %d", i, size)
            pdfbytes[trailer.start("size"):trailer.end("size")] = "{:d}".format(size).encode()
            # Re-parsing because we might have an offset change due to previous change
            xref = getXref(pdfbytes)[i]
            trailer = getTrailer(pdfbytes)[i]

        if previousxrefstart and i in updatetrailerprev and trailer.start("prev") > 0:
            #debug("Update /Prev in Trailer %d to %d", i, previousxrefstart)
            pdfbytes[trailer.start("prev"):trailer.end("prev")] = "{:d}".format(previousxrefstart).encode()
            # Re-parsing because we might have an offset change due to previous change
            xref = getXref(pdfbytes)[i]
            trailer = getTrailer(pdfbytes)[i]

        if i in updatexreftable:
            # Finally, update xref table
            newxreftable = updatedxref.getXrefTable()
            #debug("Update xref table %d to:\n%s", i,newxreftable)
            pdfbytes[xref.start():xref.end()] = newxreftable.encode()

        previousxrefstart = xref.start()
    return pdfbytes


def generateContentBytes(id, content, flatedecode=False):
    # TODO: Fix a Bug with flatdecode=True
    if flatedecode:
        content = zlib.compress(content.encode())
        start = """{:s} obj
    <<
    /Length {:d}
    /Filter /FlateDecode
    >>
    stream
    """.format(id, len(content) + len("stream\n")).encode()
        # TODO: It is still unclear how to compute the correct length value
        end = """
    endstream
    endobj
    """.encode()
        result = start + content + end
        #debug("Created content obj:\n%s", result)
    else:
        result = """{:s} obj
<< /Length {:d} >>
stream
{:s}
endstream
endobj""".format(id, len(content), content).encode()
    return result

def getObject(pdfbytes, objectidgenstring):
    search = "(?<=[\n\r])(%s\s+obj).*?endobj" % objectidgenstring
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(pdfbytes))

def getAllObjectOffsets(pdfbytes):
    """
    Returns a List() of re.mtach Objects. Each object has the group <object> and <generation>
    Use start() to get the offset
    :param pdfbytes:
    :return: [re.match]
    """
    search  = "(?<=[\n\r])"
    search += "(?P<object>\d+)\s+(?P<generation>\d+)\s+obj"
    pattern = re.compile(search.encode())
    return list(pattern.finditer(pdfbytes))

def getContents(pdfbytes):
    search  = "(?<=[\n\r])"
    #search += "\/Type\s+\/Pages.*?"
    search += "\/Contents\s+(?P<object>\d+\s+\d+)\s+R"
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(pdfbytes))

def getXref(pdfbytes):
    """returns a list of xref tables."""
    search = "(?<=[\n\r])"             # Lookahead for newline
    search += "xref[\n\r]+"            # xref must be in a single line
    search += "(?:"                    # Matching multple times (1/2)
    search += "(\d+\s+\d+"             # Either we have something like '0 8'
    search += "|\d{10}\s+\d{5}\s+[nf]" # Or we have something like '0000000015 00000 n'
    search += ")\s?[\n\r]+"            # Followed by possible whitespace and newline
    search += ")+"                     # Matching multple times (2/2)
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(pdfbytes))

def getTrailer(pdfbytes):
    """
    return the trailer contained in pdfbytes.
    Each match contains the following groups:
    trailer: matchtes the whole trailer
    trailerdcict: matches everything inside the dict within the trailer
    root and rootentry: matches the 'root' value or the whole 'rootentry' line
    id and identry: matches the 'id' value or the whole 'identry' line
    size and sizeentry: matches the 'size' value or the whole 'sizeentry' line
    prev and preventry: matches the 'prev' value or the whole 'preventry' line
    :param pdfbytes:
    :return: list(re.Match objects)
    """

    # New trailer parsing: now parse every know trailer key from ISO 32000
    search  = "(?<=[\n\r])trailer" # begin trailer sequence
    search += "[\n\r\s]*<<[\n\r\s]*" # Opening sequence for dictionary
    search += "(?P<trailerdict>"
    search += "(?:(?:" # <trailerkey>, e.g. /Root, /ID, /Size, /Prev. Can be followed by whitespaces, so we use double bracket
    # The following for key/value pair search regex are similar, only differ in allowed names
    # Each entry ends with either \r or \n or / (Slash, belonging to next key)
    search += "(?P<rootentry>\/Root\s+(?P<root>\d+\s+\d+\s+R))"
    search += "|"
    search += "(?P<infoentry>\/Info\s+(?P<info>\d+\s+\d+\s+R))"
    search += "|"
    search += "(?P<identry>\/ID\s*(?P<id>\[[^\]]*\]))"
    search += "|"
    search += "(?P<sizenentry>\/Size\s+(?P<size>\d+))"
    search += "|"
    search += "(?P<prevnentry>\/Prev\s+(?P<prev>\d+))"
    search += "|"
    search += "(?P<comment>[\n\r]%[^\n\r]+)" # Comments are also possible
    search += ")[\n\r\s]*)+" # </key>\s+ --> can occur multiple times (second +)
    search += ")" # </trailerdict>
    search += "[\n\r\s]*>>[\n\r\s]*" # Closing sequence for dicitonary
    search += "(?=startxref)" # end trailer sequence

    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(pdfbytes))

def getStartxref(pdfbytes):
    search = "(?<=[\n\r])startxref[\n\r]{1,2}(?P<value>\d+)"
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(pdfbytes))

def extractStream(pdfbytes):
    """ returns a stream match. group(0) includes 'stream' and 'endstream'. group(1) is the content of the stream"""
    search = "(?<=[\n\r>])stream[\n\r]{1,2}(.+?)[\n\r]{1,2}endstream"
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(pdfbytes))

def stream2ascii(streamcontent):
    try:
        result = zlib.decompress(streamcontent)
    except:
        result = b"Error while decompressing content: " + streamcontent
    return result

def getByteRangeAsMatch(pdfbytes):
    """Returns a list of ByteRange-Lists. E.g., use [0][0] to get first element of first byterange element (as integer)"""
    search = "(?:/ByteRange\s*)\[([-?\d\s]+)\]\s+"
    pattern = re.compile(search.encode())
    result = list(pattern.finditer(pdfbytes))
    return result

def getByteRange(pdfbytes):
    """Returns a list of ByteRange-Lists. E.g., use [0][0] to get first element of first byterange element (as integer)"""
    search = "(?:/ByteRange\s*)\[([-?\d\s]+)\]"
    pattern = re.compile(search.encode())
    result = list()
    for match in pattern.finditer(pdfbytes):
        splitted = match.group(1).decode().split(" ")
        #result.append([int(x) for x in splitted])
        matchresult = list()
        for x in splitted:
            stripped = x.strip()
            if stripped:
                matchresult.append(int(stripped))
        result.append(matchresult)
    return result

def getSignatureContents(pdfbytes):
    """
    Returns the /Content matches as a list.
    :param pdfbytes: pdfbytes to scan
    :return: list of /Content regex-matchtes. Each match has a 'content' and a 'zeroes' group
    """
    search = "(?<=[\n\r])\/Contents\s+<(?P<value>.+?(?P<zeroes>0*))>"
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(pdfbytes))

def getSignatureContentInfo(pdfbytes):
    search = "(?<=[\n\r])\/ContentInfo\s+<(?P<value>.+?(?P<zeroes>0*))>"
    pattern = re.compile(search.encode(), re.MULTILINE | re.DOTALL)
    return list(pattern.finditer(pdfbytes))  

def getSignatureTime(pdfbytes):
    search = "\/M\s+\(D:\d{14}\+\d{2}'\d{2}'\)"
    pattern = re.compile(search.encode(), re.VERBOSE)
    return list(pattern.finditer(pdfbytes))
