#!/bin/bash
mkdir -p output
for file in *.pdf; do
    pdfseparate -f 1 -l 4 "$file" "output/${file%.pdf}-%d.pdf"
    pdfunite output/"${file%.pdf}"-*.pdf "output/$file"
    rm output/"${file%.pdf}"-*.pdf
done
