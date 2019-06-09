import unittest


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        print
        '-- setUp --'

    def tearDown(self):
        print('-- tearDown --')

    def checkDefaultSize(self):
        print('-- checkDefaultSize --')
        assert 50 == 50, 'equal'

    def checkResize(self):
        print('-- checkResize --')
        assert 50 == 60, 'not equal'


# Fancy way to build a suite
class WidgetTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self, map(WidgetTestCase,
                                              ("checkDefaultSize",
                                               "checkResize")))


# Simpler way
def makeWidgetTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase("checkDefaultSize"))
    suite.addTest(WidgetTestCase("checkResize"))
    return suite


# Make this test module runnable from the command prompt
if __name__ == "__main__":
    # demo-01
    print('demo-01')
    case1 = WidgetTestCase('checkDefaultSize')
    case1.run()

    # demo-02
    print('demo-02')
    case2 = WidgetTestCase('checkResize')
    case2()

    # demo-03
    print('demo-03')
    unittest.TextTestRunner().run(makeWidgetTestSuite())

    # demo-04
    print('demo-04')
    unittest.TextTestRunner().run(WidgetTestSuite())

    # demo-05
    print('demo-05')
    unittest.TextTestRunner().run(unittest.makeSuite(WidgetTestCase, 'check'))