FROM docker.io/archlinux:latest
# Add archlinux mirror
RUN sed -i '1iServer = https://mirrors.bfsu.edu.cn/archlinux/$repo/os/$arch' /etc/pacman.d/mirrorlist
RUN echo '[archlinuxcn]' >> /etc/pacman.conf \
 && echo 'SigLevel = Optional TrustedOnly' >> /etc/pacman.conf \
 && echo 'Server = https://mirrors.bfsu.edu.cn/archlinuxcn/$arch' >> /etc/pacman.conf \
 && pacman -Syyu --noconfirm 
RUN pacman-key --init \
 && pacman-key --populate archlinux \
 && pacman -S --noconfirm archlinuxcn-keyring 
# Deps 
RUN pacman -S base base-devel git asp python-pip paru --noconfirm --needed
# Build with makepkg's --nocheck flag in `paru.conf`
# https://aur.archlinux.org/packages/python-ffmpeg#comment-909364
COPY paru.conf /etc/paru.conf
# Hack from https://github.com/soloturn/build-aur-action/blob/b60db00581783113a7265a7858e2441c9e79df8b/Dockerfile#L2
RUN sed -i '/E_ROOT/d' /usr/bin/makepkg
RUN useradd -m -G wheel -s /bin/bash build
RUN perl -i -pe 's/# (%wheel ALL=\(ALL:ALL\) NOPASSWD: ALL)/$1/' /etc/sudoers
USER build
# python-tiktoken
# https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=whisper-git#n42
RUN paru -S python-tiktoken-git --noconfirm
# libnuma.so.1
RUN paru -S numactl --noconfirm
# build custom PKGBUILDs (python-llvmlite and python-numba)
RUN mkdir -p /tmp/{python-llvmlite,python-numba}
COPY trunk/PKGBUILD-python-llvmlite /tmp/python-llvmlite/PKGBUILD
COPY trunk/PKGBUILD-python-numba /tmp/python-numba/PKGBUILD
WORKDIR /tmp/python-llvmlite 
RUN paru -U --noconfirm
WORKDIR /tmp/python-numba 
RUN paru -U --noconfirm
RUN paru -S whisper-git --noconfirm
USER root
RUN mkdir ~/whisper
WORKDIR ~/whisper
