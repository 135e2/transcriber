# transcriber

A simple tool that generates (and translates) transcripts.

## Highlights

- [WhisperX](https://github.com/m-bain/whisperX), with [faster-whisper](https://github.com/guillaumekln/faster-whisper) as the backend
- On-device, deep learning-based translation powered by [DL Translate](https://github.com/xhluca/dl-translate)
- Designate CPU/GPU through `-d` flag (`--device=cpu/cuda`)
- One-click run through [GitHub Actions](https://github.com/135e2/transcriber/actions) `workflow_dispatch`
- Prebuilt [docker image](https://github.com/135e2/transcriber/pkgs/container/transcriber)

---

![Python Version](https://img.shields.io/github/pipenv/locked/python-version/135e2/transcriber)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docker Image](https://ghcr-badge.egpl.dev/135e2/transcriber/latest_tag)](https://github.com/135e2/transcriber/pkgs/container/transcriber)
