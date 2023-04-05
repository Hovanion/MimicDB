import os

from io import StringIO
from django.urls import reverse
from xml.dom.minidom import parseString
from cairosvg import svg2png

# Only these elments will be recognized for alteration.
ELEMENTS = ['rect', 'ellipse', 'path']

# Map SVG element names to the Alpha monomer Structures it includes.
ALPHA_DOMAIN_MAPPING = {
    "TMa_body": ["TMa"],
    "TMa_cap": ["TMa"],
    "alpha-I": ["alpha-I"],
    "bP_body": ["bP1", "bP2", "bP3", "bP4", "bP5", "bP6", "bP7"],
    "bP_cap": ["bP1", "bP2", "bP3", "bP4", "bP5", "bP6", "bP7"],
    "calf1": ["calf1"],
    "calf2": ["calf2"],
    "cyta_body": ["cyta"],
    "cyta_cap": ["cyta"],
    "thigh": ["thigh"],
}

# Map SVG element names to the Beta monomer Structures it includes.
BETA_DOMAIN_MAPPING = {
    "EGF1": ["EGF1"],
    "EGF2": ["EGF2"],
    "EGF3": ["EGF3"],
    "EGF4": ["EGF4"],
    "Hyb": ["Hyb1", "Hyb2"],
    "PSI": ["PSI"],
    "bT": ["bT"],
    "TMb_body": ["TMb"],
    "TMb_cap": ["TMb"],
    "beta-I": ["beta-I"],
    "cytb_body": ["cytb"],
    "cytb_cap": ["cytb"],
}

# This is the linker that connects the Alpha-I Domain. This element is delted
# if this is not an Alpha subunit with an Alpha-I domain.
ALPHA_I_LINK = "alpha-I-link"

# Colormap for Alpha subunit
ALPHA_COLORMAP = {
    0: ("#f7fbff", "#deebf7"),
    1: ("#2171b5", "#08519c"),
}
# Colormap for Beta subunit
BETA_COLORMAP = {
    0: ("#fff5f0", "#fee0d2"),
    1: ("#ef3b2c", "#cb181d"),
}


ELEMENT_NAMES = {}
ALL_DOMAIN_MAPPING = {**ALPHA_DOMAIN_MAPPING, **BETA_DOMAIN_MAPPING}

# Manually assign names for Domains :-(
ELEMENT_NAMES = {
    'Hyb': "Hybrid domain",
    'bP_cap': "Beta propeller",
    'bP_body': "Beta propeller",
    'alpha-I': 'Inserted interaction domain alpha-I',
    'thigh': 'Thigh domain',
    'calf1': 'Calf domain 1',
    'calf2': 'Calf domain 2',
    'TMa_body': 'Transmembrane',
    'TMa_cap': 'Transmembrane',
    'cyta_body': 'Cytoplasmic tail',
    'cyta_cap': 'Cytoplasmic tail',
    'PSI': 'PSI domain',
    'beta-I': 'Interaction domain beta-I',
    'EGF1': 'EGF-like module 1',
    'EGF2': 'EGF-like module 2',
    'EGF3': 'EGF-like module 3',
    'EGF4': 'EGF-like module 4',
    'bT': 'Beta-tail domain',
    'TMb_cap': 'Transmembrane',
    'TMb_body': 'Transmembrane',
    'cytb_cap': 'Cytoplasmic tail',
    'cytb_body': 'Cytoplasmic tail',
}


class IntegrinDiagram(object):
    """ A class to manage manipulating the Integrin diagram.

    Args:
        filename: The name of the IntegrinDiagram. Default = 'integrin.svg'

    This module is very tighyly coupled to the exact Integrin diagram that this
    module was designed for. In brief, it can be any .svg image file, and
    operations are applied on the elemens with identified by their "ID".

    In general this script will alter the colors of any object by ID.

    If an object with this ID is not found, nothing is modified.

    Searches all elements which are 'path', 'ellipse', or 'rect'.

    Example use:

    >>> integrin = IntegrinDiagram("integrin.svg")
    >>> integrin.color_domain_fill('cyta', '#FF0000')
    >>> integrin.color_domain_stroke('cyta', '#FF0000')
    >>> integrin.color_domain_stroke('cytb', fill='#FF0000', stroke='#00FFFF')
    >>> integrin.save("new_integrin.svg")

    """

    def __init__(self, filename='./integrin.svg'):

        path = os.path.dirname(os.path.abspath(__file__))

        # Set filename, and parse it.
        self._filename = os.path.join(path, filename)
        self._parse_file()

    def _parse_file(self):
        """ Parse self._filename is an XML object, and store the
        minidom.Document object in self._dom.
        """

        o = open(self._filename, 'r')
        xml = o.read()
        o.close()
        self._dom = parseString(xml)

    def _style_to_dict(self, style):
        """ Convert the string of an svg style attributes to a dictionary, and
        return it.

        Args:
            style (str): An svg formatted style attribute

        Returns:
            sdict (dict): A dictionary representing the style string

        This function assumes that each key:value pair is separated by a ";",
        and that the key and value are separated by a ";".
        """

        sdict = {}
        for kv in style.split(";"):
            k, v = kv.split(":")
            sdict[k] = v
        return sdict

    def _dict_to_style(self, sdict):
        """ Convert a dictionary to a string formatted as an svg style, and
        return it.

        Args:
            sdict (dict): A dictionary representing an svg style attribute

        Returns:
            style (str): A string that can be used as an svg style string

        This function will return any dictionary, formatted to use ":" as a
        separator between key and value, and ";" between key:value pairs.
        """

        style = []
        for k, v in sdict.items():
            style.append("{0}:{1}".format(k, v))
        return ";".join(style)

    def add_attr(self, elem_id, attr, value):
        """ Add an attribute/value pair.
        Args:
            elem_id (str): The ID of the element to change
            attr(str): The attribute to change
            value (str): The value to assign
        """

        elements = []

        for ELM in ELEMENTS:
            elements.extend(
                self._dom.getElementsByTagName(ELM)
            )

        for element in elements:
            if element.getAttribute('id') == elem_id:
                print("set: {0} to {1}".format(elem_id, value))
                element.setAttribute(attr, value)

    def remove_element(self, elem_id):
        """ Remove a node from the tree.
        Args:
            elem_id (str): The ID of the element to remove
        """

        elements = []

        for ELM in ELEMENTS:
            elements.extend(
                self._dom.getElementsByTagName(ELM)
            )

        for element in elements:
            if element.getAttribute('id') == elem_id:
                parent = element.parentNode
                parent.removeChild(element)

    def change_element_style(self, elem_id, attr, value):
        """ Change the a style attribute of an element in self._dom.

        NOTE: at the moment, it only searches for elements defined in the
        ELEMENTS variable (rect, path and ellipse)

        Args:
            elem_id (str): The ID of the element to change
            attr(str): The style attribute to change
            value (str): The value to assign

        """

        elements = []

        for ELM in ELEMENTS:
            elements.extend(
                self._dom.getElementsByTagName(ELM)
            )

        changed = 0

        for element in elements:
            if element.getAttribute('id') == elem_id:

                style = element.getAttribute('style')

                sdict = self._style_to_dict(style)
                sdict[attr] = value

                style = self._dict_to_style(sdict)

                element.setAttribute('style', style)

                changed += 1

        if changed == 0:
            raise Exception(
                "Could not find an element '{0}' in file!".format(elem_id)
            )

    def save_svg(self, filename):
        """ Save the IntegrinDiagram object to an svg file.

        Args:
            filename: Filename/path to save the svg to.
        """

        o = open(filename, 'w')
        self._dom.writexml(o)
        o.close()

    def save_png(self, filename):
        """ Save the IntegrinDiagram object to a png file.

        Args:
            filename: Filename/path to save the png to.

	This function uses the Cairo library (cairosvg) to convert the diagram
        to a png (via scg2png).
	"""

        stringio = StringIO(self.get_xml_str())

        svg2png(file_obj=stringio, write_to=filename)

    def get_xml_str(self):
        """ Return the xml string
        """

        return self._dom.toxml()


def build_dimer_thumbnail(dimer, filepath):
    """ Helper function that builds a Dimer object thumbnail, and saves it

    Args:
        dimer (obj:`Dimer`): The Dimer object to create a thumbnail for
        filepath (str): The location to save the file to.
    """

    diagram = IntegrinDiagram()

    for element, domains in ALPHA_DOMAIN_MAPPING.items():

        alpha_pbds = dimer.alpha.pdb_alpha.filter(
            alpha_domain__short__in=domains
            ).distinct()

        present = bool(alpha_pbds.count())

        diagram.change_element_style(
            element, 'fill', ALPHA_COLORMAP[present][0]
        )
        diagram.change_element_style(
            element, 'stroke', ALPHA_COLORMAP[present][1]
        )

    for element, domains in BETA_DOMAIN_MAPPING.items():

        beta_pbds = dimer.beta.pdb_beta.filter(
            beta_domain__short__in=domains
            ).distinct()

        present = bool(beta_pbds.count())

        diagram.change_element_style(
            element, 'fill', BETA_COLORMAP[present][0]
        )
        diagram.change_element_style(
            element, 'stroke', BETA_COLORMAP[present][1]
        )

    if not dimer.alpha.structure.filter(short="alpha-I"):
        diagram.remove_element("alpha-I")
        diagram.remove_element(ALPHA_I_LINK)

    diagram.save_png(filepath)


def build_dimer_diagram(dimer):
    """ Helper function that builds and returns the IntegrinDiagram object for
    the Dimer page.
    """

    def build_popover_content(pdbs):
        content = "<p><strong>Pdbs:</strong></p><ul>"

        if pdbs:
            for pdb in pdbs:
                content += (
                    "<li><a href='{0}'>{1}</a></li>".format(
                        reverse("pdb", args=[pdb.pdb]), pdb.pdb
                    )
                )
            content += "</ul>"
        else:

            content += "<p><strong>Pdbs:</strong>(none)</p>"
        return content

    diagram = IntegrinDiagram()

    for element, domains in ALPHA_DOMAIN_MAPPING.items():

        alpha_pbds = dimer.alpha.pdb_alpha.filter(
            alpha_domain__short__in=domains
            ).distinct()

        present = bool(alpha_pbds.count())

        diagram.change_element_style(
            element, 'fill', ALPHA_COLORMAP[present][0]
        )
        diagram.change_element_style(
            element, 'stroke', ALPHA_COLORMAP[present][1]
        )

        if present:

            content = build_popover_content(alpha_pbds)

            diagram.add_attr(element, 'data-toggle', 'popover',)
            diagram.add_attr(element, 'data-placement', 'right',)
            diagram.add_attr(element, 'data-title', ELEMENT_NAMES[element])
            diagram.add_attr(element, 'data-content', content)

    for element, domains in BETA_DOMAIN_MAPPING.items():

        beta_pbds = dimer.beta.pdb_beta.filter(
            beta_domain__short__in=domains
            ).distinct()

        present = bool(beta_pbds.count())

        diagram.change_element_style(
            element, 'fill', BETA_COLORMAP[present][0]
        )
        diagram.change_element_style(
            element, 'stroke', BETA_COLORMAP[present][1]
        )

        content = build_popover_content(beta_pbds)

        if present:

            diagram.add_attr(element, 'data-toggle', 'popover',)
            diagram.add_attr(element, 'data-placement', 'right',)
            diagram.add_attr(element, 'data-title', ELEMENT_NAMES[element])
            diagram.add_attr(element, 'data-content', content)

    if not dimer.alpha.structure.filter(short="alpha-I"):
        diagram.remove_element("alpha-I")
        diagram.remove_element(ALPHA_I_LINK)

    return diagram.get_xml_str()


def build_pdb_diagram(pdb):
    """ Helper function that builds and returns the IntegrinDiagram object for
    the Dimer page.
    """

    diagram = IntegrinDiagram()

    for element, domains in ALPHA_DOMAIN_MAPPING.items():

        alpha_pbds = pdb.alpha_domain.filter(short__in=domains)

        present = bool(alpha_pbds.count())

        diagram.change_element_style(
            element, 'fill', ALPHA_COLORMAP[present][0]
        )
        diagram.change_element_style(
            element, 'stroke', ALPHA_COLORMAP[present][1]
        )

        if present:

            diagram.add_attr(element, 'data-toggle', 'popover',)
            diagram.add_attr(element, 'data-placement', 'right',)
            diagram.add_attr(element, 'data-content', ELEMENT_NAMES[element])

    for element, domains in BETA_DOMAIN_MAPPING.items():

        beta_pbds = pdb.beta_domain.filter(short__in=domains)

        present = bool(beta_pbds.count())

        diagram.change_element_style(
            element, 'fill', BETA_COLORMAP[present][0]
        )
        diagram.change_element_style(
            element, 'stroke', BETA_COLORMAP[present][1]
        )

        if present:

            diagram.add_attr(element, 'data-toggle', 'popover',)
            diagram.add_attr(element, 'data-placement', 'right',)
            diagram.add_attr(element, 'data-content', ELEMENT_NAMES[element])

    return diagram.get_xml_str()

if __name__ == "__main__":

    diag = IntegrinDiagram('integrin.svg')
    diag.change_element_style('calf2', 'fill', '#0000ff')
    diag.change_element_style('calf2', 'stroke', '#00ff00')
    diag.save("integrin_calf2.svg")
