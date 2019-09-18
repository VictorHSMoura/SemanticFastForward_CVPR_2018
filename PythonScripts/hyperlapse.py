import matlab.engine
import os
from subprocess import Popen, PIPE, STDOUT
from hyperlapseExceptions import InputError, BuildError
from video import Video
import util
import sys
sys.path.insert(0, '..')

import generate_yolo_descriptor

#don't cover functions that create or check if a file exists
class SemanticHyperlapse(object):
    def __init__(self, video, extractor, velocity):
        self.video = video
        self.path = os.getcwd()
        self.extractor = extractor
        self.velocity = velocity
        self.maxVel = 10 * velocity

        self.checkParameters()

    def checkExtractor(self):
        if util.isEmpty(self.extractor):
            raise InputError('Please select an extractor')

    def checkAndSetVelocity(self):
        if util.isEmpty(self.velocity):
            raise InputError('Please insert speedup')
        try:
            self.isVelocityValidNumber()
            self.velocity = float(int(self.velocity))
        except ValueError:
            raise InputError('Invalid speedup value')
    
    def checkVideoInput(self):
        self.video.checkInput()

    def isVelocityValidNumber(self):
        velocity = int(self.velocity) #raises ValueError if it isn't a number
        if velocity <= 1:
            raise InputError('Error: speedup <= 1')

    def checkStabilizer(self): # pragma: no cover
        buildFolder = '_SemanticFastForward_JVCI_2018/AcceleratedVideoStabilizer/build'
        if not os.path.isdir(buildFolder) or not os.path.isfile(buildFolder +'/VideoStabilization'):
            raise BuildError('Please compile the Stabilizer and run it again.\n')

    def checkDarknet(self): # pragma: no cover
        darknet = '_Darknet/darknet'
        if not os.path.isfile(darknet):
            raise BuildError('Please compile the Darknet and run it again.\n')

    def opticalFlowExists(self): # pragma: no cover
        videoFile = self.video.file()
        outputFile = videoFile[:-4] + '.csv'

        return os.path.isfile(outputFile)

    def opticalFlowCommand(self):
        videoFile =  util.correctPath(self.video.file())
        command = './optflow'
        videoParam = ' -v ' + videoFile
        configParam = ' -c default-config.xml'
        outputParam = ' -o ' + videoFile[:-4] + '.csv'

        fullCommand = command + videoParam + configParam + outputParam
        
        return fullCommand

    def runOpticalFlow(self): # pragma: no cover
        os.chdir('_SemanticFastForward_JVCI_2018/Vid2OpticalFlowCSV')

        if not self.opticalFlowExists():
            os.system(self.opticalFlowCommand())
        else:
            print 'OpticalFlow already extracted.'
        
        os.chdir(self.path)

    def getSemanticInfo(self, eng): # pragma: no cover
        eng.cd('_SemanticFastForward_JVCI_2018/SemanticScripts')
        eng.addpath(self.path)
        eng.addpath(self.video.path())
        eng.addpath(os.getcwd())
        
        eng.ExtractAndSave(self.video.file(), self.extractor, nargout=0)
        eng.cd(self.path)

        eng.generate_transistion_costs(
            self.video.file(), self.velocity, self.extractor, nargout=0
        )

    def yoloFileExists(self, sufix): # pragma: no cover
        videoFile = self.video.file()
        outputFile = videoFile[:-4] + sufix

        return os.path.isfile(outputFile)

    def darknetCommand(self):
        videoFile = ' ' + util.correctPath(self.video.file())
        command = './darknet'
        parameters = ' detector demo'
        cfgs = ' cfg/coco.data cfg/yolo.cfg'
        weights = ' yolo.weights'
        output = videoFile[:-4] + '_yolo_raw.txt'

        fullCommand = command + parameters + cfgs + weights + videoFile + output

        return fullCommand

    def yoloExtraction(self): # pragma: no cover
        os.chdir('_Darknet')

        if not self.yoloFileExists('_yolo_raw.txt'):
            os.system(self.darknetCommand())
        else:
            print('Yolo Extraction already done.')

        if not self.yoloFileExists('_yolo_desc.csv'):
            generate_yolo_descriptor.run(
                self.video.file(), self.video.file()[:-4] + '_yolo_raw.txt',
                self.video.file()[:-4] + '_yolo_desc.csv'
            )
        else:
            print('Yolo Descriptor already done.')

        os.chdir(self.path)

    def generateXML(self, acceleratedVideo): # pragma: no cover
        videoPath = util.correctPathXML(acceleratedVideo.path())
        videoName = util.correctPathXML(acceleratedVideo.name())
        videoFile = util.correctPathXML(acceleratedVideo.file())
        oldVideoFile = util.correctPathXML(self.video.file())
        velocity = str(int(self.velocity))
        
        xmlFile = 'experiment_hyperlapse.xml'
        tags = [
            'video_path', 'video_name', 'output_path', 'original_video_filename',
            'selected_frames_filename', 'read_masterframes_filename',
            'semantic_costs_filename',  'segmentSize', 'runningParallel',
            'saveMasterFramesInDisk', 'saveVideoInDisk'
        ]

        values = [
            videoPath, videoName, videoPath, oldVideoFile,
            videoFile[:-5] + '_AppearanceCost_selected_frames.csv"', '',
            oldVideoFile[:-5] + '_SemanticCosts.csv"',
            '4', 'true', 'true', 'true']

        file = open(xmlFile, 'w')
        file.write('<?xml version=\"1.0\" ?>\n<opencv_storage>\n')
        for i in range(len(tags)):
            file.write('\t<' + tags[i] + '>\n')
            file.write('\t\t' + values[i] + '\n')
            file.write('\t</' + tags[i] + '>\n\n')
        file.write('</opencv_storage>\n')
        file.close()

        return xmlFile

    def speedUp(self, eng): # pragma: no cover
        eng.addpath(os.getcwd())
        eng.addpath('LLC')
        
        [frames, videoName] = eng.accelerate_video_LLC(
            self.video.file(), self.extractor, 'Speedup', self.velocity,
            'GenerateVideo', True, nargout=2
        )
        return videoName

    def runStabilization(self, xmlFile): # pragma: no cover
        os.chdir('build')
        os.system('./VideoStabilization ' + "../" + xmlFile)

    def checkDependencies(self): # pragma: no cover
        self.checkStabilizer()
        self.checkDarknet()

    def checkParameters(self):
        self.checkVideoInput()
        self.checkExtractor()
        self.checkAndSetVelocity()

    def speedUpPart(self, writeFunction): # pragma: no cover
        write = writeFunction
        
        write('1/7 - Running Optical Flow\n', 'title')
        self.runOpticalFlow()
    
        write('2/7 - Starting Matlab\n', 'title')
        eng = matlab.engine.start_matlab('-nodisplay')
    
        write('3/7 - Getting Semantic Info\n', 'title')
        self.getSemanticInfo(eng)

        write('4/7 - Extracting Yolo Info\n', 'title')
        self.yoloExtraction()
        
        write('5/7 - Speeding-Up Video\n', 'title')
        videoName = self.speedUp(eng)
        eng.quit()
    
        return Video(videoName + '.avi')

    def stabilizePart(self, acceleratedVideo, writeFunction): # pragma: no cover
        write = writeFunction
        write('6/7 - Stabilizing\n', 'title')

        os.chdir('_SemanticFastForward_JVCI_2018/AcceleratedVideoStabilizer')
        xmlFile = self.generateXML(acceleratedVideo)
        self.runStabilization(xmlFile)

        write('7/7 - Finished\n', 'title')
        os.chdir(self.path)

    def run(self, writeFunction): # pragma: no cover
        self.checkDependencies()
        acceleratedVideo = self.speedUpPart(writeFunction)
        self.stabilizePart(acceleratedVideo, writeFunction)