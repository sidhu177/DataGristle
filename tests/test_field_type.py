#!/usr/bin/env python
#  See the file "LICENSE" for the full license governing this code. 

import sys
import os
import tempfile
import random
import unittest

sys.path.append('../lib')
import field_type  as mod


def suit():
    suite = unittest.TestSuit()
    suite.addTest(unittest.makeSuite(TestSomething))

    return suite



class Test_is_integer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_integer(self):
        assert(mod.is_integer('3')         is True)
        assert(mod.is_integer('-3')        is True)
        assert(mod.is_integer(3)           is True)
        assert(mod.is_integer(-3)          is True)
        assert(mod.is_integer('b')         is False)
        assert(mod.is_integer('')          is False)
        assert(mod.is_integer(' ')         is False)
        assert(mod.is_integer('$3')        is False)
        assert(mod.is_integer('4,333.22')  is False)
        assert(mod.is_integer('33.22')     is False)
        assert(mod.is_integer(3.3)         is False)
        assert(mod.is_integer(None)        is False)


class Test_is_float(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_float(self):
        assert(mod.is_float('33.22')     is True)
        assert(mod.is_float(44.55)       is True)
        assert(mod.is_float(3)           is False)
        assert(mod.is_float(0.0)         is False)
        assert(mod.is_float(0)           is False)
        assert(mod.is_float('b')         is False)
        assert(mod.is_float('')          is False)
        assert(mod.is_float(' ')         is False)
        assert(mod.is_float('$3')        is False)
        assert(mod.is_float('4,333.22')  is False)
        assert(mod.is_float('3')         is False)
        assert(mod.is_float('-3')        is False)
        assert(mod.is_float(None)        is False)


class Test_is_string(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_string(self):
        assert(mod.is_string('b')         is True)
        assert(mod.is_string('')          is True)
        assert(mod.is_string(' ')         is True)
        assert(mod.is_string('$3')        is True)
        assert(mod.is_string('4,333.22')  is True)
        assert(mod.is_string('33.22')     is False)
        assert(mod.is_string('3')         is False)
        assert(mod.is_string('-3')        is False)
        assert(mod.is_string(3)           is False)
        assert(mod.is_string(3.3)         is False)
        assert(mod.is_string(None)        is False)

class Test_is_unknown(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_unknown(self):
        assert(mod.is_unknown('')          is True)
        assert(mod.is_unknown(' ')         is True)
        assert(mod.is_unknown('na')        is True)
        assert(mod.is_unknown('NA')        is True)
        assert(mod.is_unknown('n/a')       is True)
        assert(mod.is_unknown('N/A')       is True)
        assert(mod.is_unknown('unk')       is True)
        assert(mod.is_unknown('unknown')   is True)
        assert(mod.is_unknown('b')         is False)
        assert(mod.is_unknown('$3')        is False)
        assert(mod.is_unknown('4,333.22')  is False)
        assert(mod.is_unknown('33.22')     is False)
        assert(mod.is_unknown('3')         is False)
        assert(mod.is_unknown('-3')        is False)
        assert(mod.is_unknown(3)           is False)
        assert(mod.is_unknown(3.3)         is False)
        assert(mod.is_unknown(None)        is False)


class Test_is_timestamp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def runner(self, date):
        result, scope, pattern = mod.is_timestamp(date)
        return result, scope
 
    def test_failures(self):
        assert(self.runner("0")         == (False, None))
        assert(self.runner("-4")        == (False, None))
        assert(self.runner("-4.7")      == (False, None))
        assert(self.runner("blah")      == (False, None))
        assert(self.runner("blah")      == (False, None))
        assert(self.runner("2009 ")     == (False, None))
        assert(self.runner("2009 ")     == (False, None))

        assert(self.runner("2009-10-06-18") == (True, 'hour'))
        assert(self.runner("2009-10-06-03.02.01") == (True, 'second'))

    def test_real_dates(self):
        assert(self.runner("1172969203.1")   == (True, 'second'))

        assert(self.runner("2009")   == (True, 'year'))

        assert(self.runner("200910") == (True, 'month'))
        assert(self.runner("2009-10") == (True, 'month'))

        assert(self.runner("20090206")     == (True, 'day'))
        assert(self.runner("2009-10-06") == (True, 'day'))
        assert(self.runner("10/26/09")   == (True, 'day'))
        assert(self.runner("10-26-09")   == (True, 'day'))
        assert(self.runner("26/10/09")   == (True, 'day'))
        assert(self.runner("26-10-09")   == (True, 'day'))
        assert(self.runner("10/26/2009") == (True, 'day'))
        assert(self.runner("10-26-2009") == (True, 'day'))
        assert(self.runner("26/10/2009") == (True, 'day'))
        assert(self.runner("26-10-2009") == (True, 'day'))
        assert(self.runner("Feb 13,2009") == (True, 'day'))
        assert(self.runner("Feb 13, 2009") == (True, 'day'))
        assert(self.runner("February 13,2009") == (True, 'day'))
        assert(self.runner("February 13, 2009") == (True, 'day'))
        assert(self.runner("2009-10-06 18") == (True, 'hour'))
        assert(self.runner("2009-10-06-18") == (True, 'hour'))
        assert(self.runner("2009-10-06 18:10") == (True, 'minute'))
        assert(self.runner("2009-10-06-18.10") == (True, 'minute'))
        assert(self.runner("2009-10-06 03:02:01") == (True, 'second'))
        assert(self.runner("2009-10-06 00:00:00") == (True, 'second'))
        assert(self.runner("2009-10-06 03:02:01.01") == (True, 'microsecond'))
        assert(self.runner("2009-10-06 03:02:01.01234") == (True, 'microsecond'))



class TestGetType(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        assert(mod.get_type('n/a')  == 'unknown')
        assert(mod.get_type('UNK')  == 'unknown')
        assert(mod.get_type('unk')  == 'unknown')
        assert(mod.get_type(' ')    == 'unknown')
        assert(mod.get_type('')     == 'unknown')
        assert(mod.get_type('0')    == 'integer')
        assert(mod.get_type('1')    == 'integer')
        assert(mod.get_type('-1')   == 'integer')
        assert(mod.get_type('+1')   == 'integer')
        assert(mod.get_type('1.1')  == 'float')
        assert(mod.get_type('blah') == 'string')


class TestGetFieldType(unittest.TestCase):

    def setUp(self):
        self.type_0a = []
        self.type_0b = {}
        self.type_1a = {'Texas':   4}
        self.type_1b = ['1']
        self.type_2a = ['n/a', 'Texas']
        self.type_2b = ['n/a', '55']
        self.type_2c = ['n/a', '55.5']
        self.type_2d = ['n/a', '']
        self.type_3a = {'n/a':   3,
                        '0':     2,
                        '1.1':   4}
        self.type_3b = {'n/a':   3,
                        '0':     2,
                        'blah':  4}
        self.type_4 = {'n/a':   3,
                       'blah':  2,
                       '0':     2,
                       '1.1':   4}


    def tearDown(self):
        pass

    def test_1(self):
        assert(mod.get_field_type(self.type_0a) == 'unknown')
        assert(mod.get_field_type(self.type_0b) == 'unknown')
        assert(mod.get_field_type(self.type_1a) == 'string')
        assert(mod.get_field_type(self.type_1b) == 'integer')
        assert(mod.get_field_type(self.type_2a) == 'string')
        assert(mod.get_field_type(self.type_2b) == 'integer')
        assert(mod.get_field_type(self.type_2c) == 'float')
        assert(mod.get_field_type(self.type_2d) == 'unknown')
        assert(mod.get_field_type(self.type_3a) == 'float')
        assert(mod.get_field_type(self.type_3b) == 'unknown')
        assert(mod.get_field_type(self.type_4)  == 'unknown')



if __name__ == "__main__":
    unittest.main()


