% Based on ryethesis, copyright (C) 2009 by J.V. Lassaline <jvl@ryerson.ca>
% -------------------------------------------------------
%
% This file may be distributed and/or modified under the
% conditions of the LaTeX Project Public License, either version 1.3c
% of this license or (at your option) any later version.
% The latest version of this license is in:
%
%    http://www.latex-project.org/lppl.txt
%
% and version 1.3c or later is part of all distributions of LaTeX
% version 2008/05/04 or later.

\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{mythesis}[2011/04/05 v2.0 University of Canterbury thesis class definition]
\LoadClass[twoside,11pt]{book}

\RequirePackage{ifthen}
\RequirePackage{fancyhdr}
\RequirePackage{setspace}
\RequirePackage{graphicx}
\RequirePackage[usenames,dvipsnames]{xcolor}
\RequirePackage{sectsty}
\RequirePackage{vmargin}
\RequirePackage{paralist} % for tighter lists
\RequirePackage{titlesec}
\RequirePackage{mathpazo}
\RequirePackage{anyfontsize}
 
\RequirePackage{units}
\RequirePackage[font=small,labelfont=bf, justification=raggedright]{caption}

\newboolean{mylistoftables} \setboolean{mylistoftables}{true}
\newboolean{mylistoffigures} \setboolean{mylistoffigures}{true}
\newboolean{mylistofappendices} \setboolean{mylistofappendices}{false}
\newboolean{myhyperref} \setboolean{myhyperref}{true}
\newboolean{myglossary} \setboolean{myglossary}{true}
\newboolean{myindex} \setboolean{myindex}{false}

\ProcessOptions\relax

\setpapersize{A4}
\setmargrb{1.25in}{1in}{1in}{1in}

\DeclareTextFontCommand{\textsmallcaps}{\scshape}

\RequirePackage{textcase} % provides \MakeTextUppercase and \MakeTextLowercase
\RequirePackage{letterspace} % Set up letterspacing (using microtype package) -- requires pdfTeX v1.40+

\ifmyhyperref
\RequirePackage[pageanchor,hyperindex]{hyperref}
\RequirePackage{bookmark}
\fi
\RequirePackage{cleveref}

 \newcommand{\allcapsspacing}[1]{\textls[200]{#1}}
 \newcommand{\smallcapsspacing}[1]{\textls[50]{#1}}
 \newcommand{\allcaps}[1]{\textls[200]{\MakeTextUppercase{#1}}}
 \newcommand{\smallcaps}[1]{\smallcapsspacing{\scshape\MakeTextLowercase{#1}}}
 \renewcommand{\textsc}[1]{\smallcapsspacing{\textsmallcaps{#1}}}
 \newcommand{\vin}{\hspace{1.5em}}
 \def\labelenumi{\arabic{enumi}.}

 % Definitions from Tufte book class
 % Typesets the font size, leading, and measure in the form of 10/12x26 pc.
 \newcommand{\measure}[3]{#1/#2$\times$\unit[#3]{pc}}
 % Macros for typesetting the documentation
 \newcommand{\hlred}[1]{\textcolor{Maroon}{#1}}% prints in red
 \newcommand{\hangleft}[1]{\makebox[0pt][r]{#1}}
 \newcommand{\hairsp}{\hspace{1pt}}% hair space
 \newcommand{\hquad}{\hskip0.5em\relax}% half quad space
 \newcommand{\TODO}[1]{\textcolor{red}{\bf TODO #1}\xspace}
 \newcommand{\ie}{\textit{i.\hairsp{}e.}\xspace}
 \newcommand{\eg}{\textit{e.\hairsp{}g.}\xspace}
 \newcommand{\na}{\quad--}% used in tables for N/A cells

\providecommand\newthought[1]{%
   \addvspace{1.0\baselineskip plus 0.5ex minus 0.2ex}%
   \noindent\textbf{#1}%
}

\renewcommand{\quote}[2]{{\fontencoding{T1}\selectfont{\Large\guillemotleft}#1{\Large\guillemotright}\footnote{#2}}}
\newcommand\Small{\fontsize{9}{9.2}\selectfont}
\newcommand*\LSTfont{\Small\ttfamily\lsstyle}

\partfont{\color{darkgray}\sffamily\bfseries\selectfont\uppercase}
\sectionfont{\color{darkgray}\bfseries\large\selectfont}
\subsectionfont{\color{darkgray}\selectfont\normalsize}
\subsubsectionfont{\color{darkgray}\selectfont\normalsize}

\titleformat{\chapter}[block]
{\fontsize{60}{62}\selectfont}
{\thechapter}
{5pt}
{\Large}
\titlespacing*{\chapter}{0pt}{-19pt}{10em}

\renewcommand{\cleardoublepage}{%
	\newpage%
	{\pagestyle{empty}
	\clearpage%
	\ifodd \c@page%
	\else%
		\hbox{}\newpage%
		\if@twocolumn%
			\hbox{}\newpage%
		\fi%
	\fi}}
\newcommand{\UCclearpage}{\if@openright\cleardoublepage\else\clearpage\fi}

\renewcommand\frontmatter{%
	\pagenumbering{roman}
	\pagestyle{plain}
	\maketitle
	\insertabstract
	\insertacknowledgements
	\insertdedication
	\UCclearpage
	\tableofcontents
	\insertlot
	\insertlof
  	\UCclearpage
  	\pagenumbering{arabic}
  	\pagestyle{fancy}
%  	% If the acronym feature is used with the glossary of terms, \gls
%  	% commands for acronyms will be expanded on first use if used in the
%  	% front matter (e.g. in the abstract). Reset this usage so that the
%  	% first use of a \gls acronym is expanded in the main matter as well.
  	\ifthenelse{\boolean{myglossary}}{\glsresetall}{}
}

\renewcommand\mainmatter{%
	\pagenumbering{arabic}
	\pagestyle{fancy}
}
\renewcommand\backmatter{%
	\insertappendix
	\insertglossary
	\insertreferences
	\insertindex
}

% The running heads/feet don't have rules
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\fancyhead{} % Clear all header fields
\fancyhead[RO,LE]{\footnotesize \rightmark}
%\fancyhead[LE]{\footnotesize \}
\fancyfoot{} % Clear all footer fields
\fancyfoot[C]{\thepage}



\global\def\theDegree{}
\global\def\theAbstract{}
\global\def\theAcknowledgements{}
\global\def\theDedication{}
\global\def\theAppendices{}
\global\def\listofbibfiles{}

\def\title#1{\gdef\theTitle{#1}\ifmyhyperref\hypersetup{pdftitle={#1}}\fi}
\def\author#1{\gdef\theAuthor{#1}\ifmyhyperref\hypersetup{pdfauthor={#1}}\fi}
\newcommand{\degree}[1]{\gdef\theDegree{#1}\ifmyhyperref\hypersetup{pdfsubject={#1}}\fi}

\renewcommand{\maketitle}
{\begin{titlepage}

  {%
  \sffamily%
  \fontsize{18}{20}\selectfont\par\noindent\textcolor{darkgray}{\textls[200]{\MakeTextUppercase{\theAuthor}}}%
  \vspace{11.5pc}%
  \fontsize{36}{40}\selectfont\par\noindent\textcolor{darkgray}{\textls[200]{\MakeTextUppercase{\theTitle}}}%
  \vfill%
  \fontsize{14}{16}\selectfont\par\noindent{\allcaps{\theDegree}}%%
  \vspace{2pc}%
  \fontsize{12}{14}\selectfont\par\noindent{\allcaps{\today}}%%
  }

 \end{titlepage}

}

\newcommand{\abstract}[1]{\ifx\empty#1\else\gdef\theAbstract{\section*{Abstract}#1}\fi}
\newcommand{\insertabstract}{%
\UCclearpage
%\begin{spacing}{2}
\normalsize
%\theTitle\\
%\theDegree\\
\theAbstract
%\end{spacing}

 ~\vfill
{%
\setlength{\parindent}{0pt}
\setlength{\parskip}{\baselineskip}
Copyright \copyright \the\year\ \theAuthor\\

	\begin{minipage}[t]{0.70\textwidth}
	\vspace{0pt}
   	This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. To view a copy
   	of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to Creative Commons, 444
   	Castro Street, Suite 900, Mountain View, California, 94041, USA.\index{license}
   	\end{minipage}
	\begin{minipage}[t]{0.10\textwidth}
	\vspace{0pt}
   	\hfill
   	\end{minipage}
	\begin{minipage}[t]{0.20\textwidth}
   	\vspace{0pt}
   	\includegraphics[width=\textwidth]{figures/by-nc-nd}
   	\end{minipage}

} }

\newcommand{\acknowledgements}[1]{\ifx\empty#1\else\gdef\theAcknowledgements{#1}\fi}

\newcommand{\insertacknowledgements}{%
\ifx\empty\theAcknowledgements\else{%
\UCclearpage
%\begin{center}
%\section*{Acknowledgements}
%\end{center}
\textit{\theAcknowledgements}
}\fi
}

\newcommand{\dedication}[1]{\ifx\empty#1\else\gdef\theDedication{#1}\fi}

\newcommand{\insertdedication}{%
\ifx\empty\theDedication\else{%
\UCclearpage
%\begin{center}
%\section*{Dedication}
%\end{center}
\theDedication
}\fi
}

\newcommand{\insertlot}{\ifthenelse{\boolean{mylistoftables}}{\UCclearpage\listoftables}{}}
\newcommand{\insertlof}{\ifthenelse{\boolean{mylistoftables}}{\UCclearpage\listoffigures}{}}

\ifthenelse{\boolean{mylistofappendices}}
{%
\newcommand{\nohyphens}{\hyphenpenalty=10000\exhyphenpenalty=10000\relax}
\newcommand{\listofappendices}{\chapter*{List of Appendices}\@starttoc{toa}}
}
{}

\newcommand{\insertloa}{%
\ifthenelse{\boolean{mylistofappendices}}{\UCclearpage\listofappendices}{}
}

\renewcommand{\appendix}[1]{\ifx\empty#1\else\gdef\theAppendices{#1}\fi}

\newcommand{\insertappendix}{%
\ifx\empty\theAppendices\else{%
\UCclearpage
\renewcommand{\thechapter}{\Alph{chapter}}
\renewcommand{\chaptername}{Appendix}
\setcounter{chapter}{0}
\theAppendices
}\fi
}

\ifthenelse{\boolean{myglossary}}
{\RequirePackage[toc,nonumberlist]{glossaries}\makeglossaries%
  %Glossaries prints a confusing warning
  \global\let\warn@noprintglossary\relax
}{}

\ifthenelse{\boolean{myindex}}
{%
\RequirePackage{makeidx}\makeindex
\RequirePackage{multicol}
\renewenvironment{theindex}{%
               \begin{multicols}{2}[\@makeschapterhead{\indexname}\addcontentsline{toc}{chapter}{\indexname}\@mkboth{\MakeUppercase\indexname}{\MakeUppercase\indexname}]%
               \thispagestyle{plain}\parindent\z@
               \parskip\z@ \@plus .3\p@\relax
               \columnseprule \z@
               \columnsep 35\p@
               \let\item\@idxitem
               \end{multicols}
               \clearpage}}
{}

\newcommand{\insertreferences}{%
\ifx\empty\listofbibfiles
\else
 %\clearpage\bibliography{\listofbibfiles}
 \UCclearpage\printbibliography%[title=\bibname]%Change for biblatex
 \addcontentsline{toc}{chapter}{\bibname}
\fi
}

\newcommand{\insertglossary}{%
\ifthenelse{\boolean{myglossary}}
{\UCclearpage%
\printglossaries%glossaries.sty prints a false warning.
\global\let\warn@noprintglossary\relax%
}
{}
}

\newcommand{\insertindex}{%
\ifthenelse{\boolean{myindex}}
{\UCclearpage%
\printindex
}
{}
}


\newcommand{\addtoreferences}[1]{%
\ifx\empty\listofbibfiles\edef\listofbibfiles{#1}\else\edef\listofbibfiles{#1,\listofbibfiles}\fi
}
\newcommand{\ifprefchar}{\ifpunctmark{'}} % Fix for #365 - problems with names such as "van den..."
\newcommand{\biblatexstyle}[1]{%
\usepackage[style=#1,backend=bibtex]{biblatex}
\bibliography{\listofbibfiles}
}
\newcommand{\usebibliography}{\renewcommand{\bibname}{Bibliography}}
\newcommand{\usereferences}{\renewcommand{\bibname}{References}}
\newcommand{\useendnotes}{\renewcommand{\bibname}{End Notes}}


\AtEndOfClass{
\onehalfspacing
\usereferences
}
\AtBeginDocument{
\frontmatter
\mainmatter
}
\AtEndDocument{\backmatter}
\endinput
%%
%% End of file `mythesis.cls'.
