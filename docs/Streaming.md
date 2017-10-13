# Streaming
To stream a video, you can use the `stream.py` script from the VTS.

## Prerequisistes
The script requires that you have both FFmpeg and a version of Python
installed.

### FFmpeg
FFmpeg is a ridiculously powerful program that can transcode, mux, and
work all sorts of magic with a wide variety of multimedia files. So,
naturally, it's going to be doing most of the heavy lifting.

#### Linux
If you're on Linux, you can usually install FFmpeg through
your package manager:

Ubuntu/Debian:
`sudo apt install ffmpeg`

Arch Linux:
`sudo pacman -Syu ffmpeg`

OpenSUSE:
`sudo zypper install ffmpeg`

(etc.)

#### Windows
If you're on Windows, you can grab a [build from Zeranoe][winffmpeg].
I highly recommend downloading the static version, and if you're on
64-bit Windows, you should obviously choose the 64-bit build. The version
is mostly up to you - the one with the date code is built directly from
the latest Git sources, and the one with a version number is stable.
Copy the bin\ffmpeg.exe file to the same directory as the streamer script
so that Python can find it easily.

### Python
I recommend grabbing Python 3, but hey, if you're still feeling the love
for 2, I won't take that away from you... I'll let the Python Software
Foundation do that in [around three years][pep-373].

#### Linux
The `stream.py` script has been written to work properly with both Python
2 and Python 3, so you should be fine as long as you have at least one of
those installed (most Linux distributions have one installed by default).
Install Python through your package manager if it isn't already there.

#### Windows
If you're running Windows, you can grab a copy of Python from
[the official site][python] if you don't already have it.

## Running the Streamer
To run the streamer, open a terminal window or command prompt in the
`vts` directory and run `python stream.py` (Windows or Linux) or
`./stream.py` (Linux). You'll get a nice little help message telling
you that you need to add some arguments to your command-line.

Specifically, you need to specify a video source for both the left-eye
and right-eye videos. For testing, you're welcome to make these the exact
same video if you want to. To specify the videos, just add the `-l` and
`-r` flags:

`python stream.py -l left.mp4 -r right.mp4`

The software currently does not stream video from actual webcams, but that
should be a trivial change once we obtain hardware to test with.

By default, this will start streaming on the UDP multicast address
`239.0.0.1` on port `8100`. You can change these settings by adding the
`--host` and/or `--port` flags to the command-line.

The command-line help is always available by typing:

`python stream.py -h`

**IMPORTANT:** *At this time, the video must already be encoded with h.264
before being fed to the script.* You can easily convert an existing video
with the following command-line:

`ffmpeg -i <original-video> -c:v h264 <output-file>.mp4`

You can then use the re-encoded video file for `-l` and/or `-r`.

## Checking the Stream
You can easily check the stream on your local machine with a video player
like VLC. Again, you can usually get this from your package manager's
default repositories on Linux, or you can download it from
[VideoLAN's website][videolan] for Windows, Linux, macOS, Android, and
various other systems.

Open VLC and browse to `Media` > `Open Network Stream...`:

![VLC menu][img-vlc-menu]

This should open a dialog box like the one below. Enter the default
address of `rtp://239.0.0.1:8100`, or modify that based on the options you
passed to the script with `--host` and `--port`.

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
[pep-373]: https://www.python.org/dev/peps/pep-0373/ "Python PEP-373"
[videolan]: https://www.videolan.org "VideoLAN Website"

[img-vlc-menu]: img/vlc-open-network-stream.png
[img-vlc-stream-dialog]: img/vlc-network-stream-dialog.png
