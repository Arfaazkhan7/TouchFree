🖐️ TouchFree — AI-Powered Touchless Cursor & Gesture Controller
Control your computer using hand gestures and a standard webcam.
TouchFree is a Python-based desktop application that uses computer vision and hand tracking to provide touchless mouse control. It allows users to move the cursor, perform mouse clicks, drag and drop items, scroll pages, zoom documents, and trigger selected Windows functions using hand gestures.
The system uses MediaPipe for hand landmark detection, OpenCV for real-time camera processing, and cursor-smoothing techniques to improve control and reduce unwanted movement.
✨ Features
•	Real-Time Hand Tracking: Detects hand landmarks through a webcam using MediaPipe.
•	Touchless Cursor Movement: Controls the mouse pointer using index and middle finger movements.
•	Cursor Smoothing: Uses 1-D Kalman filters to reduce cursor jitter.
•	Adaptive Cursor Speed: Adjusts cursor movement based on hand movement velocity.
•	Mouse Click Controls: Supports left-click, right-click, and double-click gestures.
•	Drag and Drop: Allows users to hold the mouse button and move items using gestures.
•	Scrolling and Zooming: Enables vertical scrolling and document or browser zoom operations.
•	Cursor Freeze: Temporarily locks cursor movement to prevent unwanted navigation.
•	Windows Task View: Provides a hand gesture to trigger Windows Task View.
•	Screenshot Capture: Captures screenshots and saves them as timestamped PNG files.
•	Live Tracking Overlay: Displays hand landmarks and tracking information.
•	Windows Executable: Supports packaging the application as a standalone executable using PyInstaller.
🛠️ Technologies Used
Technology	Purpose
Python	Core application development
OpenCV	Webcam access and real-time image processing
MediaPipe	Hand landmark detection
NumPy	Numerical calculations and array operations
PyAutoGUI	Mouse and keyboard automation
Kalman Filtering	Cursor smoothing and jitter reduction
PyInstaller	Packaging the application as a Windows executable
🎮 Gesture Controls
Gesture	Hand Position	Action
Move Cursor	Index and middle fingers extended; remaining fingers closed	Move the cursor
Freeze Cursor	Thumb, index, and middle fingers extended	Freeze cursor movement
Drag and Drop	Closed fist with thumb retracted	Hold the left mouse button while moving items
Scroll	Index finger extended; remaining fingers closed	Scroll up or down
Zoom In / Out	Index, middle, and ring fingers extended	Control zoom using Ctrl + Scroll
Windows Task View	Thumb and index finger extended in an L shape	Trigger Windows Task View
Left Click	Thumb and middle fingers open; snap and release the index finger	Perform a left click
Right Click	Thumb and index fingers open; snap and release the middle finger	Perform a right click
Double Click	Thumb open; snap and release the index and middle fingers	Perform a double click
Screenshot	Use the configured screenshot gesture	Save a timestamped screenshot
Exit Application	Press Esc while the camera window is focused	Close the application
Note: Gesture recognition depends on hand visibility, camera position, lighting conditions, and the implementation in cursor_control.py.
⚙️ How It Works
The application processes hand movements through the following stages:
1.	Video Capture: OpenCV captures live video from the webcam.
2.	Hand Detection: MediaPipe identifies hand landmarks in each frame.
3.	Gesture Recognition: Finger positions and joint angles are used to identify gestures.
4.	Movement Smoothing: Kalman filters help reduce unwanted cursor movement.
5.	Velocity Adaptation: Hand movement velocity is used to adjust cursor speed.
6.	Desktop Interaction: PyAutoGUI executes supported mouse and keyboard actions.
This process enables users to interact with supported desktop operations without continuously touching a physical mouse.
🔬 Technical Approach
1. Hand Landmark and Joint-Angle Detection
TouchFree uses hand landmarks to calculate finger joint angles and distinguish between bent and extended fingers.
The angle between three landmarks can be calculated using the dot product:
[
\cos(\theta)=\frac{\vec{ba}\cdot\vec{bc}}{|\vec{ba}||\vec{bc}|}
]
The documented thresholds are:
•	Extended finger: Joint angle greater than 162°
•	Bent finger: Joint angle less than 148°
These thresholds help classify finger positions for gesture recognition.
2. Kalman Filter-Based Cursor Smoothing
The application uses independent 1-D Kalman filters for the horizontal and vertical cursor coordinates.
Parameter	Value
Process Noise (Q)	1e-3
Measurement Noise (R)	5e-2
The filtering process helps reduce small fluctuations in detected hand positions while maintaining responsive cursor movement.
3. Adaptive Cursor Speed
Hand movement velocity is calculated from the displacement between consecutive frames:
[
v=\sqrt{\Delta x^2+\Delta y^2}
]
The documented velocity bounds are 0.002 and 0.04. Cursor speed is scaled between 0.7× for fine movements and 2.4× for faster navigation.
📁 Project Structure
Touchfree(FN)/
│
├── cursor_control.py    # Main application and gesture processing
├── rough.py             # Dependency verification and test script
├── touchfree.ico        # Application icon
├── Touch Free.spec      # PyInstaller build configuration
├── screenshots/         # Location for captured screenshots
├── requirements.txt     # Python dependencies, if included
├── LICENSE              # License terms, if included
└── README.md            # Project documentation
The dist/ directory may be generated when building the Windows executable. It can be excluded from GitHub if you prefer to keep the repository smaller.
🚀 Getting Started
Prerequisites
Before running the application, ensure that you have:
•	Windows 10 or Windows 11 (64-bit)
•	Python 3.10 or a compatible version supported by your dependencies
•	A built-in or external USB webcam
•	Git installed on your computer
•	Camera access enabled in Windows settings
Step 1: Clone the Repository
Replace YOUR_USERNAME with your GitHub username.
git clone https://github.com/YOUR_USERNAME/touchfree.git
Navigate to the project directory:
cd touchfree
Step 2: Create a Virtual Environment
python -m venv venv
Activate it using Windows Command Prompt:
venv\Scripts\activate.bat
Or activate it using PowerShell:
.\venv\Scripts\Activate.ps1
Step 3: Install Dependencies
If your repository includes a requirements.txt file, run:
python -m pip install -r requirements.txt
Make sure the file lists the actual packages and compatible versions used by your project.
Step 4: Verify the Installation
Run the dependency-checking script:
python rough.py
The expected success message documented for this project is:
Everything working 🔥
Step 5: Launch TouchFree
python cursor_control.py
Allow camera access if Windows requests permission.
Once the application starts, position your hand where the webcam can clearly detect it and try the supported gestures.
⚙️ Configuration
The following parameters are documented in cursor_control.py and can be adjusted to tune the application's behavior.
Parameter	Default Value	Purpose
EDGE_MARGIN	0.15	Defines the screen-edge mapping margin
DEAD_ZONE	0.004	Filters out very small movements
BASE_SPEED	1.6	Sets the base cursor speed
KALMAN_PROCESS_N	1e-3	Controls the Kalman filter process noise
KALMAN_MEASURE_N	5e-2	Controls the Kalman filter measurement noise
CLICK_DELAY	0.35	Sets the delay between consecutive clicks, in seconds
BEND_THRESHOLD	148	Threshold for classifying a finger as bent
OPEN_THRESHOLD	162	Threshold for classifying a finger as extended
SCROLL_SPEED	30	Controls vertical scrolling intensity
ZOOM_SENSITIVITY	0.004	Sets the minimum movement delta for zoom actions
Change these values gradually and test the cursor behavior after each modification.
📦 Build a Standalone Windows Executable
TouchFree includes a PyInstaller specification file for packaging the application as a Windows executable.
Run the following command from the project directory:
pyinstaller "Touch Free.spec"
After a successful build, the executable is expected to be available in the dist/ directory as Touch Free.exe.
The build result depends on the specification file, installed dependencies, and required application assets.
💡 Tips for Better Performance
•	Lighting: Use sufficient lighting so the camera can clearly detect your hand.
•	Camera Position: Place the webcam directly in front of you.
•	Hand Distance: Maintain a comfortable distance of approximately 1.5–3 feet from the camera.
•	Finger Position: Keep your fingers clearly visible when performing gestures.
•	Cursor Stability: Adjust the smoothing and dead-zone parameters if the cursor moves too much.
•	Background: Use a background that makes your hand easier to distinguish from surrounding objects.
🛠️ Troubleshooting
Cursor Is Not Moving
Check that the webcam is connected and the application detects your hand. For cursor movement, try extending the index and middle fingers while keeping the other fingers closed.
Cursor Movement Is Shaky
Try increasing KALMAN_MEASURE_N from 0.05 to 0.08 or slightly increasing DEAD_ZONE. Test the result to find a suitable balance between smoothness and responsiveness.
Cannot Reach the Screen Edges
Try increasing EDGE_MARGIN from 0.15 to 0.20. This changes the hand-to-screen coordinate mapping.
Camera Is Not Working
Check Windows camera permissions, close other applications that may be using the webcam, and restart TouchFree.
Multiple Monitor Issues
PyAutoGUI may map cursor coordinates to the primary display by default. Review the screen_w and screen_h configuration in cursor_control.py if you need to support multiple displays.
Executable Does Not Start
Verify that the PyInstaller build completed successfully and that the required assets are included in the specification file. If an error appears, run the Python application directly to help identify the problem.
🔮 Future Enhancements
Potential improvements for future versions include:
•	Customizable gesture assignments
•	User-adjustable cursor sensitivity through the interface
•	Support for additional gestures
•	Improved multi-monitor handling
•	A settings panel for configuring tracking behavior
•	More robust gesture recognition under different lighting conditions
📜 License
This project is intended to use the MIT License, as indicated in the project documentation.
Ensure that a valid LICENSE file containing the MIT License text is included in the repository before publishing or distributing the project under that license.
👨‍💻 Author
Your Name
GitHub: YOUR_USERNAME
________________________________________
TouchFree — A simple way to interact with your computer using hand gestures.

