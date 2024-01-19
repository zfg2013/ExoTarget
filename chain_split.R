##THIS IS IN R

#load the libraries
library("bio3d")
library("XML")

#This is the current directory it will run in, change directory as needed
#getwd()


#This is the line that you need to split the chain.
pdbsplit('2j5y.pdb')

#, path="/blue/kgraim/zfg2013/ExoSearch/Amber/Input/AF_AMBER/"