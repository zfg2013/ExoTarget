import mdtraj as md
t = md.load('rfd_production.h5')
t.image_molecules()
t.save_pdb('rfd_zuo.pdb')