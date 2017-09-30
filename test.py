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

print 'Setting up joint map for Rachel and Rachel'
scene.run('zebra2-map.py')
zebra2Map = scene.getJointMapManager().getJointMap('zebra2')
rachelSkeleton = scene.getSkeleton('ChrRachel.sk')
zebra2Map.applySkeleton(rachelSkeleton)
zebra2Map.applyMotionRecurse('ChrRachel')

# Setting up face definition
print 'Setting up Rachel\'s face definition'
rachelFace = scene.createFaceDefinition('ChrRachel')
rachelFace.setFaceNeutral('ChrRachel@face_neutral')

rachelFace.setAU(1,  "left",  "ChrRachel@001_inner_brow_raiser_lf")
rachelFace.setAU(1,  "right", "ChrRachel@001_inner_brow_raiser_rt")
rachelFace.setAU(2,  "left",  "ChrRachel@002_outer_brow_raiser_lf")
rachelFace.setAU(2,  "right", "ChrRachel@002_outer_brow_raiser_rt")
rachelFace.setAU(4,  "left",  "ChrRachel@004_brow_lowerer_lf")
rachelFace.setAU(4,  "right", "ChrRachel@004_brow_lowerer_rt")
rachelFace.setAU(5,  "both",  "ChrRachel@005_upper_lid_raiser")
rachelFace.setAU(6,  "both",  "ChrRachel@006_cheek_raiser")
rachelFace.setAU(7,  "both",  "ChrRachel@007_lid_tightener")
rachelFace.setAU(10, "both",  "ChrRachel@010_upper_lip_raiser")
rachelFace.setAU(12, "left",  "ChrRachel@012_lip_corner_puller_lf")
rachelFace.setAU(12, "right", "ChrRachel@012_lip_corner_puller_rt")
rachelFace.setAU(25, "both",  "ChrRachel@025_lips_part")
rachelFace.setAU(26, "both",  "ChrRachel@026_jaw_drop")
rachelFace.setAU(45, "left",  "ChrRachel@045_blink_lf")
rachelFace.setAU(45, "right", "ChrRachel@045_blink_rt")

rachelFace.setViseme("open",    "ChrRachel@open")
rachelFace.setViseme("W",       "ChrRachel@W")
rachelFace.setViseme("ShCh",    "ChrRachel@ShCh")
rachelFace.setViseme("PBM",     "ChrRachel@PBM")
rachelFace.setViseme("FV",      "ChrRachel@FV")
rachelFace.setViseme("wide",    "ChrRachel@wide")
rachelFace.setViseme("tBack",   "ChrRachel@tBack")
rachelFace.setViseme("tRoof",   "ChrRachel@tRoof")
rachelFace.setViseme("tTeeth",  "ChrRachel@tTeeth")

# Setting up Rachel
print 'Setting up Rachel'
rachel = scene.createCharacter('ChrRachel', '')
rachelSkeleton = scene.createSkeleton('ChrRachel.sk')
rachel.setSkeleton(rachelSkeleton)
rachel.setFaceDefinition(rachelFace)
rachel.createStandardControllers()
# DeformableMesh
rachel.setVec3Attribute('deformableMeshScale', .01, .01, .01)
rachel.setStringAttribute('deformableMesh', 'ChrRachel.dae')

# Turn on GPU deformable geometry
rachel.setStringAttribute("displayType", "GPUmesh")


# # Update to repeat reaches
# last = 0
# canTime = True
# delay = 2
# class test(SBScript):
# 	def update(self, time):
# 		global canTime, last
# 		if canTime:
# 			last = time
# 			canTime = False
# 		diff = time - last
# 		if diff >= delay:
# 			diff = 0
# 			canTime = True
# 		# If time's up, do action
# 		if canTime:
# 			nextFace()

# # List of expressions
# expressionList = ['sad', 'shock', 'angry', 'happy', 'fear']
# chrName = 'ChrRachel'
# curFace = 0
# faceAmt = len(expressionList)
# # List of expressions, choice list, get and call function		
# def nextFace():
# 	global curFace
# 	expression = expressionList[curFace]
# 	if expression == 'sad': 
# 		print 'Playing sad'
# 		bml.execBML(chrName, '<face type="facs" au="1_left" amount="1"/><face type="facs" au="1_right" amount="1"/> + \
# 							  <face type="facs" au="4_left" amount="1"/><face type="facs" au="4_right" amount="1"/> + \
# 							  <face type="facs" au="6" amount="0.58"/>')
# 	if expression == 'happy':
# 		print 'Playing happy'
# 		bml.execBML(chrName, '<face type="facs" au="6" amount="1"/><face type="facs" au="12" amount="1"/>')
# 	if expression == 'angry':
# 		print 'Playing angry'
# 		bml.execBML(chrName, '<face type="facs" au="2_left" amount="1"/><face type="facs" au="2_right" amount="1"/> + \
# 							  <face type="facs" au="4_left" amount="1"/><face type="facs" au="4_right" amount="1"/> + \
# 							  <face type="facs" au="5" amount="0.68"/><face type="facs" au="7" amount="0.5"/> + \
# 							  <face type="facs" au="10" amount="1"/><face type="facs" au="26" amount="0.22"/>')
# 	if expression == 'shock':
# 		print 'Playing shock'
# 		bml.execBML(chrName, '<face type="facs" au="1_left" amount="1"/><face type="facs" au="1_right" amount="1"/> + \
# 							  <face type="facs" au="5" amount="0.86"/><face type="facs" au="26" amount="0.73"/>')
# 	if expression == 'fear':
# 		print 'Playing fear'
# 		bml.execBML(chrName, '<face type="facs" au="1_left" amount="0.6"/><face type="facs" au="1_right" amount="0.6"/> + \
# 							  <face type="facs" au="5" amount="0.7"/><face type="facs" au="26" amount="0.25"/> + \
# 							  <face type="facs" au="38" amount="1"/>')
# 	# Increment index, reset when hit max
# 	curFace = curFace + 1
# 	if curFace >= faceAmt:
# 		curFace = 0

# # Run the update script
# scene.removeScript('test')
# test = test()
# scene.addScript('test', test)
