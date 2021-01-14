import cv2
from cv2 import VideoWriter, VideoWriter_fourcc, VideoCapture

class Processer:
    def __init__(self, input_file, output_file, FPS=30, max_count=-1):
        self.vidcap = VideoCapture(input_file)
        success, self.image = self.vidcap.read()
        self.width = int(self.vidcap.get(4))
        self.height = int(self.vidcap.get(3))
        fourcc = VideoWriter_fourcc(*'XVID')
        self.videoWriter = VideoWriter(output_file, fourcc, float(FPS), (self.height, self.width))
        self.max_count = max_count

    def run(self, proc_func, end_proc=None):
        count = 0
        success = True
        while success and (count < self.max_count or self.max_count == -1):
            proc_func(self.image, count, self.width, self.height, self.videoWriter)
            success, self.image = self.vidcap.read()
            print('Count:', count)
            count += 1

        if end_proc is not None:
            end_proc(self.videoWriter)
        self.videoWriter.release()
        self.vidcap.release()
        print('Total count:', count)
