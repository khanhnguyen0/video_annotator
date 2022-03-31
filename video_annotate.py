import cv2
import torch
import pafy
from matplotlib import cm
import click



def plot_boxes(image, model, confidence_threshold):
    """Plot boxes on an image"""
    results = model(image)
    for _, (xmin, ymin, xmax, ymax, confidence, class_idx, class_name) in results.pandas().xyxy[0].iterrows():
        if confidence < confidence_threshold:
            # Only display boxes when the model is highly confident
            continue
        xmin, xmax = int(xmin), int(xmax)
        ymin, ymax = int(ymin), int(ymax)
        blue, green, red, _ = cm.get_cmap('tab10_r')(class_idx)
        background_color = blue*255, green*255, red*255
        text_label = f"{class_name} ({confidence:.2f})"
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), background_color, 2)
        cv2.putText(image, text_label, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, background_color, 2)
    return image


@click.group()
def cl1():
    pass

@cl1.command()
@click.option('--model-type', type=click.Choice(['n','s','m','l','x']), default='s')
@click.option('--confidence-threshold', type=click.FloatRange(0,.99), default=.5)
@click.option('--url', type=click.STRING, default='https://www.youtube.com/watch?v=sM-rZWOyJzc')
def youtube(model_type, confidence_threshold, url):
    video = pafy.new(url)
    play = video.getbest()
    cap = cv2.VideoCapture(play.url)
    # Check if the video is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open youtube video")
    model = torch.hub.load('ultralytics/yolov5', f"yolov5{model_type}", pretrained=True)
    print("Running object detection on webcam input, press any key to exit")
    input_key = -1
    fret = True
    while fret:
        fret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        annotated_frame = plot_boxes(frame, model, confidence_threshold)
        cv2.imshow('Input', annotated_frame)
        input_key = cv2.waitKey(1)
        if input_key != -1:
            break
    
    cap.release()
    cv2.destroyAllWindows()



@click.group()
def cl2():
    pass

@cl2.command()
@click.option('--model-type', type=click.Choice(['n','s','m','l','x']), default='s')
@click.option('--confidence-threshold', type=click.FloatRange(0,.99), default=.5)
def live(model_type, confidence_threshold):
    model = torch.hub.load('ultralytics/yolov5', f"yolov5{model_type}", pretrained=True)
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    print("Running object detection on webcam input, press any key to exit")
    input_key = -1
    while fret:
        fret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        annotated_frame = plot_boxes(frame, model, confidence_threshold)
        cv2.imshow('Input', annotated_frame)
        input_key = cv2.waitKey(1)
        if input_key != -1:
            break
    
    cap.release()
    cv2.destroyAllWindows()

main = click.CommandCollection(sources=[cl1, cl2])

if __name__ == "__main__":
    main()