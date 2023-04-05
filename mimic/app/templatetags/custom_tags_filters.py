import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def clo_link(value):
    return value.replace(":", "_")


@register.filter
@stringfilter
def superscript_replace(str):
    if "(delta)" in str:
        str = str.replace("(delta)", "Δ")
    if "^" in str:
        if "m^2," in str:
            str = str.replace("m^2,", "m<sup>2</sup>;")
        else:
            t = str.split("^")
            t_s = t[1].split()
            if len(t_s) > 1:
                str = t[0] + "<sup>" + t_s[0] + "</sup> " + " ".join(t_s[1:])
            else:
                str = t[0] + "<sup>" + t_s[0] + " </sup>"
        str = str.replace("x", " x ")
    return str


@register.filter
@stringfilter
def superscript_replace_graph(str):
    if "^" in str:
        t = str.split("^")
        t_s = t[1].split()

        if len(t_s) > 1:
            if t_s[0] == "6":
                str = t[0] + "\u2076 " + " ".join(t_s[1:])
            elif t_s[0] == "2":
                str = t[0] + "\u00B2 " + " ".join(t_s[1:])
            elif t_s[0] == "8":
                str = t[0] + "\u2078 " + " ".join(t_s[1:])
            elif t_s[0] == "7":
                str = t[0] + "\u2077 " + " ".join(t_s[1:])
            elif t_s[0] == "5":
                str = t[0] + "\u2075 " + " ".join(t_s[1:])
            elif t_s[0] == "6":
                str = t[0] + "\u2076 " + " ".join(t_s[1:])
        else:
            str = t[0] + "<sup>" + t_s[0] + " </sup>"

    str = str.replace("x", " x ")
    return str


@register.filter
@stringfilter
def three_digit_round(string):
    if ";" in string:
        t = string.split(";")
        temp = []
        for val in t:
            val = val.strip()
            if re.search(r"(\d+\.\d{5}).*", val):
                val = round(float(val), 4)
                print(val)
                val = str(val)
                temp.append(val)
            else:
                val = str(val)
                temp.append(val)
            string = "; ".join(temp)
    elif re.search(r"(\d+\.\d{5}).*", string):
        string = round(float(string), 4)
    return string


@register.filter
@stringfilter
def download_tsv(name):
    return name + ".tsv"


@register.filter
@stringfilter
def download_xml(name):
    return name + ".xml"


@register.filter
@stringfilter
def download_json(name):
    return name + ".json"


@register.filter
@stringfilter
def source_organism_oneletter(name):
    name = name.split()
    new_name = "{}. {}".format(name[0][0], name[1])
    return new_name


@register.filter
@stringfilter
def gene_id_multipleline(name):
    if ";" in name:
        name = name.split(";")
        new_name = "<br>".join(name)
    else:
        new_name = name
    return new_name


@register.filter
@stringfilter
def threedots(name):
    if len(name) > 38:
        name = name[:38] + "..."
    return name


@register.filter
@stringfilter
def threedots_long(name):
    if len(name) > 15:
        name_split = name.split()
        name_tmp = ""
        name = ""
        for word in name:
            name_tmp = +word
            if len(name_tmp) > 13:
                name = name + "<br>" + word
    if 30 < len(name):
        name = name[:30] + "..."

    return name


@register.filter
@stringfilter
def extrachrom(name):
    if "expression" in name:
        name = "extrachrom. expression"
    return name


@register.filter
@stringfilter
def split(string, sep):
    """Return the string split by sep.

    Example usage: {{ value|split:"/" }}
    """
    return string.split(sep)


@register.filter
@stringfilter
def ionindex(name):
    if "2+" in name:
        name = name.replace("2+", "<sup>2+</sup>")
    if "3+" in name:
        name = name.replace("3+", "<sup>3+</sup>")
    if " ->" in name:
        name = name.replace("->", " &#129058; ")
    if "Kd=" in name:
        name = name.replace("Kd=", "K<sub>d</sub>=")
    return name


@register.filter
@stringfilter
def kd(name):
    new_name = name
    if "Kd=" in name:
        name = name.split("Kd")
        new_name = name[0] + "K<sub>d</sub>" + name[1]
    return new_name


@register.filter
@stringfilter
def function_pubmed_link(text):
    # < a href = "https://pubmed.ncbi.nlm.nih.gov/7989369/"
    # target = "_blank"class ="btn btn-rounded btn-info" > 7989369 < / a >
    link_pattern = '<a href = "https://pubmed.ncbi.nlm.nih.gov/\\1/"' \
                   'target = "_blank" class ="btn btn-rounded btn-info">\\1</a>'
    pubmed = re.sub(r"PubMed\:(\d+)", link_pattern, text)
    return pubmed


@register.filter
@stringfilter
def integrin_name(text):
    text = text.replace("alpha-", "&alpha;")
    text = text.replace("beta-", "&beta;")
    return text


@register.filter
@stringfilter
def structure_interactions_list(text):
    # print(text, len(text))
    if text != "-":
        links = text[1:-2]
    else:
        links = text

    return links


@register.filter
@stringfilter
def synthetic_peptide_capital(text):
    if "synthetic peptide" in text:
        text = text.replace("synthetic peptide", "Synthetic Peptide")
    return text
