
## Documentation of some general Cologne programs

### updateByLine.py

python updateByLine.py {OLDFILE} (CHGFILE} {NEWFILE}

This is a simple but fairly general program to modify the
lines of a text file based upon a file of changes.

In the Cologne system of dictionaries, it is used as a primary way
to convert  one form of a dictionary digitization {OLDFILE} into
a better version {NEWFILE} based upon a file of corrections {CHGFILE}.

All files are assumed to be in the UTF-8 encoding.

The format of the CHGFILE is as a sequence of transactions, with two
lines per transaction. In this version, there are three kinds of transactions,
indicated by codes `new`, `ins`, or `del`.

```
'new' = simple change of the text of a particular line
ln old {the text of line number "ln" in file OLDFILE}
ln new {the new text}

'ins' = insertion of new text line
ln old {the text of line number "ln" in file OLDFILE}
ln ins {the new text to be inserted AFTER line 'ln'}

'del' = delete line
ln old {the text of line number "ln" in file OLDFILE}
ln del {this should be empty, but there should be space after 'del'}
```

When there are insertions or deletions, it is important to remember that
'ln' always refers to a line number in {OLDFILE};  the linenumbers of
{NEWFILE} will be changed by insertions or deletions.

The reason for always have the 'old' line in a transaction is as an extra
check on errors.   If the text of the 'old' line # ln in {CHGFILE} differs
from the actual text of line#ln in {OLDFILE}, then the program stops with
an error message.

One other detail of {CHGFILE} format is:
* lines beginning with a semicolon are treated as comment lines.

### xmlvalidate.py

python xmlvalidate.py {xml file) {dtd file}

Written for Python 2.7, with lxml module installed.

Checks that the xml file is *valid* in relation to the dtd file.

This may be used in Windows operating system as a functional equivalent
of the *xmllint* utility of Linux operating systems.


### dictionary_init.sh
This downloads a 'working environment' for a given dictionary.  The downloads are from aws blobs.

I suggest you do the following as preparation.
In your server path  (e.g., \c\xampp\htdocs\),  make a 'cologne' directory.
Cd into this 'cologne' directory.
Then  (using a bash syntax -- I use git-bash for Windows under Windows 10):
`sh dictionary_init.sh mw`

This will create  an 'mw' directory  (\c\xampp\htdocs\cologne\mw)
and three subdirectories:
* \c\xampp\htdocs\cologne\mw\orig  the digitizations; latest form is mw.txt
* \c\xampp\htdocs\cologne\mw\pywork  All the programs used for various updates to mw.txt; also logic for making mw.xml
   See readme_update.sh  for the current instructions for updating or correcting
* \c\xampp\htdocs\cologne\mw\web   This contains the display programs

This could be modified to just download the 'web' directory, which is the only part needed for displays.

