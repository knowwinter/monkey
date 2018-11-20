# -*- coding: utf-8 -*-
import re
def parseContent(content, pattern):
    result = re.findall(pattern, content, re.S)
    return result