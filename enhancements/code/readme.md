
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

