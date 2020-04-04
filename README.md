# Vegetation Management

## Problem Statement

* Given a video showing the top view of wires and trees.
* Process the video to identify weather there are trees which might collide with live wires.

>>>> ![Image of Yaktocat](https://www.bpa.gov/PublicInvolvement/Vegetation-Management/Images%20Vegetation/Vegetation-diagram-460.jpg)

## Solution

* **Segmentation of Video :-** Created segments of video using OpenCV.
* **Depth Analysis :-** Finding depth depths of trees and wires by detecting these objects.
* **Drawing Inferences :-** Inferences were drawn based on the relative depths of wires and wires.
* **Results :-** Results were stored in the form of geographical points of those trees and a mail in sent to oncall team to acknowledge the issue.

## Testing

* The above solution was tested on a dummy scenario.
* Drawback of the solution is frames have been skipped in each fragment so that one tree should reside in more than one fragment. This needs to be improvised by making it continuous.
