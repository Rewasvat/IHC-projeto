import QtQuick 2.0
import DPCS 1.0

import "sentenceManage.js" as Sentence

Rectangle {
    id: mainWindow
    width: 1280
    height: 720

    property int timerIntervalInSeconds: 2

    property int currentIndex: 0
    property int currentCategoryIndex: -1

    property bool isInCategory: false  

    function tick() {

        if (sentenceComponent.goBack) {
            circularView.model = myData.categories;
            isInCategory = false;
            currentIndex = 0;

            sentenceComponent.goBack = false;

            mainWindow.color = "white";
        }
        else if (!isInCategory) {
            currentIndex = (currentIndex + 1) % myData.categories.length;
        }
        else {
            currentIndex = (currentIndex + 1) % myData.categories[currentCategoryIndex].symbols.length;
        }

        circularView.currentIndex = currentIndex;
    }

    function _click() {
        if (sentenceComponent.isFocused) {
            sentenceComponent.clicked = true;
        }
        else if (!isInCategory) {
            console.log('etering a category (' + myData.categories[currentIndex].name + ')...');
            sp.speak(myData.categories[currentIndex].name, myData.categories[currentIndex].name);

            var currentCategory = myData.categories[currentIndex];

            if (currentCategory.name == 'Tocar') {
                sentenceComponent.isFocused = true;
            }

            circularView.model = currentCategory.symbols;
            currentCategoryIndex = currentIndex;
            currentIndex = 0;

            mainWindow.color = myData.categories[currentCategoryIndex].ccolor;

            isInCategory = true;
        }
        else {
            var currentSymbol = myData.categories[currentCategoryIndex].symbols[currentIndex];
            
            if (currentSymbol.name === "voltar") {
                circularView.model = myData.categories;
                isInCategory = false;
                currentIndex = 0;

                mainWindow.color = "white";
            }
            else {
                Sentence.SManager.append(currentSymbol);
                sentenceComponent.myModel = Qt.binding(function () { return Sentence.SDatabase.select(); });
            }

            sp.speak(currentSymbol.name, currentSymbol.sText);
        }
    }

    Timer {
        interval: timerIntervalInSeconds * 1000;
        repeat: true;
        running: true;
        onTriggered: { tick(); }
    }

    MouseArea {
        anchors.fill: parent
        z: 1
        onClicked: {
            _click();
        }
    }

    Database {
        id: myData
    }

    Speaker {
        id: sp
    }

    Image {
        source: "simbolos/dpcs.jpg"
        width: 322
        height: 70
        x: 10
        y: 10
    }

    CircularCategoryView {
        id: circularView
        anchors.fill: parent
        model:        myData.categories
    }

    SentenceManager {
        id: sentenceComponent
        x: parent.width / 2 - width / 2
        y: parent.height / 2 - height / 2
        border.color: "red"
    }

    Component.onCompleted: {
        tick();
    }
}
