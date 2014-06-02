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
        anchors.centerIn: parent
        text: "Hello World"
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                //Qt.quit();
                sp.speak("deletaMe", "Testando 1 2 3")
            }
        }
    }
    
    
    /*Button {
        x: 10
        y: 10
        text: "fala"
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                
            }
        }
    }*/
}
