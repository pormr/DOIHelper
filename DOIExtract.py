import PyPDF3, sys, argparse, requests

arg_parser = argparse.ArgumentParser()
arg_parser.description = 'DOIHelper ---- Extracts DOI Links and bibilography from PDF files.'
arg_parser.add_argument('"<PDF file>"', help='target PDF file', type=str)
arg_parser.add_argument('-o', '--output', help='output file location', default='')
arg_parser.add_argument('-d', '--offline', help='disable bibliography(offline mode)', action='store_true')

if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    arg_parser.print_help()
    sys.exit(1)

try:
    args = arg_parser.parse_args()
except:
    print('Incorrect/invalid argument(s) supplied.')
    sys.exit(1)



PDFsource = getattr(args, '"<PDF file>"')
network_available = not args.offline

PDFFile = open(PDFsource,'rb')
PDF = PyPDF3.PdfFileReader(PDFFile)
pages = PDF.getNumPages()
key = '/Annots'
uri = '/URI'
anc = '/A'
bib = []
headers = {
    "Accept": "text/x-bibliography"
}

for page in range(pages):

    pageSliced = PDF.getPage(page)
    pageObject = pageSliced.getObject()

    if key in pageObject:
        ann = pageObject[key]
        for a in ann:
            u = a.getObject()
            if uri in u[anc] and "doi" in u[anc][uri]:
                bib.append(u[anc][uri])

if args.output != '':
    file_out = open(args.output, 'w', encoding='utf-8')
else:
    file_out = sys.stdout
    
for bib_url in bib:
    file_out.write(bib_url + '\n')
    if network_available:
        file_out.write(requests.post(bib_url, headers=headers).text)

sys.exit(1)
