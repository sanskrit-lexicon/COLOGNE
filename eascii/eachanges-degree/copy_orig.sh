origdir=../../../../cologne/csl-orig/v02
for dictlo in acc ap90 ben  gst  ieg \
              inm  krm  mci  yat mw72 \
              pwg  shs  vei  
do
    dig=$origdir/${dictlo}/${dictlo}.txt
    changes=changes/${dictlo}_changes.txt
    neworig="temporig"
    newdig=$neworig/${dictlo}.txt
    cmd="cp $newdig $dig"
    echo $cmd
    $cmd
done

 
