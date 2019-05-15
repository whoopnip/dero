from typing import Optional, List, Dict, Any
import warnings
from data import Data
import latex
from latex.exc import LatexBuildError
from dero.latex.logic.pdf.errors.exc import (
    TooManyUnprocessedFloatsException,
    OutputLoopConsecutiveDeadCycles,
    LatexException,
    exception_manager
)
from dero.latex.logic.pdf.api.exc_handler.main import APIExceptionHandler
from dero.latex.logic.pdf.api.exc_handler.prepend.typing import PrependKwargsDict, PrependItemsDict
from dero.latex.logic.pdf.api.exc_handler.prepend.main import add_prepend_items_dict_to_latex_str
from dero.latex.logic.pdf.api.builders.pdflatex import PdfLatexBuilder

def latex_str_to_pdf_obj(latex_str: str,  texinputs: Optional[List[str]] = None, retries_remaining: int = 3,
                         prepend_items_dict: PrependItemsDict = None,
                         prepend_kwargs_dict: PrependKwargsDict = None) -> Data:
    try:
        new_latex_str = add_prepend_items_dict_to_latex_str(prepend_items_dict, latex_str)
        return _latex_to_pdf_obj(new_latex_str, texinputs=texinputs)
    except LatexBuildError as e:
        exceptions = exception_manager.exceptions_from_latex_build_error(e)
        handler = APIExceptionHandler(
            exceptions,
            e,
            latex_str,
            prepend_kwargs_dict=prepend_kwargs_dict,
            prepend_items_dict=prepend_items_dict,
            retries_remaining=retries_remaining,
            texinputs=texinputs
        )
        return handler.handle_exceptions()


def _latex_to_pdf_obj(latex_str: str, texinputs: Optional[List[str]] = None) -> Data:
    if texinputs is None:
        texinputs = []
    pdf = PdfLatexBuilder().build_pdf(latex_str, texinputs=texinputs)
    return pdf

