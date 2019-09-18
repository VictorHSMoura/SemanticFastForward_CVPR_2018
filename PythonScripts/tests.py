import unittest
from hyperlapse import SemanticHyperlapse
from stabilizer import Stabilizer
from video import Video
from hyperlapseExceptions import InputError
import util
import os

class TestHyperlapse(unittest.TestCase):
    
    def setUp(self):
        video = Video('/home/victorhugomoura/Documents/example.mp4')

        extractor = 'face'
        velocity = 10

        self.hyperlapse = SemanticHyperlapse(video, extractor, velocity)

    def testExtractor(self):
        self.hyperlapse.checkExtractor()
        self.hyperlapse.extractor = ''
        self.assertRaises(InputError, self.hyperlapse.checkExtractor)

    def testVelocity(self):
        self.hyperlapse.checkAndSetVelocity()
        self.hyperlapse.velocity = ''
        self.assertRaises(InputError, self.hyperlapse.checkAndSetVelocity)
        self.hyperlapse.velocity = 'A'
        self.assertRaises(InputError, self.hyperlapse.checkAndSetVelocity)
        self.hyperlapse.velocity = '1'
        self.assertRaises(InputError, self.hyperlapse.checkAndSetVelocity)

    def testOpticalFlowCommand(self):
        command = self.hyperlapse.opticalFlowCommand()
        expectedCommand = './optflow -v /home/victorhugomoura/Documents/example.mp4 ' + \
            '-c default-config.xml -o /home/victorhugomoura/Documents/example.csv'

        self.assertEqual(command, expectedCommand)

    def testDarknetCommand(self):
        command = self.hyperlapse.darknetCommand()
        expectedCommand = './darknet detector demo cfg/coco.data cfg/yolo.cfg '\
            + 'yolo.weights /home/victorhugomoura/Documents/example.mp4 ' \
            + '/home/victorhugomoura/Documents/example_yolo_raw.txt'
        self.assertEqual(command, expectedCommand)

        self.hyperlapse.video = Video('/home/victorhugomoura/Documents/teste.mp4')
        command = self.hyperlapse.darknetCommand()
        expectedCommand = './darknet detector demo cfg/coco.data cfg/yolo.cfg '\
            + 'yolo.weights /home/victorhugomoura/Documents/teste.mp4 ' \
            + '/home/victorhugomoura/Documents/teste_yolo_raw.txt'
        self.assertEqual(command, expectedCommand)

    def testCheckVideoInput(self):
        self.hyperlapse.checkVideoInput()
        self.hyperlapse.video = Video('')
        self.assertRaises(InputError, self.hyperlapse.checkVideoInput)
        self.hyperlapse.video = Video('/home/victorhugomoura/Documents/example.csv')
        self.assertRaises(InputError, self.hyperlapse.checkVideoInput)
    
    def testInputError(self):
        self.hyperlapse.checkVideoInput()
        self.hyperlapse.video = Video('')
        
        try:
            self.hyperlapse.checkVideoInput()
        except InputError as IE:
            self.assertEqual(IE.__str__(), 'Please insert input video first')

class TestVideo(unittest.TestCase):
    
    def setUp(self):
        self.video = Video('/home/victorhugomoura/Documents/example.mp4')

    def testFile(self):
        self.assertEqual(self.video.file(),
                        '/home/victorhugomoura/Documents/example.mp4')

    def testName(self):
        self.assertEqual(self.video.name(), 'example.mp4')

    def testPath(self):
        self.assertEqual(self.video.path(),
                        '/home/victorhugomoura/Documents')

    def testEmpty(self):
        self.assertFalse(self.video.isEmpty())
        self.video.videofile = ''
        self.assertTrue(self.video.isEmpty())

    def testInvalid(self):
        self.assertFalse(self.video.isInvalid())
        self.video.videofile = '/home/victorhugomoura/Documents/example.csv'
        self.assertTrue(self.video.isInvalid())

class TestUtil(unittest.TestCase):

    def testCorrectPathXML(self):
        path = '/home/victorhugomoura/Documents/Folder With Spaces/example.mp4'
        expected = '"/home/victorhugomoura/Documents/Folder&#32;With&#32;'\
                + 'Spaces/example.mp4"'

        self.assertEqual(expected, util.correctPathXML(path))

    def testCorrectPath(self):
        path = '/home/victorhugomoura/Documents/Folder With Spaces/example.mp4'
        expected = '/home/victorhugomoura/Documents/Folder\ With\ Spaces/example.mp4'

        self.assertEqual(expected, util.correctPath(path))

    def testIsEmpty(self):
        string = ''
        self.assertTrue(util.isEmpty(string))

        string = 'not empty'
        self.assertFalse(util.isEmpty(string))

if __name__ == '__main__':
    unittest.main()