"C:\Program Files\R\R-3.2.4revised/bin/Rscript.exe" -e "library(knitr); knit('mythesis.Rnw')"
"C:\Program Files\R\R-3.2.4revised/bin/Rscript.exe" -e "library(knitr); knit('body.Rnw')"

latexmk -pdf mythesis
REM makeglossaries mythesis
REM latexmk -pdf mythesis
latexmk -c mythesis