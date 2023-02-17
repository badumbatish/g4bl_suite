# FROM golang:1.19.4

# RUN apt-get update

FROM ubuntu:22.04

WORKDIR /root

RUN apt-get update

RUN apt -y install wget axel

RUN apt -y install build-essential openmpi-bin openmpi-doc libopenmpi-dev cmake
RUN apt -y install qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools

RUN apt -y install libgsl-dev fftw3-dev

ENV GSL_DIR=/usr
ENV FFTW_DIR=/usr


RUN axel -n $(nproc) https://root.cern/download/root_v6.26.06.Linux-ubuntu22-x86_64-gcc11.2.tar.gz
RUN tar -xf root_v6.26.06.Linux-ubuntu22-x86_64-gcc11.2.tar.gz
RUN rm -rf root_v6.26.06.Linux-ubuntu22-x86_64-gcc11.2.tar.gz
RUN mv root root_v6.26.06
ENV ROOTSYS=/root/root_v6.26.06

# Install dependency for geant4
RUN apt -y install libxmu-dev
RUN axel -n $(nproc) https://gitlab.cern.ch/geant4/geant4/-/archive/v11.0.2/geant4-v11.0.2.tar.gz
RUN tar -xf geant4-v11.0.2.tar.gz
RUN rm -rf geant4-v11.0.2.tar.gz
WORKDIR /root/geant4-v11.0.2 
RUN mkdir build
WORKDIR /root/geant4-v11.0.2/build

RUN cmake -DCMAKE_INSTALL_PREFIX=$HOME/geant4.v11.0.2 -DBUILD_SHARED_LIBS=OFF -DBUILD_STATIC_LIBS=ON -DGEANT4_USE_SYSTEM_EXPAT=OFF -DCMAKE_BUILD_TYPE=Release -DGEANT4_USE_RAYTRACER_X11=ON -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_USE_QT=ON ..
RUN cmake --build . --config Release --target install -- -j$(nproc)
ENV GEANT4_DIR=/root/geant4.v11.0.2

WORKDIR /root
RUN axel -n $(nproc) https://github.com/badumbatish/g4bl_source/raw/main/G4beamline-3.08-source.tar.xz

RUN tar -xf G4beamline-3.08-source.tar.xz
RUN rm G4beamline-3.08-source.tar.xz
RUN mkdir G4beamline-3.08
WORKDIR /root/G4beamline-3.08

RUN cmake /root/G4beamline-3.08-source -DGeant4_DIR=/root/geant4.v11.0.2/lib/Geant4-11.0.2
RUN cmake --build . --config Release --target install -- -j$(nproc)

# RUN mkdir -p /app/etc
# RUN mkdir -p /app/lib
# RUN mkdir -p /app/golang

# COPY ./local-worker.yaml /app/etc/worker.yaml
# COPY ./golang /app/lib/golang

# WORKDIR /app/golang

# ENTRYPOINT [ "/app/lib/golang" ]