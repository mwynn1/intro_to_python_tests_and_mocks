# (c) Copyright 2017 Zymergen, Inc.
# All rights reserved.

from mock import patch, Mock
import requests_mock
import unittest

from chemical_module.chemical_property_lookup import get_molecular_formula_by_cid


MOL_FORM_QUERY_STR = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/' \
                     'property/MolecularFormula/JSON'


class TestChemicalPropertyLookupWithMocks(unittest.TestCase):
    """ These unit tests use mocks. """

    def setUp(self):
        """
        The setUp method is executed BEFORE each test method in a class is run.
        Similarly, a tearDown method can be implmented, which will run AFTER
        each test method in a class is run.
        """

        # set expected values for aspirin
        self.aspirin_cid = 2244
        self.expected_mol_form = 'C9H8O4'

    # Questions:
    # What do you think about this mock?
    # What is it testing?
    # Might this be an "over-mock"? Why or why not?
    # Can you suggest another way to test this function?
    @patch('chemical_module.chemical_property_lookup.get_properties_by_cid')
    def test_get_molecular_formula_first_mock(self, get_properties_mock):
        """
            Verify the correct molecular formula is returned for aspirin.

            The code we're mocking looks like this, which is executed from
            within get_molecular_formula_by_cid:

                properties = get_properties_by_cid(cid, [MOLECULAR_FORMULA])
        """

        # mock the return value of get_properties_mock
        get_properties_mock.return_value = {'MolecularFormula': 'C9H8O4'}

        # did we get expected formula?
        mol_form = get_molecular_formula_by_cid(self.aspirin_cid)
        self.assertEqual(self.expected_mol_form, mol_form)

        # was the mock called as expected?
        get_properties_mock.assert_called()
        get_properties_mock.assert_called_with(self.aspirin_cid, ['MolecularFormula'])

    # Here's another way we could mock the same function
    # @patch('requests.get')                                # Note: this will not work
    @patch('chemical_module.chemical_property_lookup.get')  # this will!
    def test_get_molecular_formula_second_mock(self, mock_get):
        """
        Verify the correct molecular formula is returned for aspirin.

        The code we're trying to mock looks like:

            response = get(url)
            results = response.json()

        Thus, we need our mock_get function to return an object with a
        function that returns the json that our test expects to see.  We
        set the return_value of our mock object to be a stub of a class with
        the expected .json() function.
        """

        # Our mock_results class is a mock with a method, json, which returns
        # our expected json
        mock_results = Mock()
        mock_results.json.return_value = \
            {'PropertyTable': {'Properties': [{'MolecularFormula': 'C9H8O4'}]}}

        # When get() is called, our mock results are returned and no
        # external API call is made
        mock_get.return_value = mock_results

        # now call the function we are testing
        mol_form = get_molecular_formula_by_cid(self.aspirin_cid)

        # We can both check that our mock was called and that our function
        # took the result of the mock and returned the correct information
        mock_results.json.assert_called()
        mock_get.assert_called_with(MOL_FORM_QUERY_STR)
        self.assertEqual(self.expected_mol_form, mol_form)

    # And here's yet another way we mock the same function.
    @requests_mock.mock()  # another way to mock a request!
    def test_get_molecular_formula_third_mock(self, mock_req):
        """
        Verify the correct molecular formula is returned for aspirin.

        The code we're trying to mock looks like:

            response = get(url)
            results = response.json()

        Thus, we need our mock_get function to return an object with a
        function that returns the json that our test expects to see.  We
        set the return_value of our mock object to be a stub of a class with
        the expected .json() function.
        """

        # The requests object will be mocked. When get() is called, the request will
        # contain the information we set here
        mock_req.get(MOL_FORM_QUERY_STR,
                     text='{"PropertyTable": {"Properties": [{"MolecularFormula": '
                          '"C9H8O4", "CID": 2244}]}}')

        mol_form = get_molecular_formula_by_cid(self.aspirin_cid)
        self.assertEqual(True, mock_req.called)
        self.assertEqual(1, mock_req.call_count)
        self.assertEqual(self.expected_mol_form, mol_form)

    # Questions to consider:
    #   1. are the second and third mocks better than the first? Why or why not?
    #   2. what is different between the 2nd and 3rd mock?  Is one better? Why or why not?
    #   3. How else might we test the chemical_property_lookup module with or without mocks?


if __name__ == '__main__':
    unittest.main()
