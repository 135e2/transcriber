#!/bin/env  python3

"""
Author: 135e2
License: WTFPLv2
Deps:
  - pysrt
  - translators
"""

import argparse


def translate_srt(
    filepath, output, replace=False, target_language="zh", translate_provider="bing"
):
    subtitles = pysrt.open(filepath, encoding="utf-8")

    # Translate
    def __translator():
        translator = getattr(tss, translate_provider)(
            text, to_language=target_language, update_session_after_seconds=15
        )
        return translator

    for subtitle in subtitles:
        text = subtitle.text
        try:
            srt_language = langdetect.detect(text)
        except langdetect.lang_detect_exception.LangDetectException as e:
            logger.warning(
                f"Got langdetect error: {e}, '{text}' might be a string `langdetect` cannot recognize."
            )
        if srt_language == target_language or (
            srt_language == "zh-cn" and target_language == "zh"
        ):  # Hack for ISO 639-1 zh-cn :(
            logger.info(
                f"The language of the srt file is already {target_language}, Skipping translation..."
            )
            break
        try:
            translation = __translator()
            if replace:
                subtitle.text = translation
            else:
                subtitle.text += "\n" + translation
            logger.info(
                f"[{subtitle.start.minutes}:{subtitle.start.seconds:02d}:{subtitle.start.milliseconds:03d} - "
                + f"{subtitle.end.minutes}:{subtitle.end.seconds:02d}:{subtitle.end.milliseconds:03d}] {subtitle.text}"
            )
        except AttributeError:
            logger.error("Got invalid translate_provider: " + translate_provider)
            logger.error(
                "Checkout https://github.com/UlionTse/translators#features for avaliable providers."
            )
            subtitles.save(output, encoding="utf-8")
            exit(1)
        except requests.exceptions.HTTPError as e:
            logger.error(f"Got a HTTP error, please check your session: \n{e}")
            subtitles.save(output, encoding="utf-8")
            exit(1)
    subtitles.save(output, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="translate.py", description="Yet another simple subtitle translator."
    )
    parser.add_argument("FILE", help="The path of the srt file")
    parser.add_argument(
        "-tl",
        "--target-language",
        help="The target language for translation, default is zh (Chinese)",
        default="zh",
    )
    parser.add_argument(
        "-tp",
        "--translate-provider",
        help="The translate provider for translation, default is bing\n\nCheckout https://github.com/UlionTse/translators#features for more details.",
        default="bing",
    )
    parser.add_argument(
        "-O",
        "--output",
        help="The output file path, default it FILE_{TARGET_LANGUAGE}-{TRASLATE_PROVIDER}.srt",
    )
    parser.add_argument(
        "-R", "--replace", help="Replace the origin subtitle", action="store_true"
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s v1.5-20230113",
        help="%(prog)s version code",
    )
    args = parser.parse_args()

    filepath, target_language, translate_provider, output, replace = (
        args.FILE,
        args.target_language,
        args.translate_provider,
        args.output,
        args.replace,
    )
    if output == None:
        output = args.FILE.replace(
            ".srt", f"_{target_language}-{translate_provider}.srt"
        )

    # Dynamic Import
    import pysrt
    from translators import server as tss
    import timeit
    import requests
    import langdetect
    from logger import logger

    time = timeit.default_timer()
    translate_srt(filepath, output, replace, target_language, translate_provider)
    logger.success(f"{filepath} has been translated to {output}")
    logger.success("Time used: %.1fs" % (timeit.default_timer() - time))
