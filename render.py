"""Offers methods to render frames for a given time with a given device"""

import bpy

from glob import glob
from datetime import datetime
from natsort import natsorted
from os import makedirs, path, remove, rename
from subprocess import call
from time import time

import meta


SAMPLES_INITIAL = 8
SAMPLES_MULTIPLIER = 0.5
SAMPLES_CAP = 3200

QUALITY_PREVIEW = 32
QUALITY_PRODUCTION = 320

def render_frame(render_directory,
                 frame,
                 existing_samples,
                 additional_samples,
                 existing_frame=None):
    benchmark = time()

    bpy.context.scene.frame_current = frame
    bpy.context.scene.cycles.samples = additional_samples

    # Enable SVG export when using Freestyle
    if bpy.context.scene.render.use_freestyle:
        bpy.context.scene.svg_export.use_svg_export = True

    cache_filename = ".render-cache.png"
    cache_filepath = path.join(render_directory, cache_filename)

    bpy.context.scene.render.filepath = cache_filepath
    bpy.ops.render.render(write_still=True)

    if existing_frame:
        alpha = float(existing_samples) / float(existing_samples + additional_samples)

        result_samples = existing_samples + additional_samples
        result_filename = "{0:06}.{1}.png".format(frame, result_samples)
        result_filepath = path.join(render_directory, result_filename)

        ffmpeg_call = [
            "ffmpeg",
            "-y",
            "-i", existing_frame,
            "-i", cache_filepath,
            "-filter_complex",
            "[1:v][0:v]blend=all_expr='A*{0}+B*{1}'".format(alpha, 1 - alpha),
            result_filepath
        ]

        call(ffmpeg_call)

        remove(existing_frame)
        remove(cache_filepath)

    else:
        result_filename = "{0:06}.{1}.png".format(frame, additional_samples)
        result_filepath = path.join(render_directory, result_filename)

        rename(cache_filepath, result_filepath)

    if bpy.context.scene.render.use_freestyle:
        svg_old_filepath = path.join(render_directory,
                                     "{0}{1:04}.svg".format(cache_filename, frame))
        svg_new_filepath = path.join(render_directory,
                                     "{0:06}.svg".format(frame))

        if existing_frame:
            remove(svg_new_filepath)

        rename(svg_old_filepath, svg_new_filepath)

    # Thumbnail creation

    thumbnail_filepath = path.join(render_directory, "..", "thumbnail.png")
    call([
        "ffmpeg",
        "-y",
        "-f", "image2",
        "-i", result_filepath,
        "-vf", "scale=480:270:force_original_aspect_ratio=decrease",
        thumbnail_filepath
    ])

    meta.write({
        "renderDevice": bpy.context.scene.cycles.device,
        "lastRenderedFrame": frame,
        "lastRenderDuration": time() - benchmark,
        "lastRender": datetime.now().isoformat(),
        "lastRenderedSamples": additional_samples
    })


def render_frames(target_time, device):
    benchmark = time()

    bpy.context.scene.cycles.seed = int(benchmark) # Imagestacking random seed
    bpy.context.scene.cycles.device = device

    render_directory = path.join(bpy.path.abspath("//"), "rendered_frames")

    if not path.exists(render_directory):
        makedirs(render_directory)

    first = bpy.context.scene.frame_start
    last = bpy.context.scene.frame_end
    total_frames = last - first + 1

    rendered_frames = natsorted(glob(path.join(render_directory, "*.png")))
    requested_frames = []

    if len(rendered_frames) < total_frames:
        meta.write({"processing": "Rendering missing frames"})

        for number in range(first + len(rendered_frames), last + 1):
            requested_frames.append({
                "number": number,
                "available_samples": 0,
                "requested_samples": SAMPLES_INITIAL,
                "available_frame": None
            })
    else:
        samples = [int(path.basename(r).split(".")[1]) for r in rendered_frames]
        min_samples = min(samples)
        max_samples = max(samples)

        if min_samples < QUALITY_PREVIEW:
            render_quality = "draft"
        elif min_samples > QUALITY_PREVIEW:
            render_quality = "preview"
        elif min_samples > QUALITY_PRODUCTION:
            render_quality = "production"

        meta.write({
            "processing": "Rendering more samples",
            "minimumSamples": min_samples,
            "renderQuality": render_quality
        })

        if min_samples != max_samples:
            for frame in rendered_frames:
                frame_info = path.basename(frame).split(".")
                frame_number = int(frame_info[0])
                frame_samples = int(frame_info[1])

                if frame_samples < max_samples:
                    requested_frames.append({
                        "number": frame_number,
                        "available_samples": frame_samples,
                        "requested_samples": max_samples - frame_samples,
                        "available_frame": frame
                    })

        elif min_samples < SAMPLES_CAP:
            for frame in rendered_frames:
                frame_info = path.basename(frame).split(".")
                frame_number = int(frame_info[0])

                requested_frames.append({
                    "number": frame_number,
                    "available_samples": min_samples,
                    "requested_samples": int(min_samples * SAMPLES_MULTIPLIER),
                    "available_frame": frame
                })

    for frame in requested_frames:
        render_frame(render_directory,
                     frame["number"],
                     frame["available_samples"],
                     frame["requested_samples"],
                     frame["available_frame"])

        if time() - benchmark > target_time:
            break

    meta.write({"processing": False})


def render(target_time, device):

    if bpy.context.scene.render.engine == "BLEND4WEB":
        meta.write({
            "lastRender": datetime.now().isoformat()
        })
    else:
        render_frames(target_time, device)
