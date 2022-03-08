To install in Windows
Needed software:
xampp, python3, gitbash
My Windows installation
/c/xampp/htdocs/cologne
/c/xampp/htdocs/sanskrit-lexicon-scans/

# clone repositories
cd /c/xampp/htdocs/cologne/
git clone https://github.com/sanskrit-lexicon/csl-orig.git
git clone https://github.com/sanskrit-lexicon/csl-websanlexicon.git
git clone https://github.com/sanskrit-lexicon/csl-pywork.git
git clone https://github.com/sanskrit-lexicon/csl-apidev.git
git clone https://github.com/sanskrit-lexicon/csl-homepage.git
git clone https://github.com/sanskrit-lexicon/csl-doc.git

cd csl-pywork/v02
# Could do 'sh redo_xampp_all.sh', but maybe better to do one dictionary at
# a time.
sh generate_dict.sh md  ../../md

-----------------------------------------------------
cd /c/xampp/htdocs/cologne1/csl-homepage
sh update_version.sh
sh redo_xampp.sh
-----------------------------------------------------
start up xampp Apache  (the other Xampp modules are not used)
In browser
