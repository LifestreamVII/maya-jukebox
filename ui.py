from PySide2 import QtWidgets, QtGui, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import base64
import maya.cmds as cmds
import maya.mel as mel
import urllib.request
import os
import requests

def fetch_image_url(title, artist):
    try:
        url = f"https://maya.na-no.pro/cover/spotify/cover?title={title}&artist={artist}"
        
        response = requests.get(url)
        response.raise_for_status()
        image_url = response.json()["coverUrl"]
        return image_url
    
    except requests.RequestException as e:
        print(f"Erreur téléch. image: {e}")
        return None

    except Exception as e:
        print(f"Erreur téléch. image: {e}")
        return None

def fetch_screenshot(title, artist):
    try:
        url = f"https://maya.na-no.pro/cover/spotify/cover?title={title}&artist={artist}"
        
        response = requests.get(url)
        response.raise_for_status()
        image_url = response.json()["spotUrl"]
        dl_url = f"https://maya.na-no.pro/spotpage/take?url={image_url}&format=jpeg&viewport-width=1280&viewport-height=720&wait-until-event=networkidle2"
        return dl_url
    
    except requests.RequestException as e:
        print(f"Erreur téléch. image: {e}")
        return None
    
    except Exception as e:
        print(f"Erreur téléch. image: {e}")
        return None

def fetch_image(url, save_path):
    response = urllib.request.urlopen(url)
    with open(save_path, 'wb') as out_file:
        out_file.write(response.read())

def apply_texture_to_mesh(texture_path, mesh_name):
    file_node = cmds.shadingNode('file', asTexture=True, name="tex1")
    cmds.setAttr(file_node + '.fileTextureName', texture_path, type='string')
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="shading1")
    shader_node = cmds.shadingNode('lambert', asShader=True, name="shadingLambert")
    cmds.connectAttr(file_node + '.outColor', shader_node + '.color')
    cmds.connectAttr(shader_node + '.outColor', shading_group + '.surfaceShader')
    cmds.sets(mesh_name, e=True, forceElement=shading_group)

def adjust_timeline_to_animation():
    # Get the animation range
    start_time = cmds.playbackOptions(q=True, min=True)
    end_time = cmds.playbackOptions(q=True, max=True)

    # Adjust the timeline range to fit the animation
    cmds.playbackOptions(min=start_time, animationStartTime=start_time)
    cmds.playbackOptions(max=92, animationEndTime=end_time)

def apply_animation_1(mesh_name1, mesh_name2):
    cmds.select(mesh_name1, r=True)
    cmds.setKeyframe(attribute='translateZ', value=0.234, t=0, inTangentType="spline", outTangentType="flat")
    cmds.setKeyframe(attribute='translateZ', value=-0.02, t=20, inTangentType="flat", outTangentType="auto")
    cmds.select(mesh_name2, r=True)
    cmds.setKeyframe(attribute='rotateZ', value=180, t=0, inTangentType="auto", outTangentType="auto")
    cmds.setKeyframe(attribute='rotateZ', value=180, t=25, inTangentType="auto", outTangentType="auto")
    cmds.setKeyframe(attribute='rotateZ', value=0, t=50, inTangentType="slow", outTangentType="fast")
    cmds.select(clear=True)

def run_anim1(title, artist, model):
    image_url = fetch_image_url(title, artist)
    save_path = os.path.join(cmds.internalVar(userTmpDir=True), 'downloaded_texture.jpg')
    
    booklet = 'booklet'
    front_cover = 'front_cover'
    back_cover = 'back_cover'
    cd = 'cd'

    fetch_image(image_url, save_path)

    # Specify FBX import options
    cmds.FBXImportHardEdges('-v', False) 
    cmds.FBXImportUnlockNormals('-v', True) 
    cmds.FBXImportConstraints('-v', False)
    cmds.modelEditor('modelPanel4', e=True, displayTextures=True)
    
    # Do not import animation
    cmds.FBXImportSetTake('-takeIndex', 0) 
    
    # Do not show warnings
    cmds.FBXProperty('Import|AdvOptGrp|UI|ShowWarningsManager', '-v', 0)

    # Import the model
    cmds.file(model, i=True)

    # Apply the texture to the mesh
    apply_texture_to_mesh(save_path, booklet)
    apply_texture_to_mesh(save_path, back_cover)
    apply_texture_to_mesh(save_path, cd)

    apply_animation_1(cd, front_cover)
    cmds.play()

def run_anim2(title, artist, model):
    image_url = fetch_screenshot(title, artist)
    save_path = os.path.join(cmds.internalVar(userTmpDir=True), 'downloaded_texture.jpg')
    
    human = 'human'
    screen = 'screen'

    fetch_image(image_url, save_path)

    cmds.modelEditor('modelPanel4', e=True, displayTextures=True)
    
    # Do not show warnings
    cmds.FBXProperty('Import|AdvOptGrp|UI|ShowWarningsManager', '-v', 0)
    cmds.FBXImportSetTake('-takeIndex', 1) 

    # Import the model
    cmds.file(model, i=True)

    adjust_timeline_to_animation()

    if cmds.objExists(human):
        cmds.FrameSelected(cmds.select(human))

    apply_texture_to_mesh(save_path, screen)

    cmds.play()

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class SpotifUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SpotifUI, self).__init__(parent)
        self.setWindowTitle("Maya Jukebox")
        self.setFixedSize(300, 400)
        self.layout = QtWidgets.QVBoxLayout()
        self.status = ""
        self.model = None

    def init_ui(self):
        self.init_header_img()
        self.init_header_txt()
        self.init_inputs()
        self.init_radios()
        self.init_buttons()
        self.set_connections()
        self.set_layouts()

    def init_header_img(self):
        # Header Image
        header_image = QtWidgets.QLabel(self)
        header_image.setFixedWidth(280)
        header_image.setFixedHeight(150)
        header_image.setAlignment(QtCore.Qt.AlignCenter)
        header_image.setStyleSheet("border: 1px solid white;")
        
        # Load the image
        encoded_image = "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"
        image_data = base64.b64decode(encoded_image)
        image = QtGui.QImage.fromData(image_data)
        pixmap = QtGui.QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(header_image.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        header_image.setPixmap(scaled_pixmap)

        self.layout.addWidget(header_image)

    def init_header_txt(self):
        # Header Text
        header_text = QtWidgets.QLabel("Maya Jukebox", self)
        header_text.setAlignment(QtCore.Qt.AlignCenter)
        header_text.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.status_text = QtWidgets.QLabel(self.status, self)
        self.status_text.setAlignment(QtCore.Qt.AlignCenter)
        self.status_text.setStyleSheet("font-weight: normal; font-size: 12px;")
        self.layout.addWidget(header_text)
        self.layout.addWidget(self.status_text)

    def init_inputs(self):
        title = QtWidgets.QLabel("Titre d'album", self)
        self.layout.addWidget(title)
        self.title = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.title)
        artist = QtWidgets.QLabel("Nom d'artiste", self)
        self.layout.addWidget(artist)
        self.artist = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.artist)

    def init_radios(self):
        # Radio Buttons
        radio_layout = QtWidgets.QHBoxLayout()
        self.anim1 = QtWidgets.QRadioButton("Anim. Boîte CD", self)
        self.anim2 = QtWidgets.QRadioButton("Anim. Page Spotify", self)
        radio_layout.addWidget(self.anim1)
        radio_layout.addWidget(self.anim2)
        self.layout.addLayout(radio_layout)

    def init_buttons(self):
        # Confirm Button
        self.confirm_button = QtWidgets.QPushButton("Confirmer", self)
        self.layout.addWidget(self.confirm_button)

    def set_connections(self):
        self.confirm_button.clicked.connect(self.launch_anim)

    def set_layouts(self):
        self.setLayout(self.layout)

    def select_model_file(self):
        dialog_title = ""
        if self.anim1.isChecked():
            dialog_title = "Choisir le modèle de la boîte CD (cdmodel.fbx)"
        elif self.anim2.isChecked():
            dialog_title = "Choisir le modèle du bureau (desk.fbx)"
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            maya_main_window(),
            dialog_title,
        )
        if file_path:
            self.model = file_path
        else:
            raise Exception("Aucun fichier sélectionné...")

    def show(self):
        self.init_ui()
        return super().show()

    def launch_anim(self):
        try:
            if (self.anim1.isChecked() or self.anim2.isChecked()) and (self.title.text().strip() and self.artist.text().strip()):
                cmds.file(new=True, force=True)
                self.select_model_file()
                if self.anim1.isChecked():
                    self.status = "Lancement Animation 1..."
                    self.status_text.setText(self.status)
                    print(self.status)
                    run_anim1(self.title.text(), self.artist.text(), self.model)
                elif self.anim2.isChecked():
                    self.status = "Lancement Animation 2..."
                    self.status_text.setText(self.status)
                    print(self.status)
                    run_anim2(self.title.text(), self.artist.text(), self.model)
                else:
                    raise Exception("Aucune animation sélectionnée...")
            else:
                raise Exception("Veuillez remplir tous les champs...")
            
        except requests.RequestException as e:
            self.status = "Erreur : Problème réseau ou de téléchargement."
            self.status_text.setText(self.status)
            print(f"ERR Network : {e}")
        except OSError as e:
            self.status = "Erreur : Problème d'accès aux fichiers."
            self.status_text.setText(self.status)
            print(f"ERR IO: {e}")
        except Exception as e:
            self.status = f"Erreur : {e}"
            self.status_text.setText(self.status)
            print(f"Erreur : {e}")


if __name__ == '__main__':
    try:
        if "spotifui" in globals():
            globals()["spotifui"].deleteLater()
    except:
        pass

    spotifui = SpotifUI(parent=maya_main_window())
    spotifui.show()
