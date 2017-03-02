
import logging
from tools import get_all_prior_frames

# logger = logging.getLogger(__name__)
name = get_all_prior_frames()
logger = logging.getLogger('ia.bar.' + __name__)


def baz():
    logger.info('running baz')
    logger.debug('Got some debug info for baz!')
    logger.error('Got an error in baz!')
    logger.info('prior frames in baz is {}'.format(name))
    return 5