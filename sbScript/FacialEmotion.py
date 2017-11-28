import random
import GUIInterface

print "|--------------------------------------------|"
print "|           Loading the Agent ...            |"
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
print 'Setting up Rachel\'s face definition'
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
print 'Setting up Rachel'
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


class TestInterface(GUIInterface.SBInterfaceListener):
	def onMouseClick(self, x,y,button):
		nextFace()

	def onKeyboardPress(self, c):
		if '1'<= c and c <='5':
			defaultFace(int(c))
		else:
			print("Pressed Invalid Key")

# List of expressions
expressionList = ['sad', 'shock', 'angry', 'happy', 'fear']
auList = ["1_left", "1_right", \
         "2_left", "2_right", \
         "4_left", "4_right", \
         "5", "6", "7", "10", \
         "12_left", "12_right", \
         "25", "26", "45_left", "45_right"]
chrName = 'ChrRachel'
curFace = 0
faceAmt = len(expressionList)
# List of expressions, choice list, get and call function		

def changeExpression(AUValues):
	auSize = len(AUValues)
	descptString = ''
	for i in range(auSize):
		auTag = auList[i]
		auValue = AUValues[i]
		descptString += '<face type="faces" au=' + auTag + ' amount="' + str(auValue) + '"/>'
		bml.execBML(chrName, descptString)

#def reactFace():
    # 1. Appraisal, get emotion states
    # 2. Using emotion states to get AUValues
    #changeExpression(AUValues)

def nextFace():
	global curFace
	expression = expressionList[curFace]
	if expression == 'sad': 
		print 'Playing sad'
		bml.execBML(chrName, '<face type="facs" au="1_left" amount="1"/><face type="facs" au="1_right" amount="1"/> + \
							  <face type="facs" au="4_left" amount="1"/><face type="facs" au="4_right" amount="1"/> + \
							  <face type="facs" au="6" amount="0.58"/>')
	if expression == 'happy':
		print 'Playing happy'
		bml.execBML(chrName, '<face type="facs" au="6" amount="1"/><face type="facs" au="12" amount="1"/>')
	if expression == 'angry':
		print 'Playing angry'
		bml.execBML(chrName, '<face type="facs" au="2_left" amount="1"/><face type="facs" au="2_right" amount="1"/> + \
							  <face type="facs" au="4_left" amount="1"/><face type="facs" au="4_right" amount="1"/> + \
							  <face type="facs" au="5" amount="0.68"/><face type="facs" au="7" amount="0.5"/> + \
							  <face type="facs" au="10" amount="1"/><face type="facs" au="26" amount="0.22"/>')
	if expression == 'shock':
		print 'Playing shock'
		bml.execBML(chrName, '<face type="facs" au="1_left" amount="1"/><face type="facs" au="1_right" amount="1"/> + \
							  <face type="facs" au="5" amount="0.86"/><face type="facs" au="26" amount="0.73"/>')
	if expression == 'fear':
		print 'Playing fear'
		bml.execBML(chrName, '<face type="facs" au="1_left" amount="0.6"/><face type="facs" au="1_right" amount="0.6"/> + \
							  <face type="facs" au="5" amount="0.7"/><face type="facs" au="26" amount="0.25"/> + \
							  <face type="facs" au="38" amount="1"/>')
	# Increment index, reset when hit max
	curFace = curFace + 1
	if curFace >= faceAmt:
		curFace = 0

def defaultFace(faceId):
	if 1 == faceId:
		print 'Playing sad'
		bml.execBML(chrName, '<face type="facs" au="1_left" amount="1"/><face type="facs" au="1_right" amount="1"/> + \
							  <face type="facs" au="4_left" amount="1"/><face type="facs" au="4_right" amount="1"/> + \
							  <face type="facs" au="6" amount="0.58"/>')
	if 2 == faceId:
		print 'Playing happy'
		bml.execBML(chrName, '<face type="facs" au="6" amount="1"/><face type="facs" au="12" amount="1"/>')
	if 3 == faceId:
		print 'Playing angry'
		bml.execBML(chrName, '<face type="facs" au="2_left" amount="1"/><face type="facs" au="2_right" amount="1"/> + \
							  <face type="facs" au="4_left" amount="1"/><face type="facs" au="4_right" amount="1"/> + \
							  <face type="facs" au="5" amount="0.68"/><face type="facs" au="7" amount="0.5"/> + \
							  <face type="facs" au="10" amount="1"/><face type="facs" au="26" amount="0.22"/>')
	if 4 == faceId:
		print 'Playing shock'
		bml.execBML(chrName, '<face type="facs" au="1_left" amount="1"/><face type="facs" au="1_right" amount="1"/> + \
							  <face type="facs" au="5" amount="0.86"/><face type="facs" au="26" amount="0.73"/>')
	if 5 == faceId:
		print 'Playing fear'
		bml.execBML(chrName, '<face type="facs" au="1_left" amount="0.6"/><face type="facs" au="1_right" amount="0.6"/> + \
							  <face type="facs" au="5" amount="0.7"/><face type="facs" au="26" amount="0.25"/> + \
							  <face type="facs" au="38" amount="1"/>')


print "|--------------------------------------------|"
print "|          The Student Is Ready Now          |"
print "|--------------------------------------------|"

t = TestInterface()
m = GUIInterface.getInterfaceManager()
m.addInterfaceListener(t)
