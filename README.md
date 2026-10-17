###### **TouchFree**



Control your computer using hand gestures and a standard webcam.

TouchFree is a Python-based desktop application that uses computer vision and hand tracking to provide touchless mouse control. It allows users to move the cursor, perform mouse clicks, drag and drop items, scroll pages, zoom documents, and trigger selected Windows functions using hand gestures.

The system uses MediaPipe for hand landmark detection, OpenCV for real-time camera processing, and cursor-smoothing techniques to improve control and reduce unwanted movement.



###### **Features**

•Real-Time Hand Tracking: Detects hand landmarks through a webcam using MediaPipe.

•Touchless Cursor Movement: Controls the mouse pointer using index and middle finger movements.

•Cursor Smoothing: Uses 1-D Kalman filters to reduce cursor jitter.

•Adaptive Cursor Speed: Adjusts cursor movement based on hand movement velocity.

•Mouse Click Controls: Supports left-click, right-click, and double-click gestures.

•Drag and Drop: Allows users to hold the mouse button and move items using gestures.

•Scrolling and Zooming: Enables vertical scrolling and document or browser zoom operations.

•Cursor Freeze: Temporarily locks cursor movement to prevent unwanted navigation.

•Windows Task View: Provides a hand gesture to trigger Windows Task View.

•Screenshot Capture: Captures screenshots and saves them as timestamped PNG files.

•Live Tracking Overlay: Displays hand landmarks and tracking information.

•Windows Executable: Supports packaging the application as a standalone executable using PyInstaller.



###### **Technologies Used**

+------------------+------------------------------------------+

| Technology       | Purpose                                  |

+------------------+------------------------------------------+

| Python           | Core application development             |

| OpenCV           | Webcam access and image processing       |

| MediaPipe        | Hand landmark detection                  |

| NumPy            | Numerical and array operations           |

| PyAutoGUI        | Mouse and keyboard automation            |

| Kalman Filtering | Cursor smoothing and jitter reduction    |

| PyInstaller      | Building standalone Windows executable   |

###### 

###### **Gesture Controls**



+------------------+----------------------------------------------+----------------------+

| Gesture          | Hand Pose                                    | Action               |

+------------------+----------------------------------------------+----------------------+

| Move Cursor      | Index + Middle fingers extended             | Move cursor          |

| Freeze Cursor    | Thumb + Index + Middle extended             | Freeze cursor        |

| Drag and Drop    | Closed fist                                  | Hold and drag items  |

| Scroll           | Index finger only extended                   | Scroll up/down       |

| Zoom In/Out      | Index + Middle + Ring extended              | Zoom in/out          |

| Task View        | Thumb + Index in an "L" shape               | Open Windows Task View|

| Left Click       | Thumb + Middle open; snap/release Index     | Left click           |

| Right Click      | Thumb + Index open; snap/release Middle     | Right click          |

| Double Click     | Thumb open; snap/release Index + Middle     | Double click         |

| Screenshot       | Thumb + Index + Middle + Ring open;         | Capture screenshot   |

|                  | bend and release Index, Middle, Ring        |                      |

| Quit Application | Press Esc while camera window is focused    | Exit application     |

+------------------+----------------------------------------------+----------------------+
Note: Gesture recognition depends on hand visibility, camera position, lighting conditions, and the implementation in cursor\_control.py.



###### **How It Works**

The application processes hand movements through the following stages:

1.Video Capture: OpenCV captures live video from the webcam.

2.Hand Detection: MediaPipe identifies hand landmarks in each frame.

3.Gesture Recognition: Finger positions and joint angles are used to identify gestures.

4.Movement Smoothing: Kalman filters help reduce unwanted cursor movement.

5.Velocity Adaptation: Hand movement velocity is used to adjust cursor speed.

6.Desktop Interaction: PyAutoGUI executes supported mouse and keyboard actions.

This process enables users to interact with supported desktop operations without continuously touching a physical mouse.



###### **Technical Approach**



**1. Hand Landmark Detection**

TouchFree uses MediaPipe to detect hand landmarks through a webcam. It calculates finger angles to identify whether fingers are open or bent.



\-->Open Finger: Angle greater than 162°.

\-->Bent Finger: Angle less than 148°.



This helps the system recognize different hand gestures.



**2. Kalman Filter-Based Cursor Smoothing**

TouchFree uses Kalman filters to reduce unwanted cursor shaking and make cursor movement smoother.



| Parameter             | Value |

| Process Noise (Q)     | 1e-3 |

| Measurement Noise (R) | 5e-2 |



These filters help maintain smooth and responsive cursor movement.



**3. Adaptive Cursor Speed**

TouchFree adjusts cursor speed based on how fast the hand moves.



\-->Slow Hand Movement: Provides better accuracy for precise cursor control.

\-->Fast Hand Movement: Increases cursor speed for quick navigation.



The cursor speed ranges from 0.7× to 2.4×, depending on hand movement velocity..



###### **Project Structure**

Touchfree(/

│

├── cursor\_control.py    # Main application and gesture processing

├── rough.py             # Dependency verification and test script

├── touchfree.ico        # Application icon

├── Touch Free.spec      # PyInstaller build configuration

├── screenshots/         # Location for captured screenshots

├── requirements.txt     # Python dependencies, if included

├── LICENSE              # License terms, if included

└── README.md            # Project documentation

The dist/ directory may be generated when building the Windows executable. It can be excluded from GitHub if you prefer to keep the repository smaller.



###### **Getting Started**

Prerequisites

Before running the application, ensure that you have:

•	Windows 10 or Windows 11 (64-bit)

•	Python 3.10 or a compatible version supported by your dependencies

•	A built-in or external USB webcam

•	Git installed on your computer

•	Camera access enabled in Windows settings

**Step 1: Clone the Repository**

Replace YOUR\_USERNAME with your GitHub username.

git clone https://github.com/YOUR\_USERNAME/touchfree.git

Navigate to the project directory:

cd touchfree

**Step 2: Create a Virtual Environment**

python -m venv venv

Activate it using Windows Command Prompt:

venv\\Scripts\\activate.bat

Or activate it using PowerShell:

.\\venv\\Scripts\\Activate.ps1

**Step 3: Install Dependencies**

If your repository includes a requirements.txt file, run:

python -m pip install -r requirements.txt

Make sure the file lists the actual packages and compatible versions used by your project.

**Step 4: Verify the Installation**

Run the dependency-checking script:

python rough.py

The expected success message documented for this project is:

Everything working 

**Step 5: Launch TouchFree**

python cursor\_control.py

Allow camera access if Windows requests permission.

Once the application starts, position your hand where the webcam can clearly detect it and try the supported gestures.



###### **Configuration**

The following parameters are documented in cursor\_control.py and can be adjusted to tune the application's behavior.

+----------------------+---------------+--------------------------------------------------+

| Parameter            | Default Value | Purpose                                          |

+----------------------+---------------+--------------------------------------------------+

| EDGE\_MARGIN          | 0.15          | Defines the screen-edge mapping margin           |

| DEAD\_ZONE            | 0.004         | Filters out very small movements                 |

| BASE\_SPEED           | 1.6           | Sets the base cursor speed                       |

| KALMAN\_PROCESS\_N     | 1e-3          | Controls Kalman filter process noise             |

| KALMAN\_MEASURE\_N     | 5e-2          | Controls Kalman filter measurement noise         |

| CLICK\_DELAY          | 0.35          | Sets the delay between consecutive clicks        |

| BEND\_THRESHOLD       | 148           | Identifies a finger as bent                      |

| OPEN\_THRESHOLD       | 162           | Identifies a finger as extended                  |

| SCROLL\_SPEED         | 30            | Controls vertical scrolling intensity            |

| ZOOM\_SENSITIVITY     | 0.004         | Sets the minimum movement for zoom actions       |

+----------------------+---------------+--------------------------------------------------+



Note: Change these values gradually and test the cursor

behavior after each modification.



**Build a Standalone Windows Executable**

TouchFree includes a PyInstaller specification file for packaging the application as a Windows executable.

Run the following command from the project directory:

pyinstaller "Touch Free.spec"

After a successful build, the executable is expected to be available in the dist/ directory as Touch Free.exe.

The build result depends on the specification file, installed dependencies, and required application assets.



**Tips for Better Performance**

•Lighting: Use sufficient lighting so the camera can clearly detect your hand.

•Camera Position: Place the webcam directly in front of you.

•Hand Distance: Maintain a comfortable distance of approximately 1.5–3 feet from the camera.

•Finger Position: Keep your fingers clearly visible when performing gestures.

•Cursor Stability: Adjust the smoothing and dead-zone parameters if the cursor moves too much.

•Background: Use a background that makes your hand easier to distinguish from surrounding objects.



**Troubleshooting**

Cursor Is Not Moving

Check that the webcam is connected and the application detects your hand. For cursor movement, try extending the index and middle fingers while keeping the other fingers closed.

Cursor Movement Is Shaky

Try increasing KALMAN\_MEASURE\_N from 0.05 to 0.08 or slightly increasing DEAD\_ZONE. Test the result to find a suitable balance between smoothness and responsiveness.

Cannot Reach the Screen Edges

Try increasing EDGE\_MARGIN from 0.15 to 0.20. This changes the hand-to-screen coordinate mapping.

Camera Is Not Working

Check Windows camera permissions, close other applications that may be using the webcam, and restart TouchFree.

Multiple Monitor Issues

PyAutoGUI may map cursor coordinates to the primary display by default. Review the screen\_w and screen\_h configuration in cursor\_control.py if you need to support multiple displays.

Executable Does Not Start

Verify that the PyInstaller build completed successfully and that the required assets are included in the specification file. If an error appears, run the Python application directly to help identify the problem.



###### **Future Enhancements**

Potential improvements for future versions include:

•Customizable gesture assignments

•User-adjustable cursor sensitivity through the interface

•Support for additional gestures

•Improved multi-monitor handling

•A settings panel for configuring tracking behavior

•More robust gesture recognition under different lighting conditions



###### **License**

This project is intended to use the MIT License, as indicated in the project documentation.

Ensure that a valid LICENSE file containing the MIT License text is included in the repository before publishing or distributing the project under that license.



###### **Author**

Mohamed Arfaaz Khan f

GitHub: https://github.com/Arfaazkhan7



\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

TouchFree — A simple way to interact with your computer using hand gestures.





