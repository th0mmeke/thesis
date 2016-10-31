"C:\Program Files\R\R-3.3.1/bin/Rscript.exe" -e "library(knitr); knit('mythesis.Rnw')"
"C:\Program Files\R\R-3.3.1/bin/Rscript.exe" -e "library(knitr); knit('part2.Rnw')"
"C:\Program Files\R\R-3.3.1/bin/Rscript.exe" -e "library(knitr); knit('part3.Rnw')"

latexmk -pdf mythesis
REM latexmk -c mythesis

REM del part*.tex mythesis.tex tmp*.tex
