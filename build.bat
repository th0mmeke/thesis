Rscript.exe -e "library(knitr); knit('mythesis.Rnw')"
Rscript.exe -e "library(knitr); knit('part2.Rnw')"
Rscript.exe -e "library(knitr); knit('part3.Rnw')"

latexmk -pdf mythesis
latexmk -c mythesis