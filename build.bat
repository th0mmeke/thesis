"C:\Program Files\R\R-3.3.2/bin/Rscript.exe" -e "library(knitr); knit('mythesis.Rnw')"
"C:\Program Files\R\R-3.3.2/bin/Rscript.exe" -e "library(knitr); knit('toyworld.Rnw')"
"C:\Program Files\R\R-3.3.2/bin/Rscript.exe" -e "library(knitr); knit('model.Rnw')"

latexmk -pdf mythesis
