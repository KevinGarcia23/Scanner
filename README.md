# Document Scanner using OpenCV

This is a simple **Python-based document scanner** built using OpenCV. The project captures an image of a document, detects its edges, applies a perspective transformation to simulate a top-down scanned view, and converts it into a clean, black-and-white image.

##  Demo

Original Photo → Edge Detection → Perspective Transform → Scanned Output  
*(Insert before/after images or a short gif here if available)*

---

##  Features

- Edge detection using Canny algorithm
- Automatic contour detection to locate the document
- Perspective transform for top-down "scanner-like" effect
- Adaptive thresholding for clean black-and-white output
- Modular code with separate transformation module

---

## What I Learned

- OpenCV image processing pipeline
- Contour approximation and geometric point ordering
- Perspective warping using transformation matrices
- Adaptive Gaussian thresholding
- Command-line interface design with `argparse`
- Code modularity with custom helper functions
