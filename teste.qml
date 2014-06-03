import QtQuick 2.2
import DPCS 1.0

//ver isso: http://stackoverflow.com/questions/23902968/pyqt5-executable-application-with-qml

Rectangle {
    width: 800
    height: 600

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
            id: wrapper
            Rectangle {
                color: "red"
                id: rect
                anchors.verticalCenter: wrapper.verticalCenter
                width: 760
                height: 70
            }
            Image {
                id: catImg
                anchors.left: rect.left
                anchors.leftMargin: 10
                anchors.verticalCenter: wrapper.verticalCenter
                
                width: 64; height: 64
                source: image
            }
            Text {
                text: name
                font.pointSize: 16
                color: wrapper.PathView.isCurrentItem ? "red" : "black"
                anchors.left: catImg.right
                anchors.leftMargin: 10
                anchors.verticalCenter: wrapper.verticalCenter
            }
            
        }
    }
    
    PathView {
        id: categoryView
        anchors.fill: parent

        model: myData.categories
        delegate: categoryDelegate
        
        preferredHighlightBegin: 0.5
        preferredHighlightEnd: 0.5
        path: Path {
            startX: 20
            startY: 20
            PathLine { x: 20; y: 580 }
        }
        
        Timer { 
            interval: myData.tempoDeRotacao * 1000
            repeat: true
            running: true
            onTriggered: categoryView.incrementCurrentIndex()
        }
    }
    
    
    Text {
        anchors.top: parent.top
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
