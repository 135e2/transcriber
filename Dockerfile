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
# Hack from https://github.com/soloturn/build-aur-action/blob/b60db00581783113a7265a7858e2441c9e79df8b/Dockerfile#L2
RUN sed -i '/E_ROOT/d' /usr/bin/makepkg
RUN useradd -m -G wheel -s /bin/bash build
RUN perl -i -pe 's/# (%wheel ALL=\(ALL:ALL\) NOPASSWD: ALL)/$1/' /etc/sudoers
USER build
# python-tiktoken
# https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=whisper-git#n42
RUN paru -S python-tiktoken-git --noconfirm
RUN paru -S whisper-git --noconfirm
USER root
RUN mkdir ~/whisper
WORKDIR ~/whisper
