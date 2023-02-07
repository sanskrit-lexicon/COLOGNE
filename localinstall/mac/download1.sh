dictlo=$1
dictup="${dictlo^^}"
echo "creating directory $dictlo"
mkdir $dictlo
cd $dictlo
year=2020   # for lrv, this must be 2022
zipfile=${dictlo}web1.zip
url="https://www.sanskrit-lexicon.uni-koeln.de/scans/${dictup}Scan/$year/downloads/$zipfile"
echo "downloading $url ..."
curl $url -o $zipfile
echo "unzipping $zipfile"
unzip -q $zipfile   #-q = quiet
echo "$dictlo should be installed now"
pwd
ls
echo "DONE with download1.sh $dictlo"

