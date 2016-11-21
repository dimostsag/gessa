#!bin/bash

NJOBS=2 # Number of CPU cores to use.
POINTS=1024 # Number of landmarks
ITERATIONS=500 # Number of iteration steps per optimization cycle

# Preliminary
# Surfaces are translated to (0,0,0) and scaled to have a fixed std. This has shown improved performance during landmarking. The results can be subsequently unscaled (see below).

cd ../supporting_code/

/usr/bin/python scale_surfaces.py $NJOBS '../example/data/faces/' '../example/data/scaled_faces/' # positional parameters: 1: No of cores, 2: Input surfaces' folder, 3: Output folder

cd ../example/

mkdir -p ./results/ # create a results directory

# Run GESSA software

cd ../gessa/

/usr/bin/python ./ensemble_sampling.py $NJOBS $POINTS $ITERATIONS '../example/data/scaled_faces/' '../example/results/points_example.pkl' # positional parameters: 1: No of cores, 2: No of landmarks, 3: Iteration steps, 4: Surface Input Folder, 5: Landmark Output file

# Plot resulting landmark sets on the surfaces

cd ../supporting_code/

/usr/bin/python plot_points.py '../example/results/points_example.pkl' '../example/data/scaled_faces/' # positional parameters: 1: Landmark File, 2: Surfaces' folder

# Post processing
# Unscale surfaces and landmarks to the original dimensions, if needed

#/usr/bin/python unscale_surfaces.py $NJOBS '../example/data/scaled_faces/' '../example/data/unscaled_faces/' '../example/results/points_example.pkl' '../example/results/points_unscaled.pkl'
