#!/bin/bash

Rscript -e "library(knitr); knit('mythesis.Rnw')" # simply to add in the knitr latex environments and commands for later tex includes
Rscript -e "library(knitr); knit('body.Rnw')" # doesn't add in knitr environments as only a document fragment (no documentclass)

latexmk -pdf mythesis
makeglossaries mythesis
latexmk -pdf mythesis
latexmk -c mythesis

# Latex -> Pandoc markdown citations
#sed -e 's%\\cite{\([^}]*\)}%@\1%g' # in text citation \cite(key) -> @key
#sed -e 's%\\Textcite{\([^}]*\)}%@\1%g' # in text citation \cite(key) -> @key
#sed -e 's%\\textcite{\([^}]*\)}%@\1%g' # in text citation \cite(key) -> @key
#sed -e 's%\\parencite{\([^}]*\)}%[@\1]%g' # standard citation \parencite(key) -> [@key]

# must convert \parencite(key1,key2..) to [@key1;@key2..]
# must also convert all \cite[] style citations manually...

# Markdown variant
# Rscript -e "library(knitr); knit('Body.Rtex')"
# pandoc -s --chapters --template template.latex -f markdown -t latex -o mythesis.tex mythesis.md
# latexmk -pdf mythesis.tex
# latexmk -c
