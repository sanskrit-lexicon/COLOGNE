origdir=../../../../cologne/csl-orig/v02
for dictlo in acc ap90 ben  gst  ieg \
              inm  krm  mci  yat mw72 \
              pwg  shs  vei  
do
    dig=$origdir/${dictlo}/${dictlo}.txt
    changes=changes/${dictlo}_changes.txt
    neworig="temporig"
    echo "BEGIN Dictionary $dictlo"
    python make_change.py $dig $changes
    python updateByLine.py $dig $changes $neworig/${dictlo}.txt
    echo "END Dictionary $dictlo"
    echo ""
done

 
