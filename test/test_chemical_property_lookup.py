# (c) Copyright 2017 Zymergen, Inc.
# All rights reserved.

import unittest  # You must import this package

# You must also import the code you want to test
from chemical_module.chemical_property_lookup import get_properties_by_cid
from chemical_module.chemical_property_lookup import get_molecular_formula_by_cid
from chemical_module.chemical_property_lookup import get_response_properties

MOL_FORM_QUERY_STR = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/' \
                     'property/MolecularFormula/JSON'


class TestChemicalPropertyLookup(unittest.TestCase):
    """ These unit tests do not test with mock. """

    def setUp(self):
        """
        The setUp method is executed BEFORE each test method in a class is run.
        Similiarly a tearDown method can be implmented, which will run AFTER
        each test method in a class is run.
        """

        # set expected values for aspirin
        self.aspirin_cid = 2244
        self.expected_mol_form = 'C9H8O4'
        self.expected_InChIKey = 'BSYNRYMUTXBXSQ-UHFFFAOYSA-N'
        self.expected_mol_wt = 180.159
        self.expected_exact_mass = 180.042
        self.expected_charge = 0
        self.expected_IUPACName = '2-acetyloxybenzoic acid'

    def test_get_molecular_formula(self):
        """Verify the correct molecular formula is returned for aspirin."""

        mol_form = get_molecular_formula_by_cid(self.aspirin_cid)  # external API call
        self.assertEqual(self.expected_mol_form, mol_form)

    def test_get_molecular_formula_raises_exception_with_invalid_cid(self):
        """Verify the expected exception is raised when CID is invalid."""

        invalid_cid = 'Not a CID'
        # check that an Exception is raised
        with self.assertRaises(Exception):
            get_molecular_formula_by_cid(invalid_cid)
        # you can also check the specific type
        with self.assertRaises(ValueError):
            get_molecular_formula_by_cid(invalid_cid)
        # along with the expected message
        with self.assertRaisesRegexp(ValueError, 'The CID must be numeric.'):
            get_molecular_formula_by_cid(invalid_cid)
        # or a partial message
        with self.assertRaisesRegexp(ValueError, r'must be numeric+'):
            get_molecular_formula_by_cid(invalid_cid)

    def test_get_properties(self):
        """Verify the correct values are returned for aspirin."""

        properties = ['InChIKey', 'MolecularFormula', 'MolecularWeight']

        expected_values = {'CID': self.aspirin_cid,
                           'InChIKey': self.expected_InChIKey,
                           'MolecularFormula': self.expected_mol_form,
                           'MolecularWeight': self.expected_mol_wt}

        values = get_properties_by_cid(self.aspirin_cid, properties)  # External API call
        self.assertDictEqual(expected_values, values)

    def test_get_properties_raises_exception_with_invalid_cid(self):
        """Verify the expected exception is raised when CID is invalid."""

        invalid_cid = 'Still not a CID'
        # check the specific exception type and the expected error message
        with self.assertRaisesRegexp(ValueError, 'The CID must be numeric.'):
            get_molecular_formula_by_cid(invalid_cid)

    def test_get_response_properties(self):
        """Verify the expected response of property values is returned for aspirin."""

        properties_to_query = 'MolecularFormula,InChIKey,MolecularFormula,' \
                              'MolecularWeight,ExactMass,Charge,IUPACName'

        multi_prop_query_str = \
            'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/' \
            'property/%s/JSON' % properties_to_query

        expected_properties_dict = {'CID': self.aspirin_cid,
                                    'InChIKey': self.expected_InChIKey,
                                    'MolecularFormula': self.expected_mol_form,
                                    'MolecularWeight': self.expected_mol_wt,
                                    'ExactMass': self.expected_exact_mass,
                                    'Charge': self.expected_charge,
                                    'IUPACName': self.expected_IUPACName}

        values = get_response_properties(multi_prop_query_str)  # External API call
        self.assertDictEqual(expected_properties_dict, values)

    def test_get_properties_raises_exception_with_invalid_properties(self):
        """Verify the expected exception is raised when a list is not provided."""

        invalid_prop_list = 'Not a list'

        # check the specific exception type and the expected error message
        expected_error = 'Expected a list of property names. Received: Not a list.'
        with self.assertRaisesRegexp(ValueError, expected_error):
            get_properties_by_cid(self.aspirin_cid, invalid_prop_list)


if __name__ == '__main__':
    unittest.main()
