
import os
from typing import Sequence, List
from pdfrw import PdfReader, PdfWriter
from PyPDF2 import PdfFileMerger


def strip_pages_pdf(indir, infile, outdir=None, outfile=None, numpages=1, keep=False):
    '''
    Deletes the first pages from a PDF. Omit outfile name to replace. Default is one page.
    If option keep is specified, keeps first pages of PDF, dropping rest.
    '''
    if outfile is None:
        outfile = infile
        
    if outdir is None:
        outdir = indir

    output = PdfWriter()
    inpath = os.path.join(indir,infile)
    outpath = os.path.join(outdir,outfile)
    
    for i, page in enumerate(PdfReader(inpath).pages):
        if not keep:
            if i > (numpages - 1):
                output.addpage(page)
        if keep:
            if i <= (numpages - 1):
                output.addpage(page)

    output.write(outpath)


def merge_pdfs(pdf_paths: Sequence[str], out_path: str):
    merger = PdfFileMerger()

    for pdf in pdf_paths:
        merger.append(pdf)

    merger.write(out_path)


def pdf_filenames_in_folder(folder: str) -> List[str]:
    pdf_files = [file for file in next(os.walk(folder))[2] if file.endswith('.pdf')]
    return pdf_files

