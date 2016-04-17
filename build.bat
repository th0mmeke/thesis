Rscript.exe -e "library(knitr); knit('mythesis.Rnw')"
Rscript.exe -e "library(knitr); knit('body.Rnw')"

latexmk -pdf mythesis
latexmk -c mythesis

del tmp-pdfcrop*.tex