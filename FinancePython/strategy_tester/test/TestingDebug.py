'''
Created on Dec 8, 2012

@author: phcostello
'''
import unittest
import just_a_function

class Test_withDebug(unittest.TestCase):


    def testName(self):
        
        res = just_a_function.justafunction(2)
        self.assertEqual(res, 4, 'problem')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()