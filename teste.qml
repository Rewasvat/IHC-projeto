import QtQuick 2.2
import DPCS 1.0
import QtMultimedia 5.0

//ver isso: http://stackoverflow.com/questions/23902968/pyqt5-executable-application-with-qml

Rectangle {
    width: 800
    height: 700

    Speaker {
        id: sp
    }
    
    Database {
        id: myData
    }

    Component {
        id: symbolDelegate
        Row {
            id: sWrapper
            Row {
                Image {
                    id: symImg
                    anchors.centerIn: sWrapper
                    
                    width:  sWrapper.PathView.isCurrentItem ? 80 : 64
                    height: sWrapper.PathView.isCurrentItem ? 80 : 64
                    source: image
                }
            }
        }
    }
    Component {
        id: categoryDelegate
        Column {
            id: cWrapper
            Rectangle {
                color: ccolor
                id: rect
                anchors.verticalCenter: cWrapper.verticalCenter
                width: 760
                height: cWrapper.PathView.isCurrentItem ? 88 : 70
                
                border.color: "black"
                border.width: cWrapper.PathView.isCurrentItem ? 8 : 0
                opacity: cWrapper.PathView.isCurrentItem ? 1.0 : 0.6
                
            }
            Image {
                id: catImg
                anchors.left: rect.left
                anchors.leftMargin: 10
                anchors.verticalCenter: cWrapper.verticalCenter
                
                width: 64; height: 64
                source: image
            }
            Text {
                text: name + " (" + count + ")"
                font.pointSize: 16
                anchors.left: catImg.right
                anchors.leftMargin: 10
                anchors.verticalCenter: cWrapper.verticalCenter
            }
        }
    }
    
    Image {
        width: 340
        height: 110
        x: (parent.width - width)/2;
        y: 10
        source: "simbolos/dpcs.jpg"
    }
    
    PathView {
        id: categoryView
        anchors.fill: parent
        visible: false
        model: myData.categories
        delegate: categoryDelegate
        
        preferredHighlightBegin: 0.5
        preferredHighlightEnd: 0.5
        path: Path {
            startX: 20
            startY: 120
            PathLine { x: 20; y: 680 }
        }
        
        Keys.onSpacePressed: {
            symbolView.model = myData.categories[categoryView.currentIndex].symbols
            symbolView.visible = true
            symbolView.focus = true
            categoryView.focus = false
        }
    }
    
    PathView {
        id: symbolView
        visible: false
        delegate: symbolDelegate

        preferredHighlightBegin: 0.5
        preferredHighlightEnd: 0.5
        path: Path {
            startX: 200
            startY: 400
            PathLine { x: 780; y: 400 }
        }
        
        Keys.onSpacePressed: {
            var sym = myData.categories[categoryView.currentIndex].symbols[symbolView.currentIndex]
            
            sp.speak(sym.name, sym.stext)
            symbolView.visible = false
        
            symbolView.focus = false
            categoryView.focus = true
        }
    }
    
    Timer { 
        id: iterator
        interval: myData.rotationTime * 1000
        repeat: true
        running: false
        onTriggered: symbolView.visible ? symbolView.incrementCurrentIndex() : categoryView.incrementCurrentIndex()
    }
    
    Video {
        id: tutorial
        anchors.fill: parent
        source: "tuturialDPCS.wmv"
        autoLoad: true
        autoPlay: true
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                tutorial.visible = false
                categoryView.visible = true
                categoryView.focus = true
                iterator.running = true
            }
        }
        
        onStopped: {
            tutorial.visible = false
            categoryView.visible = true
            categoryView.focus = true
            iterator.running = true
        }
        
        focus: true
        Keys.onSpacePressed: {
            tutorial.visible = false
            categoryView.visible = true
            categoryView.focus = true
            iterator.running = true
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
