# shell script takes a single argument, a dictionary code
# convert shell script argument to lower case
if [ ! $1 ]; then
 echo "script requires a dictionary code as parameter"
 echo "Usage: sh dictionary_init.sh <dictcode>"
 echo "<dictcode> must be one of the dictionary codes"
 echo "see http://www.sanskrit-lexicon.uni-koeln.de/"
 exit 1
fi
DICT=`echo $1 | tr '[:upper:]' '[:lower:]'`
if [ -d $DICT ]; then
# We require that a pre-existing directory '$DICT' be absent.
# We try to do this by saving an old version under a new name,
# but sometimes this may fail, for unknown reasons.
 echo "directory $DICT exists"
 DATE=`date +%Y%m%d`
 #echo "date=$DATE"
 SAVEDIR="$DICT-$DATE"
 if [ -d $SAVEDIR ]; then
  echo "ERROR: $SAVEDIR already exists. Please rename $DICT and rerun"
  exit 1
 fi
 echo "moving directory $DICT to $SAVEDIR"
 mv $DICT $SAVEDIR
 # check for error
 if [ $? -ne 0 ]; then
  echo "ERROR moving directory $DICT to $SAVEDIR"
  echo "Trying renaming the directory $DICT, then rerun"
  exit 1 
 fi
else
 echo "directory $DICT DOES NOT exist"
 echo "proceeding to initialize $DICT from the cloud"
fi

mkdir "$DICT"
cd "$DICT"
echo "downloading "$DICT"web1.zip  ..."
# 08-22-2018. Download from http://s3.amazonaws.com/sanskrit-lexicon/blobs/
#   rather than from .../web1/.  
curl -o "$DICT"web1.zip http://s3.amazonaws.com/sanskrit-lexicon/blobs/"$DICT"web1.zip
unzip "$DICT"web1.zip
echo "downloading "$DICT"_pywork.zip ..."
curl -o "$DICT"_pywork.zip http://s3.amazonaws.com/sanskrit-lexicon/blobs/"$DICT"_pywork.zip
unzip "$DICT"_pywork.zip
echo "downloading "$DICT"_orig.zip ..."
curl -o "$DICT"_orig.zip http://s3.amazonaws.com/sanskrit-lexicon/blobs/"$DICT"_orig.zip
unzip "$DICT"_orig.zip


#echo "You need to add a folder with sqlite3.exe to the 'path' variable"
#echo "of the system environment variables"
#echo "This is required to run, pywork/redo_xml.sh"
