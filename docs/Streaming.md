# Streaming
To stream a video, you can use the `stream.py` script from the VTS.

## Prerequisistes
The script requires that you have both FFmpeg and a version of Python
installed.

### Linux
If you're streaming video from a webcam, the script uses Video4Linux2.
As the name would suggest, this only works on a Linux system. You can
still test using video sources on Windows, but the documentation will
assume you're on a Linux system from this point.

### FFmpeg
FFmpeg is a ridiculously powerful program that can transcode, mux, and
work all sorts of magic with a wide variety of multimedia files. So,
naturally, it's going to be doing most of the heavy lifting.

If you're on Linux, you can usually install FFmpeg through
your package manager:

Ubuntu/Debian:
`sudo apt install ffmpeg`

Arch Linux:
`sudo pacman -Syu ffmpeg`

OpenSUSE:
`sudo zypper install ffmpeg`

(etc.)

### Python 3
You must have Python 3 installed. The script will not run on Python 2.
Install Python through your package manager if it isn't already there.

## Running the Streamer
To run the streamer, open a terminal window in the `vts` directory and
run `python3 stream.py` or `./stream.py`. You'll get a nice little help
message telling you that you need to add some arguments to your command
line.

Specifically, you need to specify a video source for both the left-eye
and right-eye videos, as well as a client address. For testing, you're
welcome to make these raw MJPEG files. To specify the videos, just add
the `-l` and `-r` flags:

`python stream.py -l left.mjpg -r right.mjpg -c x.x.x.x`

If you want to make a media file for testing, you can use FFmpeg to
convert an existing file:

`ffmpeg -i <original-video> -c:v mjpeg <output-file>.mp4`

When you want to stream live video, all you have to do is swap out the
video files for video device names. The script assumes that the device
you choose can output 30fps MJPEG video at 640x480 resolution.

The client parameter needs to specify the IP address to stream to.
This was added when UDP multicast caused issues with some devices.
Putting this all together, you get a command line like this:

`python stream.py -l /dev/video0 -r /dev/video2 -c 10.107.101.2`

The command-line help is always available by typing:

`python stream.py -h`

## Checking the Stream
The streaming script hosts an HTTP server on port 8080 that serves SDP
files your media player of choice should probably be able to handle.
These SDP files describe the streams for the left and right videos, and
you can access them at:

```
http://ip.of.streaming.device:8080/left.sdp
http://ip.of.streaming.device:8080/right.sdp
```

In the VTM, the IP address is 10.107.101.1, so it would look like this:

```
http://10.107.101.1:8080/left.sdp
http://10.107.101.1:8080/right.sdp
```

You can easily check the stream on your local machine with a video player
like VLC. Again, you can usually get this from your package manager's
default repositories on Linux, or you can download it from
[VideoLAN's website][videolan] for Windows, Linux, macOS, Android, and
various other systems.

Open VLC and browse to `Media` > `Open Network Stream...`:

![VLC menu][img-vlc-menu]

This should open a dialog box like the one below. Enter one of the stream
addresses, such as the one for the left stream:

`http://ip.of.streaming.device:8080/left.sdp`

Check `Show more options` at the bottom, then change the caching option to
something low, like 20ms, or eliminate it entirely (0ms).
Often, media is streamed over the Internet, and VLC buffers a full second
of video by default before starting playback. This is good for viewing
media online, where that latency isn't a big deal and it helps avoid the
video stream cutting out, but it's awful for real-time video because it
introduces a full second of latency!

![VLC network stream dialog][img-vlc-stream-dialog]

After clicking `Play`, you should see the video being streamed from FFmpeg
(assuming you have the streaming script running).

[winffmpeg]: https://ffmpeg.zeranoe.com/builds/ "Zeranoe FFmpeg Builds"
[python]: https://python.org "Python Official Website"
[videolan]: https://www.videolan.org "VideoLAN Website"

[img-vlc-menu]: img/vlc-open-network-stream.png
[img-vlc-stream-dialog]: img/vlc-network-stream-dialog.png
