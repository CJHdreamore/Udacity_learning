class ObsFile(object):
    def __init__(self, file):
        self.fh = file

    def skip_header(self):
        '''Seek to the line right after
        'START OF TEC MAP'  '''
        try:
            for row in self.fh:
                header_label = self._get_header_label(row)
                if header_label == 'START OF TEC MAP':
                    break
        except StopIteration:
            warnings.warn("{program}:Couldn't find 'START OF TEC MAP'")
            raise StopIteration

        @staticmethod
        def _get_header_label(h_row):
            '''Return header label'''
            h_row = h_row.lstrip()
