# Docker Selenium Automation

## Docker selenium containers

**Base on Github.** [SeleniumHQ docker-selenium](https://github.com/SeleniumHQ/docker-selenium)

---

### Available docker images

#### ![Firefox](https://raw.githubusercontent.com/alrra/browser-logos/main/src/firefox/firefox_24x24.png) Firefox
```sh
selenium/standalone-firefox
```

#### ![Chrome](https://raw.githubusercontent.com/alrra/browser-logos/main/src/chrome/chrome_24x24.png) Chrome 
```sh
selenium/standalone-chrome
```

#### ![Edge](https://raw.githubusercontent.com/alrra/browser-logos/main/src/edge/edge_24x24.png) Edge
```sh
selenium/standalone-edge
```

#### All browsers in single container
```bash
selenium/standalone-all-browsers
```

_Note:_ Only one Standalone container can run on port `4444` at the same time.

---

### Video recording

Tests execution can be recorded by using the `selenium/video`
Docker image. One container is needed per each container where a browser is running. This means if you are
running 5 Nodes/Standalone containers, you will need 5 video containers, the mapping is 1-1.

Currently, the only way to do this mapping is manually (either starting the containers manually or through `docker compose`).

**Notes**:
- Video recording for headless browsers is not supported. 
- Video recording tends to use considerable amounts of CPU. Normally you should estimate 1CPU per video container, 
and 1 CPU per browser container.
- Videos are stored in the `/videos` directory inside the video container. Map a local directory to get the videos.
- If you are running more than one video container, be sure to overwrite the video file name through the `FILE_NAME`
environment variable to avoid unexpected results.

---

## Environment setup

### Install virtualenv

Windows

```cmd
pip install virtualenv
```

Linux

```sh
sudo apt install python3-virtualenv -y
```

<br>

### Create virtualenv using python and set environment name `env`

Windows

```python
python -m virtualenv env
```

Linux

```python
python3 -m virtualenv env
```

<br>

### Activate to endearment execute this command in `CMD`

Windows

```cmd
env\Scripts\activate
```

Linux

```python
source env/bin/activate
```

<br>

### Deactivate to endearment execute this command in `CMD`

```cmd
deactivate
```

<br>

### Setup env with installing required libs that list with `requirements.txt`

Windows

```cmd
pip install -r requirements.txt
```

Linux

```python
pip3 install -r requirements.txt
```

<br>

### Verify Installation

```cmd
pip list
```
