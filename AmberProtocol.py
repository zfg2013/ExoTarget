from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout
from mdtraj.reporters import HDF5Reporter


#Laod pDB
pdb = PDBFile('zuo_rfd.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
modeller = Modeller(pdb.topology, pdb.positions)
modeller.deleteWater()
residues=modeller.addHydrogens(forcefield)

print('Adding solvent...')
modeller.addSolvent(forcefield, padding=1.0*nanometer)
print('Minimizing...')

#
system = forcefield.createSystem(modeller.topology, nonbondedMethod=PME, nonbondedCutoff=1.0*nanometer, constraints=HBonds, rigidWater=True)
integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
integrator.setConstraintTolerance(0.00001)
simulation = Simulation(modeller.topology, system, integrator)
simulation.context.setPositions(modeller.positions)



# Perform local energy minimization
print("Minimizing energy...")
simulation.minimizeEnergy()

#minpositions = simulation.context.getState(getPositions=True).getPositions()
#app.PDBFile.writeFile(modeller.topology, minpositions, open('minimized_pdb.pdb', 'w'))


#Run the simulation for 10000 timsteps to equilibriate
print("Running NVT")
simulation.step(10000)



#Now run NPT for pressure
system.addForce(MonteCarloBarostat(1*bar, 300*kelvin))
simulation.context.reinitialize(preserveState=True)
simulation.reporters.append(HDF5Reporter('rfd_production.h5',10000))
simulation.reporters.append(StateDataReporter(stdout, 10000, step=True,
        potentialEnergy=True, kineticEnergy=True, totalEnergy=True))
simulation.reporters.append(StateDataReporter("rfd_md_log.txt", 10000, step=True,
         potentialEnergy=True, kineticEnergy=True, totalEnergy=True))
  
  
print("Running NPT (Production Mode - 1 ns)")
simulation.step(1000000)

#

#basic plotting
import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt("rfd_md_log.txt", delimiter=',')

step = data[:,0]
potential_energy = data[:,3]

plt.plot(step, potential_energy)
plt.xlabel("Step")
plt.ylabel("Total ENergy (kJ/mol)")
plt.savefig("rfd_zuo_pe.png")
plt.show()


# Reinitialize simulation reporters. We do this because we want different information printed from the production run than the equilibration run.
#simulations.reporters.clear()