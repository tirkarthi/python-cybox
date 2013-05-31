# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import cybox.test
import cybox.utils


class ObjectTestCase(object):
    """A base class for testing all subclasses of ObjectProperties.

    Each subclass of ObjectTestCase should subclass both unittest.TestCase
    and ObjectTestCase, and defined two class-level fields:
    - klass: the ObjectProperties subclass being tested
    - object_type: The name prefix used in the XML Schema bindings for the
      object.
    """

    def test_type_exists(self):
        # Verify that the correct class has been added to the OBJECT_TYPES_DICT
        # dictionary in cybox.utils.nsparser

        # Skip this base class
        if type(self) == type(ObjectTestCase):
            return

        t = self.__class__.object_type

        expected_class = cybox.utils.get_class_for_object_type(t)
        actual_class = self.__class__.klass

        self.assertEqual(expected_class, actual_class)

        expected_namespace = expected_class._XSI_NS
        actual_namespace = cybox.utils.nsparser.OBJECT_TYPES_DICT.get(t).get('namespace_prefix')
        self.assertEqual(expected_namespace, actual_namespace)

        self.assertEqual(expected_class._XSI_TYPE, t)

    def test_object_reference(self):
        klass = self.__class__.klass

        ref_dict = {'object_reference': "some:object-reference-1",
                    'xsi:type': klass._XSI_TYPE}

        ref_dict2 = cybox.test.round_trip_dict(klass, ref_dict)
        print klass.from_dict(ref_dict).to_xml()
        # Some "missing" attributes are required, so don't check for complete
        # equality
        #self.assertEqual(ref_dict, ref_dict2)
        self.assertEqual(ref_dict['object_reference'], ref_dict2['object_reference'])
        self.assertEqual(ref_dict['xsi:type'], ref_dict2['xsi:type'])
