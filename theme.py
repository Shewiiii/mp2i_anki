# Adapted from Anki's Dracula theme

fields = [
    {"name": "Front"},
    {"name": "Back"},
    {"name": "tags"},
    {"name": "Reference"},
]

qfmt = """
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Fira Sans">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Fira Code">

<div class="outside"> Question</div>

<div class="card-front shadow">

  {{#Front}}
    <div class="tags">{{edit:tags}}</div>
  {{/Front}}

  <div class="front">{{edit:Front}}</div>

  
    <div class="frontopt"></div>
  

</div>
"""

afmt = """
{{FrontSide}}

<div class="outside"> Answer</div>

<div class="card-back shadow">

  <div class="back">{{edit:Back}}</div>

</div>

{{#Reference}}
<div class="reference">
  <strong>From:</strong> {{edit:Reference}}
</div>
{{/Reference}}
"""

css = """
.card {
 font-family: "Fira Sans";
 font-size: 20px;
 text-align: left;
 color: #584E5C;
 background-color: #e5e5e5;
}

kbd {
 display: inline-block;
 padding: 3px 5px;
 background: #fafbfc;
 border: 1px solid #d1d5da;
 border-radius: 6px;
 color: #333;
 box-shadow: inset 0 -2px 0 #d1d5da;
 font-family: Fira Code;
}

code {
 display: block;
 font-family: Fira Code;
 font-size: 16px;
 padding: 10px;
 border-radius: 5px;
 background-color: #1e1a1f;
 color: #f8f8f2;
}


hr {
 background-color: transparent;
 height: 0px;
 border: none;
 border-bottom: 1px solid rgba(0, 0, 0, .15);
}

.shadow {
 box-shadow: 0 2px 5px rgba(0, 0, 0, .15);
}

.card-front {
 background-color: #4287f5;
 padding: 20px;
 border-radius: 10px;
 color: white;
 margin: 0px 0px 15px 0px;
}

.card-back {
 background-color: white;
 padding: 20px;
 border-radius: 10px;
}

.tags {
 font-family: Fira Code;
 font-size: 14px;
 color: white;
 opacity: 50%;
 margin: 0px 0px 5px 0px;
}

.front {
 font-weight: bold;
}

.back {
 font-weight: normal;
}

.frontopt {
 font-size: 16px;
 margin-top: 5px;
}

.backopt {
 font-size: 14px;
}

.reference {
 margin: 10px 0px;
 font-size: 12px;
 padding-left: 20px;
 opacity: 30%;
}

.outside {
 margin-bottom: 5px;
 color: #6272a4;
 font-size: 12px;
 display: none;
}

# -----------------------------------------------------------------
# NIGHT MODE CONFIG
# -----------------------------------------------------------------

.nightMode b {
 color: #50fa7b;
}

.nightMode hr {
 border-bottom: 1px solid rgba(255, 255, 255, .15);
}

.nightMode.card {
 background-color: #1E1A1F;
}

.nightMode .card-front {
 background-color: #342F36;
}

.nightMode .card-back {
 background-color: #584E5C;
}

# -----------------------------------------------------------------
# HIGHLIGHT CONFIG
# -----------------------------------------------------------------

 .highlight  {
 background: #1E1A1F;
 color: #f8f8f2;
}

.highlight pre {
 font-family: "Fira Code";
 font-size: 14px;
 margin: 0px;
}

.nightMode .highlight .hll { background-color: #f1fa8c }
.nightMode .highlight .c { color: #6272a4 } /* Comment */
.nightMode .highlight .err { color: #f8f8f2 } /* Error */
.nightMode .highlight .g { color: #f8f8f2 } /* Generic */
.nightMode .highlight .k { color: #ff79c6 } /* Keyword */
.nightMode .highlight .l { color: #f8f8f2 } /* Literal */
.nightMode .highlight .n { color: #f8f8f2 } /* Name */
.nightMode .highlight .o { color: #ff79c6 } /* Operator */
.nightMode .highlight .x { color: #f8f8f2 } /* Other */
.nightMode .highlight .p { color: #f8f8f2 } /* Punctuation */
.nightMode .highlight .ch { color: #6272a4 } /* Comment.Hashbang */
.nightMode .highlight .cm { color: #6272a4 } /* Comment.Multiline */
.nightMode .highlight .cp { color: #ff79c6 } /* Comment.Preproc */
.nightMode .highlight .cpf { color: #6272a4 } /* Comment.PreprocFile */
.nightMode .highlight .c1 { color: #6272a4 } /* Comment.Single */
.nightMode .highlight .cs { color: #6272a4 } /* Comment.Special */
.nightMode .highlight .gd { color: #8b080b } /* Generic.Deleted */
.nightMode .highlight .ge { color: #f8f8f2; text-decoration: underline } /* Generic.Emph */
.nightMode .highlight .gr { color: #f8f8f2 } /* Generic.Error */
.nightMode .highlight .gh { color: #f8f8f2; font-weight: bold } /* Generic.Heading */
.nightMode .highlight .gi { color: #f8f8f2; font-weight: bold } /* Generic.Inserted */
.nightMode .highlight .go { color: #584E5C } /* Generic.Output */
.nightMode .highlight .gp { color: #f8f8f2 } /* Generic.Prompt */
.nightMode .highlight .gs { color: #f8f8f2 } /* Generic.Strong */
.nightMode .highlight .gu { color: #f8f8f2; font-weight: bold } /* Generic.Subheading */
.nightMode .highlight .gt { color: #f8f8f2 } /* Generic.Traceback */
.nightMode .highlight .kc { color: #ff79c6 } /* Keyword.Constant */
.nightMode .highlight .kd { color: #8be9fd; font-style: italic } /* Keyword.Declaration */
.nightMode .highlight .kn { color: #ff79c6 } /* Keyword.Namespace */
.nightMode .highlight .kp { color: #ff79c6 } /* Keyword.Pseudo */
.nightMode .highlight .kr { color: #ff79c6 } /* Keyword.Reserved */
.nightMode .highlight .kt { color: #8be9fd } /* Keyword.Type */
.nightMode .highlight .ld { color: #f8f8f2 } /* Literal.Date */
.nightMode .highlight .m { color: #bd93f9 } /* Literal.Number */
.nightMode .highlight .s { color: #f1fa8c } /* Literal.String */
.nightMode .highlight .na { color: #50fa7b } /* Name.Attribute */
.nightMode .highlight .nb { color: #8be9fd; font-style: italic } /* Name.Builtin */
.nightMode .highlight .nc { color: #50fa7b } /* Name.Class */
.nightMode .highlight .no { color: #f8f8f2 } /* Name.Constant */
.nightMode .highlight .nd { color: #f8f8f2 } /* Name.Decorator */
.nightMode .highlight .ni { color: #f8f8f2 } /* Name.Entity */
.nightMode .highlight .ne { color: #f8f8f2 } /* Name.Exception */
.nightMode .highlight .nf { color: #50fa7b } /* Name.Function */
.nightMode .highlight .nl { color: #8be9fd; font-style: italic } /* Name.Label */
.nightMode .highlight .nn { color: #f8f8f2 } /* Name.Namespace */
.nightMode .highlight .nx { color: #f8f8f2 } /* Name.Other */
.nightMode .highlight .py { color: #f8f8f2 } /* Name.Property */
.nightMode .highlight .nt { color: #ff79c6 } /* Name.Tag */
.nightMode .highlight .nv { color: #8be9fd; font-style: italic } /* Name.Variable */
.nightMode .highlight .ow { color: #ff79c6 } /* Operator.Word */
.nightMode .highlight .w { color: #f8f8f2 } /* Text.Whitespace */
.nightMode .highlight .mb { color: #bd93f9 } /* Literal.Number.Bin */
.nightMode .highlight .mf { color: #bd93f9 } /* Literal.Number.Float */
.nightMode .highlight .mh { color: #bd93f9 } /* Literal.Number.Hex */
.nightMode .highlight .mi { color: #bd93f9 } /* Literal.Number.Integer */
.nightMode .highlight .mo { color: #bd93f9 } /* Literal.Number.Oct */
.nightMode .highlight .sa { color: #f1fa8c } /* Literal.String.Affix */
.nightMode .highlight .sb { color: #f1fa8c } /* Literal.String.Backtick */
.nightMode .highlight .sc { color: #f1fa8c } /* Literal.String.Char */
.nightMode .highlight .dl { color: #f1fa8c } /* Literal.String.Delimiter */
.nightMode .highlight .sd { color: #f1fa8c } /* Literal.String.Doc */
.nightMode .highlight .s2 { color: #f1fa8c } /* Literal.String.Double */
.nightMode .highlight .se { color: #f1fa8c } /* Literal.String.Escape */
.nightMode .highlight .sh { color: #f1fa8c } /* Literal.String.Heredoc */
.nightMode .highlight .si { color: #f1fa8c } /* Literal.String.Interpol */
.nightMode .highlight .sx { color: #f1fa8c } /* Literal.String.Other */
.nightMode .highlight .sr { color: #f1fa8c } /* Literal.String.Regex */
.nightMode .highlight .s1 { color: #f1fa8c } /* Literal.String.Single */
.nightMode .highlight .ss { color: #f1fa8c } /* Literal.String.Symbol */
.nightMode .highlight .bp { color: #f8f8f2; font-style: italic } /* Name.Builtin.Pseudo */
.nightMode .highlight .fm { color: #50fa7b } /* Name.Function.Magic */
.nightMode .highlight .vc { color: #8be9fd; font-style: italic } /* Name.Variable.Class */
.nightMode .highlight .vg { color: #8be9fd; font-style: italic } /* Name.Variable.Global */
.nightMode .highlight .vi { color: #8be9fd; font-style: italic } /* Name.Variable.Instance */
.nightMode .highlight .vm { color: #8be9fd; font-style: italic } /* Name.Variable.Magic */
.nightMode .highlight .il { color: #bd93f9 } /* Literal.Number.Integer.Long */
"""
