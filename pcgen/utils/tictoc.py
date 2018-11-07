
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
from datetime import timedelta


class TicToc():

    """Docstring for TicToc. """

    def __init__(self,logger=None,name=''):
        """TODO: to be defined1. """
        if logger is None:
            logger = logging.getLogger('generator.utils.TicToc')
        self.logger = logger
        self.name = name
        self.tic = time.time() 

        self.logger.debug('{} started'.format(self.name))

    def toc(self):
        tac = time.time() - self.tic
        tac = timedelta(seconds=tac)
        self.logger.debug('{} finished: {}'.format(self.name,str(tac)))


if __name__ == "__main__":
    print(' tic toc :) ')
