import random
print "|--------------------------------------------|"
print "|       Starting Facial Movement Demo        |"
print "|--------------------------------------------|"

# Add asset paths
scene.addAssetPath('mesh', 'mesh')
scene.addAssetPath('motion', 'ChrRachel')
scene.addAssetPath('script', 'scripts')
scene.loadAssets()

# Runs the default viewer for camera
scene.setScale(1.0)
scene.run('default-viewer.py')
camera = getCamera()
camera.setEye(0.0, 1.61, 0.33)
camera.setCenter(0.0, 1.61, -0.12)
camera.setUpVector(SrVec(0, 1, 0))
camera.setScale(1)
camera.setFov(1.0472)
camera.setFarPlane(100)
camera.setNearPlane(0.1)
camera.setAspectRatio(0.966897)

print 'Setting up joint map for Brad and Rachel'
scene.run('zebra2-map.py')
zebra2Map = scene.getJointMapManager().getJointMap('zebra2')
bradSkeleton = scene.getSkeleton('ChrRachel.sk')
zebra2Map.applySkeleton(bradSkeleton)
zebra2Map.applyMotionRecurse('ChrRachel')

# Setting up face definition
print 'Setting up Brad\'s face definition'
bradFace = scene.createFaceDefinition('ChrRachel')
bradFace.setFaceNeutral('ChrRachel@face_neutral')

bradFace.setAU(1,  "left",  "ChrRachel@001_inner_brow_raiser_lf")
bradFace.setAU(1,  "right", "ChrRachel@001_inner_brow_raiser_rt")
bradFace.setAU(2,  "left",  "ChrRachel@002_outer_brow_raiser_lf")
bradFace.setAU(2,  "right", "ChrRachel@002_outer_brow_raiser_rt")
bradFace.setAU(4,  "left",  "ChrRachel@004_brow_lowerer_lf")
bradFace.setAU(4,  "right", "ChrRachel@004_brow_lowerer_rt")
bradFace.setAU(5,  "both",  "ChrRachel@005_upper_lid_raiser")
bradFace.setAU(6,  "both",  "ChrRachel@006_cheek_raiser")
bradFace.setAU(7,  "both",  "ChrRachel@007_lid_tightener")
bradFace.setAU(10, "both",  "ChrRachel@010_upper_lip_raiser")
bradFace.setAU(12, "left",  "ChrRachel@012_lip_corner_puller_lf")
bradFace.setAU(12, "right", "ChrRachel@012_lip_corner_puller_rt")
bradFace.setAU(25, "both",  "ChrRachel@025_lips_part")
bradFace.setAU(26, "both",  "ChrRachel@026_jaw_drop")
bradFace.setAU(45, "left",  "ChrRachel@045_blink_lf")
bradFace.setAU(45, "right", "ChrRachel@045_blink_rt")

bradFace.setViseme("open",    "ChrRachel@open")
bradFace.setViseme("W",       "ChrRachel@W")
bradFace.setViseme("ShCh",    "ChrRachel@ShCh")
bradFace.setViseme("PBM",     "ChrRachel@PBM")
bradFace.setViseme("FV",      "ChrRachel@FV")
bradFace.setViseme("wide",    "ChrRachel@wide")
bradFace.setViseme("tBack",   "ChrRachel@tBack")
bradFace.setViseme("tRoof",   "ChrRachel@tRoof")
bradFace.setViseme("tTeeth",  "ChrRachel@tTeeth")

# Setting up Brad
print 'Setting up Brad'
brad = scene.createCharacter('ChrRachel', '')
bradSkeleton = scene.createSkeleton('ChrRachel.sk')
brad.setSkeleton(bradSkeleton)
brad.setFaceDefinition(bradFace)
brad.createStandardControllers()
# DeformableMesh
brad.setVec3Attribute('deformableMeshScale', .01, .01, .01)
brad.setStringAttribute('deformableMesh', 'ChrRachel.dae')

# Turn on GPU deformable geometry
brad.setStringAttribute("displayType", "GPUmesh")


# Update to repeat reaches
last = 0
canTime = True
delay = 2
class FacialMovementDemo(SBScript):
	def update(self, time):
		global canTime, last
		if canTime:
			last = time
			canTime = False
		diff = time - last
		if diff >= delay:
			diff = 0
			canTime = True
		# If time's up, do action
		if canTime:
			nextFace()


