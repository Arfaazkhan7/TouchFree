# TouchFree

## About the Project

TouchFree is a Python desktop application that allows users to control their computer using hand gestures and a webcam. It helps users move the mouse cursor, click, drag and drop items, scroll pages, zoom documents, and take screenshots without using a physical mouse.

The project uses MediaPipe to detect hand movements, OpenCV to process camera images, and PyAutoGUI to control mouse and keyboard actions. Kalman filtering is used to reduce unwanted cursor movement and make control smoother.

## Features

- **Hand Tracking:** Detects hand landmarks using a webcam.
- **Cursor Movement:** Moves the mouse pointer using hand gestures.
- **Cursor Smoothing:** Uses Kalman filters to reduce cursor shaking.
- **Adaptive Cursor Speed:** Changes cursor speed based on hand movement.
- **Mouse Clicks:** Supports left-click, right-click, and double-click gestures.
- **Drag and Drop:** Allows users to hold and move items using gestures.
- **Scrolling:** Scrolls pages using hand movements.
- **Zoom Control:** Zooms in and out using gestures.
- **Cursor Freeze:** Temporarily stops cursor movement.
- **Windows Task View:** Opens Windows Task View using a gesture.
- **Screenshot:** Captures screenshots and saves them as PNG files.
- **Tracking Overlay:** Displays hand landmarks and tracking information.
- **Windows Executable:** Supports creating a standalone executable using PyInstaller.

## Technologies Used

- **Python:** Used to develop the application.
- **OpenCV:** Captures webcam video and processes images.
- **MediaPipe:** Detects hand landmarks.
- **NumPy:** Performs numerical and array operations.
- **PyAutoGUI:** Controls mouse and keyboard actions.
- **Kalman Filtering:** Reduces cursor shaking.
- **PyInstaller:** Packages the application as a Windows executable.

## Gesture Controls

| Gesture | Hand Pose | Action |
|---|---|---|
| Move Cursor | Index and middle fingers extended | Move the cursor |
| Freeze Cursor | Thumb, index, and middle fingers extended | Freeze cursor movement |
| Drag and Drop | Closed fist | Hold and drag items |
| Scroll | Index finger extended | Scroll up or down |
| Zoom In/Out | Index, middle, and ring fingers extended | Zoom in or out |
| Task View | Thumb and index finger in an L shape | Open Windows Task View |
| Left Click | Thumb and middle finger open; snap and release index finger | Perform a left-click |
| Right Click | Thumb and index finger open; snap and release middle finger | Perform a right-click |
| Double Click | Thumb open; snap and release index and middle fingers | Perform a double-click |
| Screenshot | Thumb, index, middle, and ring fingers open; bend and release the three fingers | Capture a screenshot |
| Quit Application | Press `Esc` while the camera window is focused | Exit the application |

**Note:** Gesture recognition depends on lighting, hand visibility, camera position, and the implementation in `cursor_control.py`.

## How It Works

The application works through the following steps:

1. **Video Capture:** OpenCV captures live video from the webcam.
2. **Hand Detection:** MediaPipe detects hand landmarks.
3. **Gesture Recognition:** Finger positions and joint angles are used to identify gestures.
4. **Cursor Smoothing:** Kalman filters help reduce unwanted cursor movement.
5. **Speed Adjustment:** Cursor speed changes according to hand movement.
6. **Computer Control:** PyAutoGUI performs the required mouse and keyboard actions.

## Technical Approach

### 1. Hand Landmark Detection

MediaPipe detects hand landmarks from the webcam video. Finger angles help identify whether a finger is open or bent.

- **Open Finger:** Angle greater than 162°.
- **Bent Finger:** Angle less than 148°.

These values help identify different hand gestures.

### 2. Kalman Filter-Based Cursor Smoothing

Kalman filters help reduce cursor shaking and improve cursor control.

| Parameter | Value |
|---|---|
| Process Noise (Q) | `1e-3` |
| Measurement Noise (R) | `5e-2` |

### 3. Adaptive Cursor Speed

The application changes cursor speed according to hand movement.

- **Slow Movement:** Helps with accurate cursor control.
- **Fast Movement:** Helps move the cursor quickly across the screen.

The documented cursor speed ranges from `0.7×` to `2.4×`.

## Project Structure

```text
TouchFree/
├── cursor_control.py    # Main application and gesture processing
├── rough.py             # Dependency verification and test script
├── touchfree.ico        # Application icon
├── Touch Free.spec      # PyInstaller build configuration
├── screenshots/         # Saved screenshots
├── requirements.txt     # Python dependencies, if included
├── LICENSE              # License file, if included
└── README.md            # Project documentation
```

The `dist/` directory may be created when building the Windows executable.

## Getting Started

### Prerequisites

Before running the application, make sure you have:

- Windows 10 or Windows 11 (64-bit).
- Python 3.10 or a compatible version.
- A built-in or external USB webcam.
- Git installed on your computer.
- Camera access enabled in Windows settings.

### Step 1: Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/touchfree.git
```

Open the project directory:

```bash
cd touchfree
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it using Command Prompt:

```bash
venv\Scripts\activate.bat
```

Or activate it using PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

If the project contains a `requirements.txt` file, run:

```bash
python -m pip install -r requirements.txt
```

Make sure the file contains the packages required by the project.

### Step 4: Check the Installation

Run the dependency-checking script:

```bash
python rough.py
```

The expected success message is:

```text
Everything working
```

### Step 5: Run TouchFree

```bash
python cursor_control.py
```

Allow camera access if Windows asks for permission. Keep your hand visible to the webcam and try the supported gestures.

## Configuration

The following parameters are documented in `cursor_control.py`.

| Parameter | Default Value | Purpose |
|---|---:|---|
| `EDGE_MARGIN` | `0.15` | Sets the screen-edge mapping margin |
| `DEAD_ZONE` | `0.004` | Filters very small movements |
| `BASE_SPEED` | `1.6` | Sets the base cursor speed |
| `KALMAN_PROCESS_N` | `1e-3` | Controls Kalman filter process noise |
| `KALMAN_MEASURE_N` | `5e-2` | Controls Kalman filter measurement noise |
| `CLICK_DELAY` | `0.35` | Sets the delay between clicks |
| `BEND_THRESHOLD` | `148` | Identifies a bent finger |
| `OPEN_THRESHOLD` | `162` | Identifies an extended finger |
| `SCROLL_SPEED` | `30` | Controls scrolling speed |
| `ZOOM_SENSITIVITY` | `0.004` | Sets the minimum movement for zooming |

Change these values gradually and test the cursor after each change.

## Build a Windows Executable

TouchFree includes a PyInstaller specification file.

Run the following command from the project directory:

```bash
pyinstaller "Touch Free.spec"
```

After a successful build, the executable is expected to be available in the `dist/` directory as `Touch Free.exe`. The result depends on the build configuration, installed dependencies, and required files.

## Tips for Better Performance

- **Lighting:** Use enough light for the camera to detect your hand clearly.
- **Camera Position:** Place the webcam in front of you.
- **Hand Distance:** Stay approximately 1.5–3 feet away from the camera.
- **Finger Position:** Keep your fingers clearly visible while performing gestures.
- **Cursor Stability:** Adjust the smoothing and dead-zone values if the cursor shakes.
- **Background:** Use a background that makes your hand easy to see.

## Troubleshooting

### Cursor Is Not Moving

Check whether the webcam is connected and the application can detect your hand. Try extending your index and middle fingers.

### Cursor Movement Is Shaky

Try increasing `KALMAN_MEASURE_N` from `0.05` to `0.08` or slightly increasing `DEAD_ZONE`. Test the result to find a suitable balance.

### Cannot Reach the Screen Edges

Try increasing `EDGE_MARGIN` from `0.15` to `0.20` and test the cursor movement.

### Camera Is Not Working

Check Windows camera permissions, close other applications using the webcam, and restart TouchFree.

### Multiple Monitor Issues

PyAutoGUI may use the primary display by default. Check the `screen_w` and `screen_h` settings in `cursor_control.py` if you need multiple-monitor support.

### Executable Does Not Start

Check whether the PyInstaller build completed successfully and whether the required files are included. You can also run the Python application directly to identify errors.

## Future Improvements

Some possible improvements for future versions are:

- Customizable gesture assignments.
- Cursor sensitivity settings through the interface.
- Support for more gestures.
- Better multi-monitor support.
- A settings panel for tracking options.
- Improved gesture recognition in different lighting conditions.

## License

This project is intended to use the MIT License, as indicated in the project documentation.

Make sure a valid `LICENSE` file containing the MIT License text is included before publishing or distributing the project under that license.

## Author

**Mohamed Arfaaz Khan F**

GitHub: [Arfaazkhan7](https://github.com/Arfaazkhan7)

---

*TouchFree — A simple way to control your computer using hand gestures.*
