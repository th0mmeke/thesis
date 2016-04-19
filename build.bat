"C:\Program Files\R\R-3.2.4revised/bin/Rscript.exe" -e "library(knitr); knit('mythesis.Rnw')"
"C:\Program Files\R\R-3.2.4revised/bin/Rscript.exe" -e "library(knitr); knit('part2.Rnw')"
"C:\Program Files\R\R-3.2.4revised/bin/Rscript.exe" -e "library(knitr); knit('part3.Rnw')"

latexmk -pdf mythesis
latexmk -c mythesis