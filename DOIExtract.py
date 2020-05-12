import PyPDF3, sys, argparse, requests

arg_parser = argparse.ArgumentParser()
arg_parser.description = 'DOIHelper ---- Extracts DOI Links and bibilography from PDF files.'
arg_parser.add_argument('"<PDF file>"', help='input PDF file', type=str)
arg_parser.add_argument('-o', '--output', help='output file location', default='')
arg_parser.add_argument('-d', '--offline', help='disable bibliography (offline mode)', action='store_true')

if len(sys.argv) == 1:
    arg_parser.print_usage()
    print("Use -h to get full help.")
    sys.exit(1)

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


def output_encode(obj, fh, isbytes=False):
    if type(obj) == requests.models.Response:
        encoding = obj.encoding
        text = obj.text
    elif type(obj) == str:
        encoding = 'utf-8'
        text = obj
    else:
        raise Exception("Invalid output!", type(obj))

    if isbytes:
        fh.write(text.encode(encoding))
    else:
        fh.write(text)


if args.output != '':
    file_out = open(args.output, 'wb')
    isbytes = True
else:
    file_out = sys.stdout
    isbytes = False

for bib_url in bib:
    output_encode(bib_url + '\n', file_out, isbytes)
    if network_available:
        request_body = requests.post(bib_url, headers=headers)
        output_encode(request_body, file_out, isbytes)
            
sys.exit(1)
