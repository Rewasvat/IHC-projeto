import QtQuick 2.0
import DPCS 1.0

import "sentenceManage.js" as Sentence

Rectangle {
    width:  600
    height: 240
    color: "white"

    property int fontSize: 20
    property int currentMenuIndex: 0
    property bool isFocused: false
    property bool clicked: false
    property bool goBack: false
    property variant myModel: [] 

    Database {
        id: myData;
    }

    Speaker {
        id: sp
    }

    function tick() {
        if (isFocused) {
            currentMenuIndex = (currentMenuIndex + 1) % 4;
            options.currentIndex = currentMenuIndex;
        }
        else {
            options.currentIndex = -1;
        }
    }

    function clickCheck() {
        if (clicked) {
            var currentOption = options.model.get(currentMenuIndex);
            console.log(currentOption.txt);

            if (currentOption.txt === 'Voltar') {
                isFocused = false;
                goBack = true;
            }
            else if (currentOption.txt === 'Falar') {
                Sentence.SManager.speakCurrentSentence(sp);
            }

            clicked = false;
        }
    }

    Timer {
        id: clickTimer
        interval: 400
        running: true
        repeat: true
        onTriggered: { clickCheck(); }
    }

    Timer {
        interval: 4000;
        repeat: true;
        running: true;
        onTriggered: { tick(); }
    }

    ListView {
        id: sentences
        height: parent.height * 0.6
        width: parent.width
        orientation: ListView.Vertical
        model: myModel
        x: 10
        y: 10
        spacing: 10
        delegate: Text {
             color: "red"
             text: Sentence.SManager.getText(modelData.symbols)
             font.pixelSize: fontSize
        }
    }

    ListView {
        id: options
        height: parent.height
        width: 510

        anchors.top: sentences.bottom
        orientation: ListView.Horizontal
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 10

        model: ListModel {
            ListElement {
                img: "icones/speak.png"
                txt: "Falar"
            }


            ListElement {
                img: "icones/setaVoltar.png"
                txt: "Voltar"
            }

            ListElement {
                img: "icones/back.png"
                txt: "Limpar Um"
            }

            ListElement {
                img: "icones/lixeira.png"
                txt: "Limpar Tudo"
            }
            
        }

        highlight: Rectangle {
            height: 120
            width: 140
            color: "yellow"
            border.color: "red"
            border.width: 4
            z: 5
        }

        delegate: Rectangle {
            z: 0
            width: 120  
            height: 100
            color: "transparent"
            Image {
                anchors.fill: parent
                source: img
                anchors.margins: 10
                z: 0
            }
        }
    }

    function appendSymbol(symbol) {

    }


    Component.onCompleted: {
    	/*var cat = myData.categories[1];

    	Sentence.Util.forEach(cat.symbols, function (el, idx) {
    		if (el.name !== 'voltar')
    			Sentence.SManager.append(el);
    	});

        // Sentence.SManager.speakCurrentSentence(sp);

    	sentences.model = Qt.binding(function () { return Sentence.SDatabase.select(); });

        tick();*/
    }
}
