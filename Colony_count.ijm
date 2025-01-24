// Automatically process and count algae colonies on agar plates

run("Open..."); // Opens a dialog to select the image file

run("8-bit");   // Convert image to 8-bit grayscale
run("Enhance Contrast", "saturated=0.35"); // Enhances the contrast for better visualization

// Specify the path to your summary file
summaryFile = "C:/path/to/your/summary.txt"; // Update this path as needed

// Wait for the user to define the initial area of measurement
waitForUser("Please select the initial area for measurement and then click OK.");

// Measure initial area and store it
run("Measure");

// Wait for the user to select the region of interest for cropping
waitForUser("Please zoom in to the agar plate as needed and select the region of interest, then click OK.");

// Crop the image to the selected area
run("Crop");

// Smoothing the image to reduce noise
run("Gaussian Blur...", "sigma=1"); // Adjust sigma value as necessary
run("Median...", "radius=1"); // Adjust the radius as needed

// Apply a binary threshold to isolate colonies
setAutoThreshold("Default"); // Automatically set the threshold
run("Convert to Mask"); // Convert the thresholded image to a binary mask

run("8-bit"); // Convert to 8-bit again
run("Make Binary"); // Ensure the image is binary (0s and 255s)

run("Erode"); // Erode to help pull apart merged colonies
run("Watershed"); // Apply Watershed to separate touching colonies

// Analyze particles with size, circularity, and area settings
run("Analyze Particles...", "size=10-500 circularity=0.7-1.0 show=Nothing display clear summarize");

// Measure the area of the analyzed particles
run("Measure");