for dictlo in  acc ae ap90 ben   bhs bop bor bur cae \
 ccs gra gst ieg inm  krm mci md mw mw72 \
 mwe pe pgn pui    pw pwg sch shs skd \
 snp stc vcp vei wil  yat lan armh
do
 echo "; ----------------------------------------"
 echo "; tags for ${dictlo}"
 echo "; ----------------------------------------"
 fileout="xmltag_${dictlo}.txt"   
 cat $fileout
 #dictup="${dictlo^^}"
done
