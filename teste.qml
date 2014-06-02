import QtQuick 2.2
import Speaker 1.0

//ver isso: http://stackoverflow.com/questions/23902968/pyqt5-executable-application-with-qml

Rectangle {
    width: 360
    height: 360

    Speaker {
        id: sp
    }

    Text {
        id: falacoisa
        anchors.centerIn: parent
        text: "Fala mensagem teste"
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                sp.speak("deletaMe", "Testando 1 2 3")
            }
        }
    }
    
    
    Text {
        anchors.top: falacoisa.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        text: "Fecha janela"
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                Qt.quit();
            }
        }
    }
}
