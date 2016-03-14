C:/PROGRA~1/R/R-32~1.3/bin/Rscript.exe -e "library(knitr); knit('mythesis.Rnw')"
C:/PROGRA~1/R/R-32~1.3/bin/Rscript.exe -e "library(knitr); knit('body.Rnw')"

latexmk -pdf mythesis
REM makeglossaries mythesis
REM latexmk -pdf mythesis
latexmk -c mythesis