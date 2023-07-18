import re
from whisperx.utils import format_timestamp


def edit_file_extension(filename, new_ext):
    # Use a regular expression to match the last occurrence of .*
    replaced_filename = re.sub(r"\.(.*)$", new_ext, filename)

    return replaced_filename


def write_result(result, o):
    foutput = open(o, "w", encoding="utf-8")
    ct = 0
    for i in result["segments"]:
        start = format_timestamp(i["start"], True)
        end = format_timestamp(i["end"], True)
        print(
            f"{(ct := ct + 1)}\n{start} --> {end}\n{i['text']}\n",
            file=foutput,
            flush=True,
        )
    foutput.close()
