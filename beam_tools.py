#Script context use	: This script is for RAYMOBTIME purposes uses
#Author       		: Ailton Oliveira - Msc Degree (in progress) - PPGEE - UFPA
#Email          	: ailtonpoliveira01@gmail.com
################################################################################
import numpy as np
import matplotlib.pyplot as plt
from shapely import geometry
import csv

def add_buildings():
    polygons = []
    #Rosslyn
    build_vertice =((855,402), (808,403), (808,445), (791,443), (777,448), (768,644), (780,657), (831,657))
    build_polygon = geometry.Polygon(build_vertice)
    polygons.append(build_polygon)
    build_vertice = ((816, 687),(710, 692),(708, 733),(693, 735),(691, 710),(660, 712),(660, 755),(764, 746))
    build_polygon = geometry.Polygon(build_vertice)
    polygons.append(build_polygon)
    build_vertice = ((841, 295),(842, 317),(830, 340),(806, 354),(802, 371),(706, 433),(684, 435),(664, 424))
    build_polygon = geometry.Polygon(build_vertice)
    polygons.append(build_polygon)
    build_vertice = ((658, 660),(685,661),(685,657),(720,658),(722,635),(735,635),(751,458),(740,467),(700,471),(700,484),(660,483))
    build_polygon = geometry.Polygon(build_vertice)
    polygons.append(build_polygon)
    return polygons

# Codebook based in DFT 
def dft_codebook(dim):
    seq = np.matrix(np.arange(dim))
    mat = seq.conj().T * seq
    w = np.exp(-1j * 2 * np.pi * mat / dim)
    return w/np.sqrt(dim)

def arrayFactorGivenAngleForULA(numAntennaElements, theta, normalizedAntDistance=0.5, angleWithArrayNormal=0):
    if (angleWithArrayNormal == 1):
        temp = -1j*2*np.pi*normalizedAntDistance*np.sin(theta)
        arrayFactor = np.exp(np.kron(np.arange(0, numAntennaElements), temp))
    else:  # default
        temp = -1j*2*np.pi*normalizedAntDistance*np.cos(theta)
        arrayFactor = np.exp(np.kron(np.arange(0, numAntennaElements), temp))
    arrayFactor = arrayFactor / np.sqrt(numAntennaElements)
    return arrayFactor  # normalize to have unitary norm

def plot_position_and_beam(csv_position_file,theta,beams_data,arrayFactor, codebook, tx,builds,animation = False):
    with open(csv_position_file, 'r') as f:
        insiteReader = csv.DictReader(f)
        sample = 0
        for row in insiteReader:
            isValid = row['Val'] #V or I are the first element of the list thisLine            
            if isValid != 'V': #filter the invalid channels 
                continue
            target = np.argmax(beams_data[sample,:])
            rx_coord = [float(row['x']),float(row['y'])]
            
            fig = plt.figure()
            ax = fig.add_subplot(121)
            for polygon in builds:
                x,y = polygon.exterior.xy
                ax.plot(x, y, color = 'black')
            ax.scatter(tx[0],tx[1], color = 'b') 
            ax.scatter(rx_coord[0],rx_coord[1], color = 'r') 
            ax.set_title('Tx Rx position')
            ax.set_ylim(350, 700)
            ax.set_xlim(660, 850)
            
            steeredArrayFactors = np.matmul(arrayFactor, codebook[:, target])
            ax1 = fig.add_subplot(122, polar=True) 
            ax1.set_title('Beams\n')
            ax1.plot(theta,np.absolute(steeredArrayFactors))
            plt.pause(2)
            if not(animation):
                if input('Continue ? (Press N to stop)') == 'n':
                    exit()
            plt.close(fig)
            sample += 1

def position_dist_per_beam(csv_position_file,theta,beams_data,desired_beam, arrayFactor, codebook, tx,builds):
    with open(csv_position_file, 'r') as f:
        insiteReader = csv.DictReader(f)
        sample = -1
        rx_x_coord = []
        rx_y_coord = []
        for row in insiteReader:
            isValid = row['Val'] #V or I are the first element of the list thisLine            
            if isValid != 'V': #filter the invalid channels 
                continue
            sample += 1
            target = np.argmax(beams_data[sample,:])
            if target != desired_beam:
                continue
            rx_x_coord.append(float(row['x']))
            rx_y_coord.append(float(row['y']))
            
        fig = plt.figure()
        ax = fig.add_subplot(121)
        for polygon in builds:
            x,y = polygon.exterior.xy
            ax.plot(x, y, color = 'black')
        ax.scatter(tx[0],tx[1], color = 'b') 
        ax.scatter(rx_x_coord,rx_y_coord, color = 'r') 
        ax.set_title('Tx Rx position')
        ax.set_ylim(350, 700)
        ax.set_xlim(660, 850)
        
        steeredArrayFactors = np.matmul(arrayFactor, codebook[:, desired_beam])
        ax1 = fig.add_subplot(122, polar=True) 
        ax1.set_title('Beams\n')
        ax1.plot(theta,np.absolute(steeredArrayFactors))
        plt.savefig(f'beam_{desired_beam}_position_distribution.png')
        #plt.show()
        plt.pause(1)
        #input('Press a key to continue!')
        plt.close(fig)
            