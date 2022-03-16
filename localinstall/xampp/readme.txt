To install in Windows
  Windows 10 Home, 20H2 installed 10/18/2021
Needed software:  
xampp https://www.apachefriends.org/index.html
  use the default installilocation: /c/xampp:
  windows Defender Firewall has blocked some features of this app
    check: Private networks
    uncheck: Public networks... chosen.  Click Allow access
     click 'Allow access'
  check: Xampp Do you want to start the control panel now
  click Finish
  XAMPP Control Panel:  Click 'Apache Start'
     Close Control panel windwo.
     Control Panel now in 'hidden icons' in tool bar.
 xammp is now installed at /c/xampp/
python3
  Uninstall if needed.
     Goto 'Add or Remove Programs' in windows
  https://www.python.org/downloads/
     Download version of Python 3 for Windows.
     run the 'python-x.y.z-www.exe' installer in your Downloads folder
	check 'Install launcher for all users
	check 'Add Python x.y to PATH
        click 'Install Now'
	(location /c/users/xxx/AppData/Local/Programs/Python/Pythonvvv
  enable 'python3' to invoke python.
     open new Gitbash terminal
     'which python'  lists where python executables are.
     # cd to that location
     cd /c/Users/jimfu/AppData/Local/Programs/Python/Python310/
     # If 'python3.exe' not present ...
     cp python.exe python3.exe
     # start new git bash terminal
     # Now 'python --version' and 'python3 --version' work both in
     # top level gitbash, and also if run within a script ('e.g. sh test.sh')
  install 'mako' module
     pip install mako


gitbash
  https://git-scm.com/downloads
  click 'Windows'
  '64-bit Git for Windows Setup'  etc.

sqlite https://sqlite.org/download.html
  Precompiled binaries for Windows
  sqlite-tools-SSS.zip
  unzip and copy sqlite3.exe to /c/xampp/sqlite/sqlite3.exe
  add /c/xampp/sqlite/ to the system path
    System Properties/Environment Variables...
      Path -- Edit -- New
      c:\xampp\sqlite\
  Open new gitbash terminal and 'sqlite3 --version' to be sure it is there.
  
zip  This is used to create zip-archives in
     /c/xampp/htdocs/cologne/xxx/downloads. These archives are not essential.
     If you want them created, then 'zip.exe' is needed.
     Do you already have it?
       in GitBash terminal, try 'zip --version'.
     If you don't have zip, then install GOW (Gnu on Windows)"
       https://github.com/bmatzelle/gow/.
       Download the installer 'Gow-x.y.z.exe' from
       https://github.com/bmatzelle/gow/releases.
       Run the installer.
     Open a new GitBash terminal, try 'zip --version'.  You should now
       have zip.

Assume rest of installation in /c/ directory

# make directories in which repositories will be cloned.
cd /c/xampp/htdocs
mkdir cologne
mkdir sanskrit-lexicon-scans
Now we have:
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
cd /c/xampp/htdocs/cologne/csl-homepage
sh update_version.sh
sh redo_xampp.sh
-----------------------------------------------------
start up xampp Apache  (the other Xampp modules are not used)
-----------------------------------------------------
In browser, url http://localhost/cologne
   You should get the 'Cologne Digital Sanskrit Dictionaries' home page.
Click on md (the dictionary we initialized above)
-----------------------------------------------------
# Install all the dictionaires:
cd  /c/xampp/htdocs/cologne/csl-pywork/v02
# You can do them one at a time (as with md) for the various dictionary codes,
#   or for just the dictionary codes you want.
#   see redo_xampp_all.sh  to see the dictionary codes.
# OR
# You can run a script which installs all the dictionaries.
sh redo_xampp_all.sh
-----------------------------------------------------
# activate simple-search.
# copy the .htaccess file to your cologne directory
# in gitBash terminal,
cd /c/xampp/htdocs/cologne
curl https://raw.githubusercontent.com/sanskrit-lexicon/COLOGNE/master/localinstall/xampp/.htaccess -o .htaccess

Now go to home page (http://localhost/cologne) and click on 'simple'.
(or go directly to url http://localhost/cologne/simple/)
This simple display should work
-----------------------------------------------------
