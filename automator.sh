for angle_step in {1..10}
do
    #x = 'echo "0.0005*$angle_step" | bc'
    angle=`echo "0.0005*$angle_step" | bc`
    str="beam gaussian meanMomentum=100 sigmaP=20 nEvents=100000 particle=pi- sigmaX=5 sigmaY=5 meanXp=0 meanYp=0 sigmaXp=-$angle sigmaYp=-$angle beamZ=16"

    echo "Updating Pion_Line_BeamEllipse.g4bl with new angle = -$angle"
    sed -i "" s/"beam.*"/"$str"/ Pion_Line_BeamEllipse.g4bl

    detector_name="uniform_$angle\_rad_detector_8"
    sed -i "" s/"place Det rename=.*_detector_8 z=5921"/"place Det rename=$detector_name z=5921"/ Pion_Line_BeamEllipse.g4bl

    echo "Running G4beamline with modified g4bl file"
    /Applications/G4beamline-3.08.app/Contents/MacOS/g4bl Pion_Line_BeamEllipse.g4bl viewer=none >> Pion_Line_BeamEllipse.out
done