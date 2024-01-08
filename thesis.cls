\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{thesis}
\def\thesis@class{book}
\PassOptionsToClass{a4paper,11pt,twoside,openright}{\thesis@class}

\newif\if@lablogo
\DeclareOption{lablogo}{\@lablogotrue}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{\thesis@class}}
\ProcessOptions\relax
\LoadClass{\thesis@class}

% must be loaded before cleveref
\RequirePackage{amsmath}

% sets the font to Latin Modern
\RequirePackage{lmodern}
\let\familydefault\sfdefault

% switch to Type-1 fonts
\RequirePackage[T1]{fontenc}

% needed for low-level TeX hacks
\RequirePackage{xpatch, etoolbox}

% add support for French
\RequirePackage[french,english,shorthands=off]{babel}

% needed for defining commands
\RequirePackage{xparse}

% needed for including the resume
\RequirePackage{pdfpages}

% add Appendices to ToC, and as a page before the appendix contents
\RequirePackage[toc,page]{appendix}

% needed for custom headers and footers
\RequirePackage{fancyhdr}
\RequirePackage{emptypage} % hide them on empty pages

% for setting up hyperlinks
\RequirePackage{hyperref}

% backreferencing
\RequirePackage[nosort]{cleveref}

% color boxes
\RequirePackage[most]{tcolorbox}

% source code listings
\RequirePackage{minted}

% needed for `absolute` environment
\RequirePackage{everypage}

% for setting the date
\RequirePackage[nodayofweek]{datetime}

% for captioninig
\RequirePackage{caption}

% for setting up and adjusting ToC bookmarks
\RequirePackage{bookmark}

% \counterwithin
\RequirePackage{chngcntr}

% better typesetting
\RequirePackage{fourier}

\RequirePackage{expl3}

\RequirePackage[utf8]{inputenc}
\RequirePackage[tracking=true,kerning=true,spacing=true]{microtype}
\microtypecontext{spacing=nonfrench}
\RequirePackage[DIV=12,BCOR=2mm,headinclude=true,footinclude=false]{typearea}
\RequirePackage{setspace} % slightly larger spacing
\setstretch{1.1}

%-------------------------------------------------------------------------------

\hypersetup{pdfborder={0 0 0}, colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}

%-------------------------------------------------------------------------------

\fancypagestyle{chapter}{%
  \fancyhf{}%
  \fancyfoot[LE,RO]{\thepage}
  \renewcommand{\headrulewidth}{0pt}%
}

% configure headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\nouppercase{\bfseries\leftmark}}
\fancyhead[RO]{\nouppercase{\bfseries\rightmark}}
\fancyfoot[LE,RO]{\thepage}

\patchcmd{\chapter}{\thispagestyle{plain}}{\thispagestyle{chapter}}{}{}

%-------------------------------------------------------------------------------

% Syntax: <get>: \thedate
%         <set>: \thedate={...}
\NewDocumentCommand\thedate{t=}{%
  \IfBooleanTF{#1}%
  {\def\tmpa##1{\date{##1}}\tmpa}%
  {\@date}%
}

%-------------------------------------------------------------------------------

\def\@definejury[#1]#2{%
  \expandafter\gdef\csname @jurytitle#1\endcsname{#2}%
  \global\expandafter\let\csname if@jury#1\endcsname\iffalse%
  \listgadd{\@jurydefs}{#1}%
}

\def\@appendjury[#1]#2{%
  \expandafter\listgadd\csname @jurylist#1\endcsname{#2}%
  \global\expandafter\let\csname if@jury#1\endcsname\iftrue%
}

\def\@listjurybytitle[#1]{%
  \renewcommand{\do}[1]{%
    \ifblank{##1}{}{%
      {##1, \textit{\@jurytitle} \\}%
    }%
  }%
  \expandafter\let\expandafter\@jurytitle\csname @jurytitle#1\endcsname%
  \csname if@jury#1\endcsname%
    \expandafter\dolistloop\csname @jurylist#1\endcsname%
  \fi
}

\def\@printjury{%
  \renewcommand{\do}[1]{%
    \bgroup\@listjurybytitle[##1]\egroup
  }%
  \dolistloop{\@jurydefs}
}

\@definejury[president]{Jury President}
\@definejury[director]{Thesis Director}
\@definejury[codirector]{Thesis Co-director}
\@definejury[internal]{Internal Examiner}
\@definejury[external]{External Examiner}
\bgroup
\renewcommand{\do}[1]{%
  \expandafter\gdef\csname #1\endcsname ##1{%
    \@appendjury[#1]{##1}%
  }%
}
\dolistloop{\@jurydefs}
\egroup

%-------------------------------------------------------------------------------

\def\@dedication{%
  \begin{raggedleft}
      Follow the white rabbit...\\
      --- The Matrix\\
  \end{raggedleft}
  \vspace{4cm}
  \begin{center}
    Dedicated to my pet bunny.
  \end{center}
  The dedication is usually a short inspirational quote.

  Define your dedication in \texttt{\textbackslash{}dedication\{...\}}
  and show them with \texttt{\textbackslash{}makededication}.
}

\def\@acknowledgments{%
  This is where you thank those who supported you on this journey. Good examples
  are your significant other, family, directors, and other parties that inspired
  you during this project. Generally this section is about 1/2 page to a page.

  Consider acknowledging the use and location of this thesis package.

  Define your acknowledgments in \texttt{\textbackslash{}acknowledgments\{...\}}
  and show them with \texttt{\textbackslash{}makeacks}.
}

\def\@abstract{Don't forget to write your abstract!}
\def\@frenchabstract{N'oubliez pas d'écrire votre résumé !}

%-------------------------------------------------------------------------------

\def\maketitle{\par%
  \begingroup%
    \renewcommand\thefootnote{\fnsymbol{footnote}}%
    \def\@makefnmark{\hbox to\z@{$\m@th^{\@thefnmark}$\hss}}%
    \long\def\@makefntext##1{%
      \parindent 1em\noindent%
      \hbox to1.8em{\hss$\m@th^{\@thefnmark}$}##1%
    }%
    \newpage%
    \global\@topnum\z@%
    \@maketitle\@thanks%
  \endgroup%
  \setcounter{footnote}{0}%
  \let\maketitle\relax%
  \let\@maketitle\relax%
  \let\thanks\relax%
}

\def\@maketitle{
  \begin{titlepage}
    \begin{center}
      \sffamily

      \null\vspace{2cm}
      {\huge \@title}\\[24pt]
      \textcolor{gray}{\small{
      THIS IS A TEMPORARY TITLE PAGE \\
      It will be replaced for the final print by a version \\
      provided by the registrar's office.}}

      \vfill

      \begin{tabular} {cc}
        \parbox{0.3\textwidth}{
          \includegraphics[width=4cm]{EPFLlogo}
          \if@lablogo \vspace{1cm} \\
            \includegraphics[width=4cm]{LABlogo}
          \fi
        }
        &
        \parbox{0.7\textwidth}{%
          Doctoral Thesis \\
          by\\ [4pt]
          \null \hspace{3em} \@author\\[4pt]
          presented on \thedate\\
          %
          at EPFL, Lausanne\\[9pt]
          %
          (To be) Approved by the examining committee:\\[4pt]
          %
          \@printjury
        }
      \end{tabular}
    \end{center}
    \vspace{2cm}
  \end{titlepage}
}

\NewDocumentEnvironment{dedication}{+b}{\long\gdef\@dedication{#1}}{}
\NewDocumentEnvironment{acknowledgments}{+b}{\long\gdef\@acknowledgments{#1}}{}
\NewDocumentEnvironment{abstract}{+b}{\long\gdef\@abstract{#1}}{}
\NewDocumentEnvironment{frenchabstract}{+b}{\long\gdef\@frenchabstract{#1}}{}

\def\makededication{\par%
  \cleardoublepage%
  \thispagestyle{empty}%
  \@dedication%
}

\def\makeacks{\par%
  \cleardoublepage%
  \chapter*{Acknowledgments}%
  \markboth{}{Acknowledgments}%
  \addcontentsline{toc}{chapter}{Acknowledgments}%

  \@acknowledgments%

  \bigskip%

  \noindent\textit{Lausanne, \thedate}%
  \hfill \@author%
}

\def\makeabstracts{%
  \cleardoublepage%
  \chapter*{Abstract}%
  \markboth{}{Abstract}%
  \addcontentsline{toc}{chapter}{Abstract}%
  \@abstract%

  \begin{otherlanguage}{french}%
    \cleardoublepage%
    \chapter*{Résumé}%
    \markboth{}{Résumé}%
    \@frenchabstract%
  \end{otherlanguage}%
}

\def\maketoc{%
  \cleardoublepage%
  \pdfbookmark{\contentsname}{toc}%
  \tableofcontents%

  \listoffigures
  \addcontentsline{toc}{chapter}{List of Figures}

  \listoftables
  \addcontentsline{toc}{chapter}{List of Tables}
  \setlength{\parskip}{1em}%
}

%-------------------------------------------------------------------------------

\xapptocmd{\document}{%
  \frontmatter%
  \counterwithin{listing}{chapter}%
  \maketitle%
  \makededication%
  \makeacks%
  \makeabstracts%
  \maketoc%
  \mainmatter%
}{}{}

%-------------------------------------------------------------------------------

\newcommand{\cv}[1]{%
  \def\@cv{#1}%
}

\def\makecv{%
  \cleardoublepage%
  \phantomsection%
  \addcontentsline{toc}{chapter}{Curriculum Vitae}%
  \includepdf[pages=-,scale=1]{\@cv}%
}
\AtEndDocument{\@ifundefined{@cv}{}{\makecv}}

%-------------------------------------------------------------------------------

\AtBeginEnvironment{appendices}{
  % Shift bookmarks of all appendices under the "Appendices" bookmark
  % FIXME not the cleanest ever, and would probably break if placed elsewhere
  \bookmarksetupnext{rellevel=-1,keeplevel}%
}
\AfterEndEnvironment{appendices}{
  \bookmarksetup{startatroot}%
}
% We use xapptocmd instead of AtBeginEnvironment;
% See https://tex.stackexchange.com/a/540667
\xapptocmd{\appendices}{%
  \makeatletter%
  \addtocontents{toc}{%
    \bgroup
    % Shift appendices in ToC one level inward
    % \let\protect\l@chapter\protect\l@section
    % \let\protect\l@section\protect\l@subsection
    % \let\protect\l@subsection\protect\l@subsubsection

    % Only show "Appendices" in the ToC; exclude listing the chapters, etc...
    \protect\newcounter{oldtocdepth}
    \protect\setcounter{oldtocdepth}{\protect\value{tocdepth}}
    \protect\setcounter{tocdepth}{-1}
  }%
  \makeatother%
}{}{}
\xpretocmd{\endappendices}{%
  \addtocontents{toc}{%
    \protect\setcounter{tocdepth}{\protect\value{oldtocdepth}}
    \egroup
  }%
}{}{}

%-------------------------------------------------------------------------------

%%% Colorboxes %%%
\tcbset{nicetcb/.style={
  enhanced,
  sharp corners,
  attach boxed title to top left={
    xshift=0.5em,
    yshift=-\tcboxedtitleheight/2,
  },
  top=3ex,
  frame hidden,
  boxrule=0pt,
  fonttitle=\bfseries,
  boxed title style={
    sharp corners,
    size=small,
    frame hidden,
    boxrule=0pt
  },
  lines before break=8
}}
%%
% \makespecialtcb [tcbsetupopts] {tcbname} [tcbstyleopts] {tcbcolor} {envheader} {envfooter}
%   defines a new environment with 2 parameters: [tcbstyleopts] {tcbtitle}
\NewDocumentCommand{\makespecialtcb}{O{} m O{} m m m}{%
  \newtcolorbox[#1]{{#2}tcb}[3][]{
    nicetcb,
    colback=##3!15!white,
    title=##2,
    boxed title style={colback=##3},
    label type=#2,
    ##1
  }%
  \newenvironment{#2}[2][]{%
    \RenewDocumentEnvironment{figure}{}{%
      \captionsetup{type=figure}%
      \setlength{\abovecaptionskip}{5pt}%
      \setlength{\belowcaptionskip}{10pt}%
    }%
    {}
    \begin{{#2}tcb}[#3,##1]{##2}{#4}%
      \captionsetup{type=#2}%
      #5%
  }{%
      #6%
    \end{{#2}tcb}%
  }%
}

%-------------------------------------------------------------------------------

\NewDocumentEnvironment{code}{}{%
    \captionsetup{type=listing}%
    \setlength{\abovecaptionskip}{5pt}%
    \setlength{\belowcaptionskip}{10pt}%
  }
  {}
%
\newcounter{line}
\BeforeBeginEnvironment{minted}{%
  \let\oldlabel\label%
  \setcounter{line}{0}
  \renewcommand{\label}[1]{%
    \setcounter{line}{\arabic{FancyVerbLine}}%
    \addtocounter{line}{-1}% Nasty hack to make cleveref work
    \refstepcounter{line}%
    \oldlabel[line]{#1}%
    \hypertarget{#1}{}%
  }%
}
\AfterEndEnvironment{minted}{%
  \let\label\oldlabel%
}

%-------------------------------------------------------------------------------

\crefname{line}{line}{lines}
\apptocmd{\cref@getref}{\xdef\@lastusedlabel{#1}}{}{error}
\crefformat{line}{line~#2\ref{\@lastusedlabel}#3}

%-------------------------------------------------------------------------------

\ExplSyntaxOn
\prop_new:N \g_scope_cmd_prop
\prop_new:N \g_scope_color_prop
\prop_new:N \g_scope_color_alias_prop

\NewDocumentEnvironment{namedscope}{ m t+ }
{
  % Rename common commands for internal use
  \cs_set_eq:NN \origdefinecolor \definecolor
  \cs_set_eq:NN \origcolorlet \colorlet
  \cs_set_eq:NN \origgraphicspath \graphicspath

  % \NewScopedCommand {<cs name>} {<opts>} {<cs body>}
  \NewDocumentCommand{\NewScopedCommand}{ s m m m }
  {
    \IfBooleanTF {##1}
      { \tl_set:Nn \l_tmpa_tl {NewExpandableDocumentCommand} } % FIXME, should be NewDocumentCommand
      { \tl_set:Nn \l_tmpa_tl {NewExpandableDocumentCommand} }
    \seq_clear:N \l_tmpa_seq
    \seq_put_right:Nn \l_tmpa_seq {##2}
    \seq_put_right:Nn \l_tmpa_seq {##3}
    \seq_put_right:Nn \l_tmpa_seq {##4}
    \seq_put_right:NV \l_tmpa_seq \l_tmpa_tl
    \prop_gput:NnV \g_scope_cmd_prop {#1_##2} \l_tmpa_seq
    \exp_args:cc {\l_tmpa_tl} {##2}
      {##3}{##4}
    \IfBooleanT {##1} {
      \expandafter\gdef\csname #1##2\endcsname {%
        \DeclareDocumentCommand\localtmp{##3}{##4}%
        \localtmp%
      }
    }
  }

  % \DefineScopedColor {<color name>} {<color type>} {<color value>}
  \NewDocumentCommand{\DefineScopedColor}{ m m m }
  {
    \prop_gput:Nnn \g_scope_color_prop {#1_##1} {##2, {##3}}
    \origdefinecolor{##1}{##2}{##3}
  }

  % \DefineScopedColorAlias {<color alias>} {<color name>}
  \NewDocumentCommand{\DefineScopedColorAlias}{ m m }
  {
    \prop_gput:Nnn \g_scope_color_alias_prop {#1_##1} {##2}
    \origcolorlet{##1}{##2}
  }

  \NewDocumentCommand{\SetScopedGraphicsPath}{ m }
  {
    \NewScopedCommand{scopedgraphicspath}{}{##1}%
    \bool_lazy_and:nnT
      { \bool_not_p:n {\tl_if_empty_p:c {Ginput@path}} }
      { \tl_if_empty_p:N \l_saved_graphicspath_tl }
      { \tl_set_eq:Nc \l_saved_graphicspath_tl {Ginput@path} }%
    \tl_set:cx {Ginput@path} {##1}
  }

  % Define macros within the scope
  \prop_map_inline:Nn \g_scope_cmd_prop
  {
    \str_set:Nx \l_tmpa_str { \str_range:nnn {##1} { 1 } { \str_count:n { #1 } + 1 } }
    \str_set:Nx \l_tmpb_str { #1_ }
    \str_if_eq:VVT { \l_tmpa_str } { \l_tmpb_str }
    {
      \tl_set:Nn \l_tmpb_tl {\str_range:nnn {##1} { \str_count:n { #1 } + 2 } { -1 }}
      \tl_set:Nx \l_tmpa_tl {\prop_item:Nn \g_scope_cmd_prop {##1}}
      \seq_set_eq:NN \l_tmpa_seq \l_tmpa_tl

      \cs_set_eq:Nc \l_tmpa_cs {\seq_item:Nn \l_tmpa_seq 4}
      \exp_args:Neee \l_tmpa_cs
        {\csname \seq_item:Nn \l_tmpa_seq 1\endcsname}
        {\seq_item:Nn \l_tmpa_seq 2}
        {\seq_item:Nn \l_tmpa_seq 3}
    }
  }

  % Define colors within the scope
  \prop_map_inline:Nn \g_scope_color_prop
  {
    \str_set:Nx \l_tmpa_str { \str_range:nnn {##1} { 1 } { \str_count:n { #1 } + 1 } }
    \str_set:Nx \l_tmpb_str { #1_ }
    \str_if_eq:VVT { \l_tmpa_str } { \l_tmpb_str }
    {
      \clist_set:Nx \l_tmpa_clist { \prop_item:Nn \g_scope_color_prop {##1} }
      \definecolor{ \str_range:nnn {##1} { \str_count:n { #1 } + 2 } { -1 } }
                  { \clist_item:Nn \l_tmpa_clist {1} }
                  { \clist_item:Nn \l_tmpa_clist {2} }
    }
  }

  % Define color aliases within the scope
  \prop_map_inline:Nn \g_scope_color_alias_prop
  {
    \str_set:Nx \l_tmpa_str { \str_range:nnn {##1} { 1 } { \str_count:n { #1 } + 1 } }
    \str_set:Nx \l_tmpb_str { #1_ }
    \str_if_eq:VVT { \l_tmpa_str } { \l_tmpb_str }
    {
      \tl_set:Nn \l_tmpa_tl {\prop_item:Nn \g_scope_color_alias_prop {##1}}
      \colorlet{ \str_range:nnn {##1} { \str_count:n { #1 } + 2 } { -1 } }
               { \tl_use:N \l_tmpa_tl }
    }
  }

  % Restore scoped graphics path if it exists
  \tl_clear_new:N \l_saved_graphicspath_tl
  \cs_if_exist:NT \scopedgraphicspath {%
    \tl_if_empty:cF {Ginput@path} {%
      \tl_set_eq:Nc \l_saved_graphicspath_tl {Ginput@path}%
    }
    \tl_set:cx {Ginput@path} {\scopedgraphicspath}%
  }

  % Only redefine commands if the + (declare) option is set.
  % WARN it's best not to activate this except in a "definitions environment";
  %   overriding commands is very fragile and can break the functionality of
  %   other packages.
  \IfBooleanT {#2} {%
    % Override common commands to use scoped definitions
    \RenewDocumentCommand{\newmacro}{s m O{} m s}{%
      \tl_clear:N \l_tmpa_tl
      \IfBooleanT {##5}
        { \tl_put_right:Nn \l_tmpa_tl * }
      \tl_put_right:Nn \l_tmpa_tl {{##2}}
      \tl_put_right:Nn \l_tmpa_tl {{##3}}
      \IfBooleanTF {##1}
        { \tl_put_right:Nn \l_tmpa_tl {{##4}} }
        { \tl_put_right:Nn \l_tmpa_tl {{##4\xspace}} }
      \expandafter \NewScopedCommand \l_tmpa_tl
    }
    \RenewDocumentCommand{\definecolor}{m m m}{%
      \DefineScopedColor{##1}{##2}{##3}}
    \RenewDocumentCommand{\colorlet}{m m}{%
      \DefineScopedColorAlias{##1}{##2}}
    \RenewDocumentCommand{\graphicspath}{m}{%
      \SetScopedGraphicsPath{##1}}
  }
}
{
  % Undefine macros on scope exit
  \prop_map_inline:Nn \g_scope_cmd_prop
  {
    \str_set:Nx \l_tmpa_str { \str_range:nnn {##1} { 1 } { \str_count:n { #1 } + 1 } }
    \str_set:Nx \l_tmpb_str { #1_ }
    \str_if_eq:VVT { \l_tmpa_str } { \l_tmpb_str }
    {
      \cs_undefine:c { \str_range:nnn {##1} { \str_count:n { #1 } + 2 } { -1 } }
    }
  }
  % TODO undefine colors as well? somehow??
  % Restore saved graphicspath
  \tl_if_empty:NF \l_saved_graphicspath_tl {%
    \origgraphicspath{\l_saved_graphicspath_tl}%
    \tl_set:cn {Ginput@path} {\l_saved_graphicspath_tl}%
  }
}

\NewDocumentCommand{\newmacro}{m O{} m}{%
  \exp_args:Neee \NewDocumentCommand {\csname #1\endcsname} {#2} {#3\xspace}}
\ExplSyntaxOff

%-------------------------------------------------------------------------------

\def\PageTopMargin{1in}
\def\PageLeftMargin{1in}
\newcommand\atxy[3]{%
  \AddThispageHook{%
  \smash{\hspace*{\dimexpr-\PageLeftMargin-\hoffset+#1\relax}%
  \raisebox{\dimexpr\PageTopMargin+\voffset-#2\relax}{#3}}}}

\NewDocumentEnvironment{absolute}{O{0.5}O{0.5}+b}{%
  \atxy{#1\paperwidth}{#2\paperheight}{#3}}{}

%-------------------------------------------------------------------------------
\endinput
