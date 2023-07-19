import argparse
import timeit
from .__version import __version__
from .utils import edit_file_extension, write_result
from .transcribe import WhisperxModel
from .translate import DltModel


def parse_args():
    parser = argparse.ArgumentParser(
        prog="transcriber",
        description=(
            "A simple tool that generates "
            "(and translates) transcripts. "
            "Checkout src/transcriber/constants.py for available languages."
        ),
    )
    parser.add_argument("FILE", help="The path of the source file")
    parser.add_argument(
        "-d",
        "--device",
        help="Device used by pytorch, default is cuda",
        default="cuda",
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Whisper model, default is large-v2",
        default="large-v2",
    )
    parser.add_argument(
        "-tl",
        "--target-language",
        help=(
            "The target language for translation, " "default is zh (Chinese)"
        ),
        default="zh",
    )
    parser.add_argument(
        "-t",
        "--translate",
        help="Whether to translate the transcript",
        action="store_true",
    )
    parser.add_argument(
        "-O",
        "--output",
        help=(
            "The output file path, " "default is FILE(_TARGET_LANGUAGE).srt"
        ),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="%(prog)s version code",
    )
    return parser.parse_args()


def cli():
    args = parse_args()

    fp, device, model_name, target_language, translate, output = (
        args.FILE,
        args.device,
        args.model,
        args.target_language,
        args.translate,
        args.output,
    )
    if device not in {"cuda", "cpu"}:
        device = "cuda"
    if output is None:
        output = edit_file_extension(fp, ".srt")

    # Import logger after argparse
    from .logger import logger

    time = timeit.default_timer()

    model = WhisperxModel(model_name, device)
    model.load_audio(fp)
    result = model.transcribe()

    write_result(result, output)
    logger.success(f"{fp} has been transcribed to {output}")

    if translate:
        dlt_model = DltModel(result["language"], target_language, device)
        for segment in result["segments"]:
            segment["text"] += f"\n{dlt_model.translate(segment['text'])}"

        output = edit_file_extension(output, f"_{target_language}.srt")
        write_result(result, output)
        logger.success(f"{fp} has been translated to {output}")

    logger.success("Time used: %.1fs" % (timeit.default_timer() - time))

    model.cleanup()


if __name__ == "__main__":
    cli()
