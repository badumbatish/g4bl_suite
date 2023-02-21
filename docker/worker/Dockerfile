
FROM ubuntu:22.04

WORKDIR /root
RUN apt-get update \ 
    && apt -y  install --no-install-recommends wget axel build-essential openmpi-bin openmpi-doc libopenmpi-dev cmake qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools libgsl-dev fftw3-dev libxmu-dev \
    && rm -rf /var/lib/apt/lists/*
RUN axel --insecure -n $(nproc) https://root.cern/download/root_v6.26.06.Linux-ubuntu22-x86_64-gcc11.2.tar.gz
RUN axel --insecure -n $(nproc) https://gitlab.cern.ch/geant4/geant4/-/archive/v11.0.2/geant4-v11.0.2.tar.gz
RUN axel --insecure -n $(nproc) https://github.com/badumbatish/g4bl_source/raw/main/G4beamline-3.08-source.tar.xz

ENV GSL_DIR=/usr
ENV FFTW_DIR=/usr

# Install geant4 dependency for g4bl
WORKDIR /root
RUN tar -xf geant4-v11.0.2.tar.gz \ 
    && rm -rf geant4-v11.0.2.tar.gz
WORKDIR /root/geant4-v11.0.2 
RUN mkdir build
WORKDIR /root/geant4-v11.0.2/build
RUN cmake -DCMAKE_INSTALL_PREFIX=$HOME/geant4.v11.0.2 -DBUILD_SHARED_LIBS=OFF -DBUILD_STATIC_LIBS=ON -DGEANT4_USE_SYSTEM_EXPAT=OFF -DCMAKE_BUILD_TYPE=Release -DGEANT4_USE_RAYTRACER_X11=OFF -DGEANT4_USE_OPENGL_X11=OFF -DGEANT4_USE_QT=OFF .. \
    && cmake --build . --config Release --target install -- -j$(nproc)
ENV GEANT4_DIR=/root/geant4-v11.0.2


# Install root dependency for g4bl
WORKDIR /root
RUN tar -xf root_v6.26.06.Linux-ubuntu22-x86_64-gcc11.2.tar.gz \
    && rm -rf root_v6.26.06.Linux-ubuntu22-x86_64-gcc11.2.tar.gz \
    && mv root root_v6.26.06
ENV ROOTSYS=/root/root_v6.26.06


# g4bl installation
WORKDIR /root
RUN tar -xf G4beamline-3.08-source.tar.xz \
    && rm G4beamline-3.08-source.tar.xz \
    && mkdir G4beamline-3.08
WORKDIR /root/G4beamline-3.08
RUN cmake /root/G4beamline-3.08-source -DGeant4_DIR=/root/geant4.v11.0.2/lib/Geant4-11.0.2 \
    && cmake --build . --config Release --target install -- -j$(nproc) 
    
RUN rm CMakeCache.txt cmake_install.cmake install_manifest.txt  Makefile README.txt G4beamline-3.08-Ubuntu22.tgz \
    && rm -rf root/man root/cmake root/tutorials root/config \
    && rm -rf CMakeFiles finalize g4bl g4blmpi g4bltest doc validation examples 


# # Allow mpi to run as root, check https://www.open-mpi.org/doc/current/man1/mpirun.1.php#toc25 
FROM ubuntu:22.04

COPY --from=0 /root/G4beamline-3.08 /root/G4beamline-3.08

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1


RUN apt-get update \ 
    && apt -y  install --no-install-recommends build-essential libopenmpi-dev  \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir root/Geant4Data
WORKDIR /root/Geant4Data

ADD *.tar.gz .

WORKDIR /root
#WORKDIR /root/Geant4Data
#RUN bash script.sh 


