# (c) Copyright 2017 Zymergen, Inc.
# All rights reserved.

from requests import get

# some chemical properties that can be queried in PubChem:
CHARGE = 'Charge'
EXACT_MASS = 'ExactMass'
INCHI_KEY = 'InChIKey'
IUPAC_NAME = 'IUPACName'
MOLECULAR_FORMULA = 'MolecularFormula'
MOLECULAR_WEIGHT = 'MolecularWeight'
# other valid valid properties that can be queried are listed here:
# https://pubchem.ncbi.nlm.nih.gov/pug_rest/PUG_REST.html#_Toc458584223)

# Helper module for looking up chemical property information in PubChem.


def get_molecular_formula_by_cid(cid):
    """
    Find the molecular formula of a compound.

    Args:
        cid: A PubChem CID (e.g., 5793 for glucose), which must be numeric.

    Returns:
        The conventional representation of the compound's molecular formula
        as a string.
    """

    properties = get_properties_by_cid(cid, [MOLECULAR_FORMULA])
    return properties[MOLECULAR_FORMULA]


def get_properties_by_cid(cid, properties_list):
    """
    Lookup one or more chemical properites of a compound.

    Args:
        cid: A PubChem CID (e.g., 5793 for glucose), which must be numeric.
        properties_list: A list of property name strings to lookup.

    Returns:
        A dictionary of chemical properties where keys are property names
        and values are the associated property values for the passed CID.
    """

    url = build_url(cid, properties_list)
    return get_response_properties(url)


def get_response_properties(url):
    """
    Make the request to PubChem and return the results as a dictionary.

    Args:
        url: A formatted PubChem query string.

    Returns:
        A dictionary of chemical properties where keys are property names
        and values are the associated property values for the passed CID.

    """
    response = get(url)
    results = response.json()
    return results["PropertyTable"]["Properties"][0]


def build_url(cid, properties_list):
    """
    Create a PubChem query string for looking up properties by CID.

    Args:
        cid: A PubChem CID (e.g., 5793 for glucose), which must be numeric.
        properties_list: A list of property names as strings.

    Returns:
         A correctly formatted PubChem query string.

    Raises:
        Value Error if a non-numeric CID is passed or the
        properties_list is not a list.
    """

    if not isinstance(properties_list, list):
        raise ValueError('Expected a list of property names. Received: %s.'
                         % properties_list)

    if not isinstance(cid, (long, int)):
        raise ValueError('The CID must be numeric.')

    properties_str = ",".join(properties_list)
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" \
               "%s/property/%s/JSON"
    url = base_url % (cid, properties_str)
    return url


if __name__ == "__main__":
    # get the molecular formula of aspirin
    print '\nThe molecular formula of aspirin is', get_molecular_formula_by_cid(2244)

    # get a list of chemical properties associated with aspirin
    chem_props = [MOLECULAR_FORMULA, MOLECULAR_WEIGHT, CHARGE, EXACT_MASS,
                  IUPAC_NAME, INCHI_KEY]
    chem_prop_values = get_properties_by_cid(2244, chem_props)
    print '\nA list chemical properties associated with aspirin:'
    for prop in chem_prop_values:
        print '%s: %s' % (prop, chem_prop_values[prop])
