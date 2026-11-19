# City Intelligence Tokyo · Current Workshop Workflow

> **Scope Note:** Legacy explorations (vvvv, TouchDesigner) are deprecated. The workshop uses the streamlined **Ableton Live + loopMIDI + Rhino/Grasshopper (Python) + GitHub Pages `<model-viewer>` + Notion** pipeline below.

---

## 1. Data Acquisition (Field Work)
- **Geospatial Base (`A1`):** Export target city district from OpenStreetMap as `.osm` (XML).
- **Field GPS & Metadata (`A2a` → `A2b`):** Pin field recording locations in Google Maps, organize and tag them in **Google My Maps** (`CH1`..`CHn`), and export as `.kml` / `.xml`.
- **Acoustic Capture (`A3`, `A4` → `A5`):**
  - Hardware field stems recorded on **Ableton Push**.
  - Mobile ambient recordings captured on **Cell Phone** and synthesized into companion tracks in **Suno AI**.

## 2. Audio-to-MIDI Bridge
- **Ableton Live (`B1`):** Multi-channel audio stems routed into MIDI channels using the open-source **`audioToMidi`** plugin.
- **loopMIDI (`B2`):** Zero-latency virtual loopback MIDI bus streaming real-time CC telemetry from Ableton Live into Grasshopper, while audio stems (`.mp3` / `.wav`) are exported for the 3D Web Viewer.

## 3. Rhino + Grasshopper Computational Engine
- **`C1` · Python XML/OSM Merger:** Parses Google My Maps `.kml`/`.xml` coordinates and injects custom `<node>` tags into the `.osm` file.
- **`C2` · Urban Area Map & Channel Anchors:** Maps multi-channel MIDI telemetry onto the geolocated `.osm` city blocks, generates vertical positioning stems topped with triangular anchor meshes named `CH1`, `CH2`, `CH3`, …, and exports the urban scene `.glb`.
- **`C3` · Python Real-Time loopMIDI Listener:** Polls `loopMIDI` at 60 FPS (`winmm.dll`) to output normalized channel values `[0.0–1.0]`.
- **`C4` · Generative Physical Artifact Script:** Drives polar loop closure and SubD MultiPipe morphogenesis to export both a web-ready `.glb` ring model and a watertight 2-manifold `.stl` / `.step` mesh for 3D printing.

## 4. Web Deployment, Notion & Digital Fabrication
- **[diagram.html](file:///c:/Users/tomas/Dropbox/00_TOMAS/00_PC/01_Work/03_Academic/Arizona/Smarts%20Cities_Tokyo/vsCode/City-Intelligence/diagram.html):** Interactive system architecture pipeline diagram (black, gray, and red theme).
- **[dual_viewport_viewer.html](file:///c:/Users/tomas/Dropbox/00_TOMAS/00_PC/01_Work/03_Academic/Arizona/Smarts%20Cities_Tokyo/vsCode/City-Intelligence/dual_viewport_viewer.html):** Asymmetric dual-window `<model-viewer>` web app:
  - **Left Window (01 · Area Map):** Dynamically detects and counts `CH#` triangular anchor meshes in the loaded `.glb`, animates vertical positioning lines from street level to each hotspot, and links them via toggleable SVG Bezier wires to the top-left **Audio Channels** rack (with per-channel and batch audio loading/playback).
  - **Right Window (02 · Ring Artifact):** Interactive 3D SubD MultiPipe ring viewer with auto-rotation and mobile AR preview.
- **Notion Team Pages (`D3`) & Digital Fabrication (`D4`):** Embeds the hosted GitHub Pages viewers via `/embed` alongside downloadable archives and 3D-printed artifacts.
