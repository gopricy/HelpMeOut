import random
import subprocess as sp
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


# Update to repeat reaches
last = 0
canTime = True
delay = 0.7
p = sp.Popen('cd /Users/congxin/Documents/HelpMeOut && python -u product.py', \
	stdin = sp.PIPE, stdout = sp.PIPE, shell = True)

class test(SBScript):
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

chrName = 'ChrRachel'

emotions = ['0. 0. 0. 0. 0. 0. 0.3', '0. 0. 0. 0. 0. 0. 0.6', '0. 0. 0. 0. 0. 0. 0.9']
feed_dict = ['Punishment', 'Nothing', 'Praise']
# List of expressions, choice list, get and call function
def nextFace():
	feedback = raw_input('what would you do to the student? Punishment(0), Nothing(1), Praise(2)')
	print("your choice is: " + feed_dict[int(feedback)])
	dif = raw_input('input the difficulty:')
	print("your choice is: " + dif)
	print >>p.stdin, emotions[int(dif)]
	aus = p.stdout.readline()
	aus = aus.split()
	aus = [float(i) for i in aus]
	# bml.execBML(chrName, '<face type="facs" au="1_left" amount="1"/><face type="facs" au="1_right" amount="1"/> + \
	# 						<face type="facs" au="4_left" amount="1"/><face type="facs" au="4_right" amount="1"/> + \
	# 						<face type="facs" au="6" amount="0.58"/>')
	bml.execBML(chrName, '<face type="facs" au="1_left" amount="{}"/><face type="facs" au="1_right" amount="{}"/>\
		<face type="facs" au="2_left" amount="{}"/><face type="facs" au="2_right" amount="{}"/>\
		<face type="facs" au="4_left" amount="{}"/><face type="facs" au="4_right" amount="{}"/>\
		<face type="facs" au="5" amount="{}"/><face type="facs" au="6" amount="{}"/>\
		<face type="facs" au="7" amount="{}"/><face type="facs" au="10" amount="{}"/>\
		<face type="facs" au="12_left" amount="{}"/><face type="facs" au="12_right" amount="{}"/>\
		<face type="facs" au="25" amount="{}"/><face type="facs" au="26" amount="{}"/>\
		<face type="facs" au="45_left" amount="{}"/><face type="facs" au="45_right" amount="{}"/>'.format(*aus))

# Run the update script
scene.removeScript('test')
test = test()
scene.addScript('test', test)
