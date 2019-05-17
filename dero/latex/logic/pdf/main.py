import os
import pathlib

from dero.latex.tools import date_time_move_latex
from dero.latex.logic.pdf.fileops import _move_if_exists_and_is_needed, _copy_if_needed
from dero.latex.texgen.replacements.filename import _latex_valid_basename
from dero.latex.logic.pdf.api.main import latex_str_to_pdf_obj
from dero.latex.typing import BytesListOrNone, StrList, BytesList, StrListOrNone


def document_to_pdf_and_move(document, outfolder, image_paths=None, outname='figure', as_document=True,
                             move_folder_name='Figures', image_binaries: BytesListOrNone = None):

    # Create tex file
    outname_tex = outname + '.tex'
    outpath_tex = os.path.abspath(os.path.join(outfolder, outname_tex))
    with open(outpath_tex, 'w') as f:
        f.write(str(document))

    if image_paths:
        # Copy first time for creation of pdf
        sources_tempfolder = os.path.join(outfolder, 'Sources')
        tex_inputs = [os.path.abspath(outfolder), '']
        if not os.path.exists(sources_tempfolder):
            os.makedirs(sources_tempfolder)
        if image_binaries:
            _write_image_paths_and_binaries_to_folder(sources_tempfolder, image_paths, image_binaries)
        else:
            [_copy_if_needed(filepath, os.path.join(sources_tempfolder, _latex_valid_basename(filepath)))
             for filepath in image_paths]
    else:
        tex_inputs = None

    if as_document:
        outname_pdf = outname + '.pdf'
        outpath_pdf = os.path.abspath(os.path.join(outfolder, outname_pdf))
        latex_str_to_pdf_file(str(document), outpath_pdf, texinputs=tex_inputs)
    new_outfolder = date_time_move_latex(outname, outfolder, folder_name=move_folder_name) #move table into appropriate date/number folder

    if image_paths and new_outfolder:
        # Copy second time to move pictures along with pdf
        sources_tempfolder = os.path.join(outfolder, 'Sources')
        sources_outfolder = os.path.join(new_outfolder, 'Sources')
        if not os.path.exists(sources_outfolder):
            os.makedirs(sources_outfolder)
        if image_binaries:
            _write_image_paths_and_binaries_to_folder(sources_outfolder, image_paths, image_binaries)
        else:
            [_move_if_exists_and_is_needed(
                os.path.join(sources_tempfolder, _latex_valid_basename(filepath)),
                os.path.join(sources_outfolder, _latex_valid_basename(filepath))
             )
            for filepath in image_paths]


def latex_file_to_pdf(folder: str, filename: str):
    # create PDF. Need to run twice for last page, as is written to aux file on the first iteration and
    # aux file is used on the second iteration
    orig_path = os.getcwd()
    os.chdir(folder)
    pdflatex_command = f'pdflatex "{filename}"'
    [os.system(pdflatex_command) for _ in range(2)]
    os.chdir(orig_path)


def latex_str_to_pdf_file(latex_str: str, filepath: str,  texinputs: StrListOrNone = None):
    pdf = latex_str_to_pdf_obj(latex_str, texinputs=texinputs)
    pdf.save_to(filepath)
    return pdf


def _write_image_paths_and_binaries_to_folder(folder: str, image_paths: StrList, image_binaries: BytesList):
    if len(image_binaries) != len(image_paths):
        raise ValueError('must have equal image_binaries and image_path lengths if image_binaries are passed')
    for filepath, binary in zip(image_paths, image_binaries):
        image_outpath = os.path.join(folder, _latex_valid_basename(filepath))
        with open(image_outpath, 'wb') as f:
            f.write(binary)