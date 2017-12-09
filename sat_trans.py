import argparse
import math
import numpy as np
import transforms3d as td

def asCartesian(rthetaphi):
    #takes list rthetaphi (single coord)
    r       = rthetaphi[0]
    theta   = rthetaphi[1]* np.pi/180 # to radian
    phi     = rthetaphi[2]* np.pi/180
    x = r * math.sin( theta ) * math.cos( phi )
    y = r * math.sin( theta ) * math.sin( phi )
    z = r * math.cos( theta )
    return [x,y,z]

def asSpherical(xyz):
    #takes list xyz (single coord)
    x       = xyz[0]
    y       = xyz[1]
    z       = xyz[2]
    r       =  math.sqrt(x*x + y*y + z*z)
    theta   =  math.acos(z/r)*180/ np.pi #to degrees
    phi     =  math.atan2(y,x)*180/ np.pi
    return [r,theta,phi]

#asCartesian(asSpherical([-2.13091326,-0.0058279,0.83697319]))

def azi_ele(x,y,z,sx=0,sy=45,sz=192):
    """
        x = roll
        y = pitch
        z = yaw
        x,y,z : current antenna euler angle in degreee
        sx,sy,sz : satellite euler anlge in degree
        return : euler azimuth and elevation for ratation from antena to satellite
    """
    # rotation matrix of antenna
    rot_ant = td.euler.euler2mat(np.radians(z),np.radians(y),np.radians(x), 'rzyx')
    #print ('rot_ant:\r\n', rot_ant)
    # rotation matrix from antenna to satelite, rotate only azimuth
    azimuth = sz-z
    rot_a2s = td.euler.euler2mat(np.radians(azimuth),np.radians(0),np.radians(0), 'rzyx')
    #print ('rot_a2s:\r\n', rot_a2s)
    # rotation matrix of satellite, azimuth only
    rot_r2s = np.dot(rot_ant, rot_a2s)
    #print ('rot_r2s:\r\n', rot_r2s)
    vec_r2s = np.dot(rot_r2s, [1,0,0])
    #print ('vec_r2s:\r\n', vec_r2s)
    r, theta, phi = asSpherical(vec_r2s)
    #print ('theta = ', theta)
    elevation = sy - (theta - 90)
    return [azimuth, elevation]
    
def rot_atos(x,y,z,sx=0,sy=45,sz=192):
    """
        x = roll
        y = pitch
        z = yaw
        x,y,z : current antenna euler angle in degree
        sx,sy,sz : satellite euler anlge in degree
        return : rotation matrix from antena to satellite
        use inverse matix
        antenna -> start, [1,0,0] -> satellite
    """   
    # rotation matrix of satelite
    rot_sat = td.euler.euler2mat(np.radians(sz),np.radians(sy),np.radians(sx), 'rzyx')  
    # rotation matrix of antenna
    rot_ant = td.euler.euler2mat(np.radians(z),np.radians(y),np.radians(x), 'rzyx')
    # inverse matirx
    rot_inv = np.linalg.inv(rot_ant)
    # rotation matrix from antenna to satelite
    rot_a2s = np.dot(rot_sat, rot_inv)
    return rot_a2s

def rot_atos2(x,y,z,sx=0,sy=45,sz=192):
    """
        x = roll
        y = pitch
        z = yaw
        x,y,z : current antenna euler angle in degree
        sx,sy,sz : satellite euler anlge in degree
        return : rotation matrix from antena to satellite
        do not use use inverse matix
        antenna -> start, [1,0,0] -> satellite
    """
    # rotation matrix of satelite
    rot_sat = td.euler.euler2mat(np.radians(sz),np.radians(sy),np.radians(sx), 'rzyx')
    # reverse rotation matrix of antenna
    rot_rev = td.euler.euler2mat(np.radians(-x),np.radians(-y),np.radians(-z), 'rxyz')
    # rotation matrix from antenna to satelite
    rot_a2s = np.dot(rot_sat, rot_rev)
    # return enuler anlge    
    az,ay,ax = np.degrees(td.euler.mat2euler(rot_a2s, 'rzyx'))
    return rot_a2s

if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser(description="Rotate antenna to satellite")
    parser.add_argument('xyz', type=float, nargs = 3, help ="x:roll, y:pitch, z:yaw")
    #parser.add_argument('-s', '--s',type=float, nargs = 3, help ="sx:roll, sy:pitch, sz:yaw")
    # add expected arguments
    # parse args
    args = parser.parse_args()    
    azimuth, elevation = azi_ele(args.xyz[0], args.xyz[1], args.xyz[2])
    print('Antenna   yaw=%3d,  pitch=%3d, roll=%d' % (args.xyz[2], args.xyz[1], args.xyz[0]))
    print('Satellite yaw=192,  pitch= 45, roll=0')
    print('Azimuth   = ', azimuth)
    print('Elevation = ', elevation)
    