import QtQuick 2.2  
import DPCS 1.0

import "qmlvar.js" as P

Rectangle {
    width: 800
    height: 800

    Database {
        id: myData
    }

    Speaker {
        id: sp
    }

    property int currentCategoryIndex: -1
    property int currentSymbolIndex: -1
    property bool isInCategory: false
    property bool selectedSymbol: false

    property Column currentColumn;
    property ListView currentSymbols;

    property int timerIntervalInSeconds: 3
    property int symbolCount: 0

    function currentCategory() {                 
        return myData.categories[currentCategoryIndex];
    }

    function currentCategoryName() {
        return currentCategory().name;
    }

    function performClick() {
        if (!isInCategory) {
            selectCategory(currentCategoryIndex);
        }
        else {
            var symbolInModel = myData.categories[currentCategoryIndex].symbols[currentSymbolIndex].name;

            if (symbolInModel === "voltar") {
                isInCategory = false;
                P.unselect(currentCategoryName());
            }
            else {
                sp.speak(symbolInModel, myData.categories[currentCategoryIndex].symbols[currentSymbolIndex].sText)
                console.log(symbolInModel);
            }
        }
    }

    function debugProperties() {
        console.log("\n");
        console.log("currentCategoryIndex: " + currentCategoryIndex);
        console.log("currentSymbolIndex: " + currentSymbolIndex);
        console.log("numberOfCategories: " + myData.categories.length);
        console.log("isInCategory: " + isInCategory);
        console.log("selectedSymbol: " + selectedSymbol);
        console.log("currentColumn: " + currentColumn);
        console.log("currentSymbols: " + currentSymbols);
        console.log("currentSymbolRect: " + currentSymbolRect);
        console.log("timerIntervalInSeconds: " + timerIntervalInSeconds);
        console.log("symbolCount: " + symbolCount);
    }

    function tick() {
        if (selectedSymbol) {
        }
        else if (isInCategory) {
            currentSymbolIndex = (currentSymbolIndex + 1) % symbolCount;
            currentSymbols.currentIndex = currentSymbolIndex
            currentSymbols.update();
        }
        else {
            currentCategoryIndex = (currentCategoryIndex + 1) % myData.categories.length
            categoryList.currentIndex = currentCategoryIndex
        }
    }

    function selectCategory(index) {
        for (var i = 0; i < myData.categories.length; i++) {
            if (i !== index) {
                P.unselect(myData.categories[i].name);
            }
        }

        var myCat = myData.categories[index];
        P.select(myCat.name);
        
        for (var j = 0; j < currentColumn.children.length; j++) {
            currentSymbols = currentColumn.children[j];
            console.log(currentColumn.children[j]);
        }

        // Colocando o numero de simbolos dessa categoria
        symbolCount = myCat.symbols.length;
        console.log("Encontrados " + symbolCount + " simbolos");

        isInCategory = true;
    }

    Timer {
        interval: timerIntervalInSeconds * 1000;
        repeat: true;
        running: true;
        onTriggered: { tick(); }
    }

    Rectangle {
        x: 10
        y: 10
        width: 60
        height: 60
        border.color: "black"
        radius: 50

        gradient: Gradient {
            GradientStop { position: 0.0; color: "lightgreen" }
            GradientStop { position: 1.0; color: "darkgreen" }
        }

        Text {
            text: "CLICK"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                performClick()
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

    ListView {
        id: categoryList
        x: 0
        anchors.fill: parent
        anchors.topMargin: 120
        model: myData.categories

        delegate: Column {
            id: columnComponent
            width: 800

            Item {
                height: 100
                width: 800
                
                Rectangle {
                    anchors.fill: parent
                    border.color: "transparent"
                    color: columnComponent.ListView.isCurrentItem ? "transparent" : ccolor

                    Image {
                        width: 80
                        height: 80
                        x: 10
                        anchors.verticalCenter: parent.verticalCenter
                        source: image
                    }

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        x: 100
                        font.pixelSize: 20
                        text: name + " (" + symbols.length + ")"
                    }
                }

                
            }


            Loader {
                   id: subItemLoader

                   visible: name === currentCategoryName()
                   property variant subItemModel : symbols
                   sourceComponent: name === currentCategoryName() ? subItemColumnDelegate : null
                   onStatusChanged: {
                        if (status == Loader.Ready) item.model = subItemModel
                        currentColumn = item
                    }
               }
        }

        highlight: Component {
            Rectangle {
                height: 150
                width: 800
                border.color: "red"
                border.width: 5
                z: 1
            }
        }
    }

    Component {
        id: subItemColumnDelegate
        Column {
            property alias model : subItemRepeater.model
            width: 750

            ListView {
                width: 550
                x: 240
                y: 12
                id: subItemRepeater
                orientation: ListView.Horizontal

                highlight: Component { Rectangle {
                    width:  80
                    height: 70
                    color: "transparent"
                    border.color: "red"
                    border.width: 5
                }
                }

                delegate: Component {
                    Rectangle {
                        color: "transparent"
                        width: 80
                        height: 70

                        Image {
                            x: 5
                            y: 5
                            width: 70
                            height: 60
                            source: image
                        }
                    }
                }

            }
        }
    }

    Component.onCompleted: { 
        tick(); 
    }
}