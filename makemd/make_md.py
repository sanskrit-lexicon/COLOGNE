# -*- coding: utf-8 -*-
""" make_md.py
    Creation - 20 January 2021
    Author - drdhaval2785
    Usage - python3 make_md.py dictcode

    To create the MD files from given XML file for given dictcode.
"""
import sys
import os
import codecs
import xml.etree.ElementTree as ET
from collections import defaultdict
from indic_transliteration import sanscript


def make_md_folder(dictcode):
    """Make a folder to store the markdown files, if it does not exist."""
    mdfolder = os.path.join('MD', dictcode)
    print(mdfolder)
    if not os.path.exists(mdfolder):
        os.makedirs(mdfolder)


def parse_xml(xmlfile):
    """Parse the Cologe XML file into a dict.

    dict has key1 in Devangari transliteration as key.
    A list of (key1, key2, lnum, pc, text).
    List is used, because there are more than one entry with given headword."""
    # Initialize the result dict.
    # By default it starts with a blank list [].
    result = defaultdict(list)
    # Parse the XML file.
    tree = ET.parse(xmlfile)
    # Get the root of the file.
    root = tree.getroot()
    # <H1><h><key1>akza</key1><key2>akza</key2></h><body><i>akṣa</i>  <div n="P"/>(1) = <i>vibhītaka</i> (Avk; Bpn, p. 9; Dgv, nr. 149; Dn 1, 212; Gul; HB; <div n="lb"/>HK; KB 2, p. 1017-1020; MW; Pr 220; PW; Rn 11, 322-323; V 6, p. <div n="lb"/>160; Vśs); <div n="P"/>(2) a) = <i>rudrākṣa</i> (Avk; Vśs); <div n="lb"/>b) the seed of <i>rudrākṣa</i> (MW; PW); <div n="P"/>(3) a) = <i>indrākṣa</i> (Vśs: = the tuberous root of the creeper called <div n="lb"/><i>ṛṣabhaka</i>); <div n="lb"/>b) = <i>ṛṣabhaka</i> (Avk; Vśs); <i>ṛṣabhaka</i> is an unidentifiable plant, <div n="lb"/>but Vśs identifies it as <bot>CARPOPOGON PRURIENS</bot>; see: <i>kapi-</i> <div n="lb"/><i>kacchū̆;</i> <div n="P"/>(4) = <i>devaśirīṣa</i> (Vśs, unidentified).</body><tail><L>1</L><pc>521</pc></tail></H1>
    for h1 in root:
        # <h><key1>akza</key1><key2>akza</key2></h>
        h = h1.find('h')
        # akza
        key1 = h.find('key1').text
        # akza
        key2 = h.find('key2').text
        # <tail><L>1</L><pc>521</pc></tail>
        tail = h1.find('tail')
        # 1
        lnum = tail.find('L').text
        # 521
        pc = tail.find('pc').text
        # <body><i>akṣa</i>  <div n="P"/>(1) = <i>vibhītaka</i> (Avk; Bpn, p. 9; Dgv, nr. 149; Dn 1, 212; Gul; HB; <div n="lb"/>HK; KB 2, p. 1017-1020; MW; Pr 220; PW; Rn 11, 322-323; V 6, p. <div n="lb"/>160; Vśs); <div n="P"/>(2) a) = <i>rudrākṣa</i> (Avk; Vśs); <div n="lb"/>b) the seed of <i>rudrākṣa</i> (MW; PW); <div n="P"/>(3) a) = <i>indrākṣa</i> (Vśs: = the tuberous root of the creeper called <div n="lb"/><i>ṛṣabhaka</i>); <div n="lb"/>b) = <i>ṛṣabhaka</i> (Avk; Vśs); <i>ṛṣabhaka</i> is an unidentifiable plant, <div n="lb"/>but Vśs identifies it as <bot>CARPOPOGON PRURIENS</bot>; see: <i>kapi-</i> <div n="lb"/><i>kacchū̆;</i> <div n="P"/>(4) = <i>devaśirīṣa</i> (Vśs, unidentified).</body>
        body = h1.find('body')
        # Keep the tags intact.
        text = ET.tostring(body, encoding="unicode")
        # Remove the opening and closing body tag. Keep only the entry.
        text = text.replace('<body>', '')
        text = text.replace('</body>', '')
        # Transliterate the key to Devanagari.
        # hugo converts URLs to lowercase.
        # Therefore, slp1, HK etc. are not usable.
        key1deva = sanscript.transliterate(key1, 'slp1', 'devanagari')
        # Append the (key1, key2, lnum, pc, text) tuple to value.
        result[key1deva].append((key1, key2, lnum, pc, text))
    return result


def key_to_entry(dictcode, key):
    """Return a webpage for given entry on Cologne."""
    baseUrl = 'https://sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/'
    script = 'getword.php'
    # Get the url.
    url = baseUrl + script + '?dict=' + dictcode + '&key=' + key
    # Convert it to markdown format for writing in a file.
    formd = '[' + key + '](' + url + ')'
    return formd


def pc_to_scan(dictcode, pc):
    """Return a webpage for given page,column detail on Cologne."""
    baseUrl = 'https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/'
    script = 'servepdf.php'
    # Get the url.
    url = baseUrl + script + '?dict=' + dictcode + '&page=' + pc
    # Convert it to markdown format for writing in a file.
    formd = '[' + pc + '](' + url + ')'
    return formd


def create_md(parsedData, dictcode):
    """Generate markdown files for given dictionary."""
    for key1deva, value in parsedData.items():
        print(key1deva)
        # MD/snp/अक्ष.md
        mdfile = os.path.join('MD', dictcode, key1deva + '.md')
        fout = codecs.open(mdfile, 'w', 'utf-8')
        fout.write('---\n')
        # title: अक्ष
        fout.write('title: ' + key1deva + '\n')
        fout.write('---\n\n')
        # akza, akza, 1, 521, entry_of_akza
        for (key1, key2, lnum, pc, text) in value:
            # write key2
            fout.write('# ' + key2 + '\n\n')
            # write entry
            fout.write(text + '\n\n')
            # write lnum
            fout.write('lnum: ' + lnum + '\n\n')
            # write link to the scanned image.
            pc1 = pc_to_scan(dictcode, pc)
            fout.write('image: ' + pc1 + '\n\n')
            # write link to Cologne website.
            # This may be removed, if we shift full fledgedly to hugo sites.
            colognelink = key_to_entry(dictcode, key1)
            fout.write('cologne link: ' + colognelink + '\n\n')
        fout.close()


if __name__ == "__main__":
    # snp / SNP
    dictcode = sys.argv[1]
    # snp
    dictcode = dictcode.lower()
    # Relative path of the cologne XML file to parse.
    xmlfile = os.path.join('..', '..', dictcode, 'pywork', dictcode + '.xml')
    # Make folder to store markdown files.
    make_md_folder(dictcode)
    # Parse the xml file.
    parsedData = parse_xml(xmlfile)
    # Write markdown files based on parsed data.
    create_md(parsedData, dictcode)
