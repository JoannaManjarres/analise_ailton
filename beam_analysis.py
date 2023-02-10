#Script context use	: This script is for RAYMOBTIME purposes uses
#Author       		: Ailton Oliveira - Msc Degree (in progress) - PPGEE - UFPA
#Email          	: ailtonpoliveira01@gmail.com
################################################################################

import numpy as np
import matplotlib.pyplot as plt
from statistics import mode
from beam_tools import *

#Data                   
beam_file = './beam_output/beams_output_1x16.npz'
insiteCSVFile = './CoordVehiclesRxPerScene_s008.csv'
beams = np.load(beam_file)['output_classification']
tx_size = beams.shape[2]
print(beams.shape)

#Calculate the steered factor
theta = np.linspace(-np.pi,np.pi,1000) #Angular domain
theta = theta[:, np.newaxis]
arrayFactors = arrayFactorGivenAngleForULA(tx_size,theta)
normalized_dft = dft_codebook(tx_size)

#Reshape beam pair index
num_classes = beams.shape[1] * beams.shape[2]  
beams = beams.reshape(beams.shape[0],num_classes)
print(beams.shape)

#Fixed data (Rosslyn S008)
tx_coord = [746,560]
polygons = add_buildings()

#Beams distribution
best_beam_index = []
for sample in range(beams.shape[0]):
    best_beam_index.append(np.argmax(beams[sample,:]))
target = mode(best_beam_index)
print(target)

#Beams Histogram
labels, counts = np.unique(best_beam_index, return_counts=True)
plt.bar(labels, counts, align='center')
plt.title('Best beam pair index')
plt.ylabel('Probability')
plt.xlabel('Data')
#plt.savefig('./best_beams_8x1')
plt.show()

#Plot all positions per beam index
for desired_beam in range(tx_size):
    position_dist_per_beam(insiteCSVFile,theta,beams,desired_beam,arrayFactors,normalized_dft,tx_coord,polygons)
    
#Just active animation if you know how to force stop the script or if you have a much free time
plot_position_and_beam(insiteCSVFile,theta,beams,arrayFactors,normalized_dft,tx_coord,polygons,False)

