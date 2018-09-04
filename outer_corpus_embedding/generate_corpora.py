# -*- coding: utf-8 -*-

import glob
import pickle


class GenerateCorpora:
    """
    Generate corpus (file) from corpora (directory)

    Because this generator generate corpus, not a line of each corpus,
    you should loop twice to get lines from each corpus.

    Use examples (to get lines from each corpus):
        generate_corpora = GenerateCorpora(dirs)
        for corpus in corpora:
            for line in corpus:
                do something
    """

    def __init__(self, file_pattern, unicode=False):
        """
        Args:
            file_pattern: [str] pattern to use glob.iglob to make list of files
                            glob.iglob(file_pattern) should return files (not a directory)
            unicode: [boolean] read file by binary if file is encoded by unicode
        """
        # if not isinstance(dirs, list):
        #     dirs = [dirs]
        # self.dirs = dirs
        self.dirs = glob.iglob(file_pattern)
        self.unicode = unicode

    def _read_data(self, fname):
        """
        Read data from single file omitting empty line

        Args:
            fname: [str] (general file or pickle object) file name to read

        Return:
            data: [list] list of file lines
        """
        if self.unicode:
            with open(fname, 'rb') as f:
                data = f.read()
            return data

        if fname.endswith('pkl'):
            with open(fname, 'rb') as f:
                data = pickle.load(f)
        else:
            with open(fname, 'r') as f:
                data = [line.strip() for line in f.read().splitlines() if line.strip()]
        return data

    def __iter__(self):
        for fname in self.dirs:
            try:
                corpus = self._read_data(fname)
                yield corpus
            except NotADirectoryError:
                pass
        # for each_dir in self.dirs:
        #     fname_list = os.listdir(each_dir)
        #     fnames = [os.path.join(each_dir, fname) for fname in fname_list]
        #     for n, fname in enumerate(fnames):
        #         self.fname = fname
        #         corpus = self._read_data(self.fname)
        #         yield corpus
        #         # for line in corpus:
        #         #     yield line
