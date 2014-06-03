import QtQuick 2.2
import DPCS 1.0

//ver isso: http://stackoverflow.com/questions/23902968/pyqt5-executable-application-with-qml

Rectangle {
    width: 500
    height: 400

    Speaker {
        id: sp
    }
    
    Database {
        id: myData
    }

    Component {
        id: symbolDelegate
        Item {
            width: 100
            anchors.topMargin: 20
            y: 50
            Row {
                height: 45
                Text {
                    text: "\n"+name + "|" + stext + "|" + image
                    
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            sp.speak(name, stext)
                        }
                    }
                }
            }
        }
    }
    Component {
        id: categoryDelegate
        Column {
            width: 100
            Row {
                height: 200
                Text {
                    text: "Category: " + name
                }
                ListView {
                    model: symbols
                    delegate: symbolDelegate
                }
            }
        }
    }
    
    ListView {
        anchors.fill: parent

        model: myData.categories
        delegate: categoryDelegate
    }
    
    Text {
        id: falacoisa
        anchors.top: parent.top
        anchors.right: parent.right
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
        anchors.right: parent.right
        text: "Fecha janela"
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                Qt.quit();
            }
        }
    }
}
