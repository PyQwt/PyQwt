#!/usr/bin/env python

import os
import re
import sys

def stamp(html):
    """Stamp a Python HTML documentation page with the SourceForge logo"""

    def replace(m):
        return ('<span class="release-info">%s '
                'Hosted on <a href="http://sourceforge.net">'
                '<img src="http://sourceforge.net/'
                'sflogo.php?group_id=82987&type=1" width="88" height="31"'
                'border="0" alt="SourceForge Logo"></a></span>' % m.group(1))

    mailRe = re.compile(r'<span class="release-info">(.*)</span>')

##     m = mailRe.search(html)
##     if m:
##          print m.groups()

    return re.sub(mailRe, replace, html)

# stamp()

if __name__ == '__main__':
    for name in sys.argv[1:]:
        html = open(name, 'r').read()
        text = stamp(html)
        if text != html:
            os.remove(name)
            file = open(name, 'w')
            file.write(text)
            file.close()
