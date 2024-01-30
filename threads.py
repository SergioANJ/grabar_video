# opening video capture stream
vcap = cv2.VideoCapture(0)
if vcap.isOpened() is False :
  print("[Exiting]: Error accessing webcam stream.")
  exit(0)
fps_input_stream = int(vcap.get(5)) # get fps of the hardware
print("FPS of input stream{}".format(fps_input_stream))
grabbed, frame = vcap.read() # reading single frame for initialization/ hardware warm-up