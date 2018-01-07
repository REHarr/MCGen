import codecs
import os, re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# http://www.i18nqa.com/debug/utf8-debug.html

cp_1252_chars = {
    # from http://www.microsoft.com/typography/unicode/1252.htm
    u"\x80": u"\u20AC", # EURO SIGN
    u"\x82": u"\u201A", # SINGLE LOW-9 QUOTATION MARK
    u"\x83": u"\u0192", # LATIN SMALL LETTER F WITH HOOK
    u"\x84": u"\u201E", # DOUBLE LOW-9 QUOTATION MARK
    u"\x85": u"\u2026", # HORIZONTAL ELLIPSIS
    u"\x86": u"\u2020", # DAGGER
    u"\x87": u"\u2021", # DOUBLE DAGGER
    u"\x88": u"\u02C6", # MODIFIER LETTER CIRCUMFLEX ACCENT
    u"\x89": u"\u2030", # PER MILLE SIGN
    u"\x8A": u"\u0160", # LATIN CAPITAL LETTER S WITH CARON
    u"\x8B": u"\u2039", # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    u"\x8C": u"\u0152", # LATIN CAPITAL LIGATURE OE
    u"\x8E": u"\u017D", # LATIN CAPITAL LETTER Z WITH CARON
    u"\x91": u"\u2018", # LEFT SINGLE QUOTATION MARK
    u"\x92": u"\u2019", # RIGHT SINGLE QUOTATION MARK
    u"\x93": u"\u201C", # LEFT DOUBLE QUOTATION MARK
    u"\x94": u"\u201D", # RIGHT DOUBLE QUOTATION MARK
    u"\x95": u"\u2022", # BULLET
    u"\x96": u"\u2013", # EN DASH
    u"\x97": u"\u2014", # EM DASH
    u"\x98": u"\u02DC", # SMALL TILDE
    u"\x99": u"\u2122", # TRADE MARK SIGN
    u"\x9A": u"\u0161", # LATIN SMALL LETTER S WITH CARON
    u"\x9B": u"\u203A", # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    u"\x9C": u"\u0153", # LATIN SMALL LIGATURE OE
    u"\x9E": u"\u017E", # LATIN SMALL LETTER Z WITH CARON
    u"\x9F": u"\u0178", # LATIN CAPITAL LETTER Y WITH DIAERESIS
} 

def fix_1252_codes(text):
    """
    Replace non-standard Microsoft character codes from the Windows-1252 character set in a unicode string with proper unicode codes.
    Code originally from: http://effbot.org/zone/unicode-gremlins.htm
    """
    if re.search(u"[\x80-\x9f]", text):
        def fixup(m):
            s = m.group(0)
            return cp_1252_chars.get(s, s)
        if isinstance(text, type("")):
            text = str(text)
        text = re.sub(u"[\x80-\x9f]", fixup, text)
    return text 

# This cleans the contents of a file, expects a full string of the contents
def clean_contents( contents ):
    first_count = len(contents)

    # Conversion
    #contents = contents.decode('iso-8859-1',errors='replace').encode('utf-8',errors='replace')
    contents = contents.decode('cp1252',errors='replace').encode('utf-8',errors='replace')
    #contents = fix_1252_codes(contents)
    #contents = contents.replace('\xc3\xc2','&nbsp;')
    #contents = contents.replace('\xc3\xe2','--')
    contents = contents.replace( 'windows-1252', 'utf-8' )

    contents = ''.join([i if ord(i) < 128 else ' ' for i in contents])
    return contents

# Read and write a file to clean its contents
def clean_file( this_filename ):
    f = codecs.open(this_filename, 'r', encoding="iso-8859-1")
    contents = f.read()    
    f.close()
    
    contents = clean_contents( contents )
    
    f = open( this_filename, 'wb' )
    f.write(bytes(contents.encode('utf-8')))
    f.close()
    return this_filename

#clean_file( 'index.htm' )
#clean_file( 'Brownfield.htm' )
#clean_file( 'HarringtonFamilyBookPosted6Jan2017.htm' )
#clean_file( 'Ackerman.htm' )

#clean_file( 'Ackerman.htm' )

# Run on all files
listing = [ filename for filename in os.listdir('../') if filename.find('.htm') > 0 ]



for filename in listing:
    this_filename = '../' + filename
    
    clean_file( this_filename )



'''
filename='../Ackerman.htm'

import codecs
f = codecs.open(filename, 'r')
contents = f.read()
f.close()

f = open( filename, 'w' )
f.write(contents.decode('iso-8859-1',errors='replace').encode('utf-8',errors='replace'))
f.close()
'''

'''
listing = [ filename for filename in os.listdir('../') if filename.find('.htm') > 0 ]



for filename in listing:
    this_filename = '../' + filename
    
    print( this_filename + ' Initial length: ' + str(first_count) + ' Final length: ' + str(len(contents)) )
'''
