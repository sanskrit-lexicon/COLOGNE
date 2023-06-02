dictlo=$1
#dictup=`echo $dictlo | tr 'a-z' 'A-Z'`
dictup=`echo $dictlo | tr '[:lower:]' '[:upper:]'`
if [ -f "$dictup" ]; then
    echo "$dictup directory exists"
else 
    echo "creating directory $dictlo"
    mkdir $dictlo
fi
# the download url has a 'year' parameter: e.g. MWScan/2020
# the 'year for most of these is 2020 (as of June 2, 2023).
# but a few use another year
year=2020   # for lrv, this must be 2022
if [ "$dictlo" == "lrv" ]; then
        year=2022
    fi
echo "Using year = $year";

cd $dictlo

zipfile=${dictlo}web1.zip
if [ -f "$zipfile" ]; then
    echo "removing previous zipfile ($zipfile)"
    rm $zipfile
fi

url="https://www.sanskrit-lexicon.uni-koeln.de/scans/${dictup}Scan/$year/downloads/$zipfile"
echo "downloading $url ..."
curl $url -o $zipfile
echo "unzipping $zipfile"
unzip -qu $zipfile   #-q = quiet, -u only changed or new
echo "$dictlo should be installed now"
pwd
ls
echo "DONE with download2.sh $dictlo"

